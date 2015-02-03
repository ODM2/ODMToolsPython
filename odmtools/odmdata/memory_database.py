
import sqlite3
import pandas as pd
import timeit
import logging
from odmtools.common.logger import LoggerTool
import odmtools.common.taskServer

tool = LoggerTool()
logger = tool.setupLogger(__name__, __name__ + '.log', 'w', logging.DEBUG)
class MemoryDatabase(object):
### this code should be changed to work with the database abstract layer so that sql queries are not in the code

    # series_service is a SeriesService
    def __init__(self, series_service):
        self.series_service = series_service        
        self.conn = sqlite3.connect(":memory:", detect_types=sqlite3.PARSE_DECLTYPES)
        self.cursor = self.conn.cursor()
        self.editLoaded = False


    ############
    # DB Queries
    ############

    def get_data_values(self):
        return []

    def getDataValuesforEdit(self):  
        # query = "SELECT ValueID, SeriesID, DataValue, ValueAccuracy, LocalDateTime, UTCOffset, DateTimeUTC, QualifierCode, OffsetValue, OffsetTypeID, CensorCode, SampleID FROM DataValues AS d LEFT JOIN Qualifiers AS q ON (d.QualifierID = q.QualifierID) "
        query = "SELECT * from DataValues ORDER BY LocalDateTime"
        self.cursor.execute(query)
        return [list(x) for x in self.cursor.fetchall()]

    
    def getEditRowCount(self):
        query ="SELECT COUNT(ValueID) FROM DataValues "
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]


    def getEditColumns(self):
        sql = "SELECT * FROM DataValues WHERE 1=0 "
        self.cursor.execute(sql)
        return [(x[0],i) for (i,x) in enumerate(self.cursor.description)]

    def getDataValuesforGraph(self, seriesID, noDataValue, startDate=None, endDate=None):

        series = self.series_service.get_series_by_id(seriesID)
        DataValues = [
            (dv.data_value, dv.local_date_time, dv.censor_code, dv.local_date_time.strftime('%m'),
                dv.local_date_time.strftime('%Y') , None)
            for dv in series.data_values
            if dv.data_value != noDataValue if dv.local_date_time >= startDate if dv.local_date_time <= endDate
        ]
        data = pd.DataFrame(DataValues, columns=self.columns)
        data.set_index(data['LocalDateTime'], inplace=True)
        return data



    def getEditDataValuesforGraph(self):
        query ="SELECT DataValue, LocalDateTime, CensorCode, strftime('%m', LocalDateTime) as Month, " \
               "strftime('%Y', LocalDateTime) as Year  FROM DataValues ORDER BY LocalDateTime"


        start=timeit.default_timer()
        self.cursor.execute(query)

        data= pd.DataFrame(self.cursor.fetchall(), columns=[x[0]for x in self.cursor.description])
        elapsed = timeit.default_timer()- start
        logger.debug("load fetchall into dataframe: %s"% elapsed)

        start=timeit.default_timer()
        df2= pd.read_sql_query(query, self.conn)
        elapsed = timeit.default_timer()- start
        logger.debug("load read_sql_query into dataframe: %s"% elapsed)
        data.set_index(data['LocalDateTime'], inplace=True)
        return  data

    def resetDB(self, series_service):
        self.series_service = series_service

        self.conn = sqlite3.connect(":memory:", detect_types=sqlite3.PARSE_DECLTYPES)
        self.cursor = self.conn.cursor()


    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def stopEdit(self):       

        self.editLoaded= False
        self.cursor.execute("DROP TABLE DataValues")
        self.commit()
    def setConnection(self, connection):
        self.conn= connection


    def initEditValues(self, seriesID, taskserver):
        """
        :param df: dataframe
        :return: nothing
        """
        if not self.editLoaded:
            logger.debug("Load series from db")
            series = self.series_service.get_series_by_id(seriesID)
            df = self.series_service.get_values_by_series(series)
            self.editLoaded = True
            taskserver.setTasks([("InitEditValues", (self.conn, df))])
            taskserver.processTasks()
            # results = self.taskserver.getCompletedTasks()
            # self.conn = results["InitEditValues"]



    def initDVTable(df, connection):
        logger.debug("Load series from db")
        df= df.to_sql("DataValues", connection, 'sqlite', chunksize = 10000)
        logger.debug("done loading database")



    '''
    def initEditValues(self, seriesID):
        if not self.editLoaded:
            logger.debug("Load series from db")
            series = self.series_service.get_series_by_id(seriesID)
            logger.debug("Load series into memory db ")
            self.DataValues = [(dv.id, dv.data_value, dv.value_accuracy, dv.local_date_time, dv.utc_offset, dv.date_time_utc,
                dv.site_id, dv.variable_id, dv.offset_value, dv.offset_type_id, dv.censor_code,
                dv.qualifier_id, dv.method_id, dv.source_id, dv.sample_id, dv.derived_from_id,
                dv.quality_control_level_id) for dv in series.data_values]

            self.cursor.executemany("INSERT INTO DataValues VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", self.DataValues)
            self.commit()
            logger.debug("done loading")
            self.editLoaded = True



    def createEditTable(self):
        self.cursor.execute("""CREATE TABLE DataValues
                (ValueID INTEGER NOT NULL,
                DataValue FLOAT NOT NULL,
                ValueAccuracy FLOAT,
                LocalDateTime TIMESTAMP NOT NULL,
                UTCOffset FLOAT NOT NULL,
                DateTimeUTC TIMESTAMP NOT NULL,
                SiteID INTEGER NOT NULL,
                VariableID INTEGER NOT NULL,
                OffsetValue FLOAT,
                OffsetTypeID INTEGER,
                CensorCode VARCHAR(50) NOT NULL,
                QualifierID INTEGER,
                MethodID INTEGER NOT NULL,
                SourceID INTEGER NOT NULL,
                SampleID INTEGER,
                DerivedFromID INTEGER,
                QualityControlLevelID INTEGER NOT NULL,

                PRIMARY KEY (ValueID),
                UNIQUE (DataValue, LocalDateTime, SiteID, VariableID, MethodID, SourceID, QualityControlLevelID, SampleID))
               """)
            '''