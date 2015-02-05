
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
    def __init__(self, taskserver = None ):

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
        self.updateDF()
        #pick up thread here before it is needed
        logging.debug("done updating memory dataframe")
        return self.df

    def getDataValues(self):
        # query = "SELECT ValueID, SeriesID, DataValue, ValueAccuracy, LocalDateTime, UTCOffset, DateTimeUTC, QualifierCode, OffsetValue, OffsetTypeID, CensorCode, SampleID FROM DataValues AS d LEFT JOIN Qualifiers AS q ON (d.QualifierID = q.QualifierID) "
        '''
        query = "SELECT * from DataValues ORDER BY LocalDateTime"
        self.cursor.execute(query)
        return [list(x) for x in self.cursor.fetchall()]
        '''
        return self.mem_service.get_all_values_list()

    
    def getEditRowCount(self):
        '''
        query ="SELECT COUNT(ValueID) FROM DataValues "
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]
        '''
        return len(self.df)


    def getEditColumns(self):
        '''
        sql = "SELECT * FROM DataValues WHERE 1=0 "
        self.cursor.execute(sql)
        return [(x[0],i) for (i,x) in enumerate(self.cursor.description)]
        '''
        return [(x,i) for (i,x) in enumerate(self.df.columns)]

    def getDataValuesforGraph(self, seriesID, noDataValue, startDate=None, endDate=None):
        '''
        series = self.series_service.get_series_by_id(seriesID)
        DataValues = [
            (dv.data_value, dv.local_date_time, dv.censor_code, dv.local_date_time.strftime('%m'),
                dv.local_date_time.strftime('%Y'))
            for dv in series.data_values
            if dv.data_value != noDataValue if dv.local_date_time >= startDate if dv.local_date_time <= endDate
        ]
        data = pd.DataFrame(DataValues, columns=self.columns)
        data.set_index(data['LocalDateTime'], inplace=True)
        return data
        '''
        self.mem_service.get_plot_values(seriesID, noDataValue, startDate, endDate)

    def getEditDataValuesforGraph(self):
        '''
        query ="SELECT DataValue, LocalDateTime, CensorCode, strftime('%m', LocalDateTime) as Month, " \
               "strftime('%Y', LocalDateTime) as Year  FROM DataValues ORDER BY LocalDateTime"


        start=timeit.default_timer()
        DataValues = [
            (dv.data_value, dv.local_date_time, dv.censor_code, dv.local_date_time.strftime('%m'),
                dv.local_date_time.strftime('%Y'))
            for dv in series.data_values

        ]
        data= pd.DataFrame(self.cursor.fetchall(), columns=[x[0]for x in self.cursor.description])
        elapsed = timeit.default_timer()- start
        logger.debug("load fetchall into dataframe: %s"% elapsed)

        start=timeit.default_timer()
        df2= pd.read_sql_query(query, self.conn)
        elapsed = timeit.default_timer()- start
        logger.debug("load read_sql_query into dataframe: %s"% elapsed)
        data.set_index(data['LocalDateTime'], inplace=True)
        return  data
        '''
        return self.mem_service.get_all_plot_values()

    def commit(self):
        self.mem_service._session_factory.engine.connect().connection.commit()

    def rollback(self):
        self.conn.rollback()

    def stopEdit(self):
        self.editLoaded= False
        query = " DROP TABLE DataValues"
        #self.cursor.execute("DROP TABLE DataValues")
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



