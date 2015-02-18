

import timeit
import logging
from odmtools.common.logger import LoggerTool
from odmtools.odmservices import SeriesService
from odmtools.odmdata import DataValue
from sqlalchemy import update
from odmtools.common.taskServer import TaskServerMP
from multiprocessing import cpu_count, freeze_support

tool = LoggerTool()
logger = tool.setupLogger(__name__, __name__ + '.log', 'w', logging.DEBUG)
class MemoryDatabase(object):
### this code should be changed to work with the database abstract layer so that sql queries are not in the code

    # series_service is a SeriesService
    def __init__(self, taskserver=None ):

        self.editLoaded = False
        self.df = None

        # Initialize TaskServer.
        # This class starts the processes before starting wxpython and is needed

        # TODO clean up closing of program
        #if taskserver is None:
            #numproc = cpu_count()
            #self.taskserver = TaskServerMP(numproc=numproc)
        #else:

        self.taskserver = taskserver

    def set_series_service(self, service):
        self.series_service = service
        self.mem_service = SeriesService("sqlite:///:memory:")

    ##############
    # DB Queries
    ##############

    def getDataValuesDF(self):
        logging.debug("update in memory dataframe")

        '''
        if self.taskserver:
            results = self.taskserver.getCompletedTasks()
            df=results['UpdateEditDF']
        #else:
        #    self.updateDF()
        '''
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
        return self.series_service.get_plot_values(seriesID, noDataValue, startDate, endDate)

    def getEditDataValuesforGraph(self):
        return self.mem_service.get_all_plot_values()

    def commit(self):
        self.mem_service._edit_session.commit()

    def rollback(self):
        self.mem_service._edit_session.rollback()
        #self.updateDF()

    def update(self, ids, values):
        self.mem_service._edit_session.query(DataValue).filter(DataValue.id.in_(ids)).update({DataValue.data_value: -9999999}, False)
        #self.updateDF()

    def updateValue(self, ids, operator, value):
        #query = DataValue.data_value+value
        if operator == '+':
            query = DataValue.data_value+value
        if operator == '-':
            query = DataValue.data_value-value
        if operator == '*':
            query = DataValue.data_value*value
        if operator == '=':
            query = value

        self.mem_service._edit_session.query(DataValue).filter(DataValue.id.in_(ids))\
            .update({DataValue.data_value: query}, False)
        #self.updateDF()


    def delete(self, ids):
        self.mem_service._edit_session.query(DataValue).filter(DataValue.id.in_(ids)).delete()
        #self.updateDF()

    def stopEdit(self):
        self.editLoaded= False
        self.df = None


    def setConnection(self, service):
        self.mem_service= service

    #TODO Thread this function
    def updateDF(self):
        '''
        if self.taskserver:
            # Give tasks to the taskserver to run parallelly
            logger.debug("Sending tasks to taskserver")
            self.taskserver.setTasks(("UpdateEditDF", self.mem_service))
            self.taskserver.processTasks()
        else:
        '''
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
            self.df.to_sql(name="DataValues", if_exists='replace', con=self.mem_service._session_factory.engine,
                           flavor='sqlite', index=False, chunksize=10000)
            logger.debug("done loading database")



