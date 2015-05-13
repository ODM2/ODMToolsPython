import timeit
import logging
from odmtools.common.logger import LoggerTool
from odmtools.odmservices import SeriesService
from odmtools.odmdata import DataValue
from sqlalchemy import update, bindparam
from odmtools.common.taskServer import TaskServerMP
from multiprocessing import cpu_count, freeze_support

tool = LoggerTool()
logger = tool.setupLogger(__name__, __name__ + '.log', 'w', logging.DEBUG)


class MemoryDatabase(object):
    ### this code should be changed to work with the database abstract layer so that sql queries are not in the code

    # series_service is a SeriesService
    def __init__(self, taskserver=None):

        self.editLoaded = False
        self.df = None
        # Series_Service handles remote database
        self.series_service = None
        # Memory_service handles in memory database
        self.mem_service = SeriesService("sqlite:///:memory:")
        # TODO clean up closing of program
        # if taskserver is None:
        #numproc = cpu_count()
        #self.taskserver = TaskServerMP(numproc=numproc)
        #else:

        self.taskserver = taskserver

    def reset_edit(self):
        self.mem_service = SeriesService("sqlite:///:memory:")

    def set_series_service(self, service):
        self.series_service = service


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
        # pick up thread here before it is needed
        logging.debug("done updating memory dataframe")
        return self.df

    def getDataValues(self):
        return self.mem_service.get_all_values()

    def getEditRowCount(self):
        return len(self.df)

    def getEditColumns(self):
        columns = []
        tmp_columns = self.df.columns.tolist()
        tmp_columns.remove('DataValue')
        tmp_columns.remove('LocalDateTime')
        tmp_columns.remove('QualifierID')
        columns.append('DataValue')
        columns.append('LocalDateTime')
        columns.append('QualifierID')
        columns.extend(tmp_columns)
        return [(x, i) for (i, x) in enumerate(columns)]
        # return [(x, i) for (i, x) in enumerate(self.df.columns)]

    def getDataValuesforGraph(self, seriesID, noDataValue, startDate=None, endDate=None):
        return self.series_service.get_plot_values(seriesID, noDataValue, startDate, endDate)

    def getEditDataValuesforGraph(self):
        return self.mem_service.get_all_plot_values()

    def commit(self):
        self.mem_service._edit_session.commit()

    def rollback(self):
        self.mem_service._edit_session.rollback()
        # self.mem_service._session_factory.engine.connect().connection.rollback()
        #self.updateDF()

    def update(self, updates):

        stmt = (DataValue.__table__.update().
                where(DataValue.id == bindparam('id')).
                values(DataValue=bindparam('value'))
        )

        self.mem_service._edit_session.execute(stmt, updates)

        # self.updateDF()


    def updateValue(self, ids, operator, value):
        # query = DataValue.data_value+value
        if operator == '+':
            query = DataValue.data_value + value
        elif operator == '-':
            query = DataValue.data_value - value
        elif operator == '*':
            query = DataValue.data_value * value
        elif operator == '=':
            query = value


        #break into chunks to get around sqlites restriction. allowing user to send in only 999 arguments at once
        chunks=self.chunking(ids)
        for c in chunks:
            q=self.mem_service._edit_session.query(DataValue).filter(DataValue.id.in_(c))
            q.update({DataValue.data_value: query}, False)

        #self.updateDF()

    def chunking(self, data):
        return [data[x:x+998] for x in xrange(0, len(data), 998)]
        
    #break into chunks to get around sqlites restriction. allowing user to send in only 999 arguments at once
    def updateFlag(self, ids, value):
        chunks=self.chunking(ids)
        for c in chunks:
            self.mem_service._edit_session.query(DataValue).filter(DataValue.id.in_(c))\
                .update({DataValue.qualifier_id: value}, False)


    def delete(self, ids):
        chunks=self.chunking(ids)
        for c in chunks:
            self.mem_service.delete_dvs(c)
        #self.updateDF()


    def addPoints(self, points):
        """
        Takes in a list of points and loads each point into the database
        """
        stmt = DataValue.__table__.insert()

        if not isinstance(points, list):
            points = [points]

        for point in points:
            vals = {"DataValue": point[0], "ValueAccuracy": point[1],
                    "LocalDateTime": point[2], "UTCOffset": point[3],
                    "DateTimeUTC": point[4], "OffsetValue": point[5],
                    "OffsetTypeID": point[6], "CensorCode": point[7],
                    "QualifierID": point[8], "SampleID": point[9],
                    "SiteID": point[10], "VariableID": point[11],
                    "MethodID": point[12], "SourceID": point[13],
                    "QualityControlLevelID": point[14]}
            self.mem_service._edit_session.execute(stmt, vals)


    def stopEdit(self):
        self.editLoaded = False
        self.df = None


    def setConnection(self, service):
        self.mem_service = service


    # TODO multiprocess this function
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
            if self.taskserver:
                self.taskserver.setTasks([("InitEditValues", (self.mem_service._session_factory.engine, self.df))])
                self.taskserver.processTasks()
            # results = self.taskserver.getCompletedTasks()
            # self.conn = results["InitEditValues"]
            else:
            '''  #TODO: Thread this call
            if len(self.df)>0:
                self.df.to_sql(name="DataValues", if_exists='replace', con=self.mem_service._session_factory.engine,
                               index=False)#,flavor='sqlite', chunksize=10000)
                logger.debug("done loading database")
            else:
                logger.debug("no data in series")

    def changeSeriesIDs(self, var=None, qcl=None, method=None):
        """

        :param var:
        :param qcl:
        :param method:
        :return:
        """

        query = self.mem_service._edit_session.query(DataValue)
        if var is not None:
            logger.debug(var)
            query.update({DataValue.variable_id: var})

        if method is not None:
            logger.debug(method)
            query.update({DataValue.method_id: method})
        # check that the code is not zero
        # if qcl is not None and qcl.code != 0:
        if qcl is not None:
            logger.debug(qcl)
            query.update({DataValue.quality_control_level_id: qcl})

