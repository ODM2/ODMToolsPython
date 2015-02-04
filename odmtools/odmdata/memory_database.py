
import sqlite3
import pandas as pd
import timeit
import logging
from odmtools.common.logger import LoggerTool
from odmtools.odmservices import SeriesService
from odmtools.common.taskServer import TaskServerMP
from multiprocessing import cpu_count, freeze_support

tool = LoggerTool()
logger = tool.setupLogger(__name__, __name__ + '.log', 'w', logging.DEBUG)
class MemoryDatabase(object):
### this code should be changed to work with the database abstract layer so that sql queries are not in the code

    # series_service is a SeriesService
    def __init__(self, taskServer= None):
        #self.series_service = series_service

        self.editLoaded = False
        self.df = None



        if not taskServer:
            # Initialize TaskServer.
            # This class starts the processes before starting wxpython and is needed
            numproc = cpu_count()
            self.taskserver = TaskServerMP(numproc=numproc)
        else:
            self.taskserver= taskServer

    def set_series_service(self, service):

        self.series_service = service
        self.mem_service = SeriesService("sqlite:///:memory:")

    ##############
    # DB Queries
    ##############

    def getDataValuesDF(self):
        logging.debug("update in memory dataframe")
        self.updateDF()
        #pick up thread here before it is needed
        logging.debug("done updating memory dataframe")
        return self.df

    def getDataValues(self):
        return self.mem_service.get_all_values_list()
    
    def getEditRowCount(self):
        return len(self.df)

    def getEditColumns(self):
        return [(x,i) for (i,x) in enumerate(self.df.columns)]

    def getDataValuesforGraph(self, seriesID, noDataValue, startDate=None, endDate=None):
        self.mem_service.get_plot_values(seriesID, noDataValue, startDate, endDate)

    def getEditDataValuesforGraph(self):
        return self.mem_service.get_all_plot_values()

    def commit(self):
        self.mem_service._session_factory.engine.connect().commit()

    def rollback(self):
        self.conn.rollback()

    def stopEdit(self):
        self.editLoaded= False
        query = "DROP TABLE DataValues"
        self.mem_service._session_factory.engine.connect().execute(query)
        self.commit()

    def setConnection(self, service):
        self.mem_service= service

    #TODO Thread this function
    def updateDF(self):
        self.df = self.mem_service.get_all_values_df()

    def initEditValues(self, seriesID):
        """
        :param df: dataframe
        :return: nothing
        """
        if not self.editLoaded:
            logger.debug("Load series from db")

            self.df = self.series_service.get_values_by_series(seriesID)
            self.editLoaded = True

            '''
            if taskserver:
                taskserver.setTasks([("InitEditValues", (self.mem_service._session_factory.engine, self.df))])
                taskserver.processTasks()
            # results = self.taskserver.getCompletedTasks()
            # self.conn = results["InitEditValues"]
            else:
            '''#TODO: Thread this call
            logger.debug("Load series from db")
            self.df.to_sql(name="DataValues", con=self.mem_service._session_factory.engine, flavor='sqlite', index = False, chunksize = 10000)
            logger.debug("done loading database")



