import logging

from sqlalchemy import bindparam

from odmtools.common.logger import LoggerTool
from odmtools.odmservices import SeriesService
from odmtools.odmservices import ServiceManager, SeriesService

# from odmtools.odmdata import SeriesService#ODM
# ODM = SeriesService.ODM
from odm2api.ODM2.models import TimeSeriesResultValues as TSRV
from odm2api.ODM2.models import setSchema
import pandas as pd


logger =logging.getLogger('main')

class MemoryDatabase(object):
    ### this code should be changed to work with the database abstract layer so that sql queries are not in the code

    # series_service is a SeriesService
    def __init__(self, taskserver=None):

        self.editLoaded = False
        self.df = None
        # Series_Service handles remote database
        self.series_service = None
        self.results_annotations = None

        # Memory_service handles in memory database
        sm = ServiceManager()
        self.mem_service = sm.get_series_service(conn_string="sqlite:///:memory:")

        setSchema(self.mem_service._session_factory.engine)

        # TODO clean up closing of program
        # if taskserver is None:
        #numproc = cpu_count()
        #self.taskserver = TaskServerMP(numproc=numproc)
        #else:

        self.taskserver = taskserver
        self.annotation_list = pd.DataFrame()
        #self.annotation_list = pd.DataFrame() columns =['ResultID', 'ValueDateTime', 'ValueID', 'AnnotationID')
        #send in engine


    def reset_edit(self):
        sm = ServiceManager()
        self.mem_service = sm.get_series_service(conn_string="sqlite:///:memory:")
        setSchema(self.mem_service._session_factory.engine)


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
        # TODO: fix me! this commit location is only temoporarily. should be flushing so that we can restore
        self.mem_service._session.commit()
        setSchema(self.mem_service._session_factory.engine)
        self.updateDF()
        # pick up thread here before it is needed
        logging.debug("done updating memory dataframe")
        return self.df

    def get_annotations(self, query_db_again=False):
        # self.mem_service._session.commit()
        setSchema(self.series_service._session_factory.engine)
        if self.results_annotations is None or query_db_again:
            result_id = self.df.resultid[0]
            annotation = self.series_service.get_annotations_by_result(resultid=result_id)
            self.results_annotations = annotation

        return self.results_annotations

    def getDataValues(self):
        # TODO: fix me! this commit location is only temoporarily. should be flushing so that we can restore
        self.mem_service._session.commit()
        setSchema(self.mem_service._session_factory.engine)
        return self.mem_service.get_all_values()

    def getEditRowCount(self):
        return len(self.df)

    def getEditColumns(self):
        columns = []
        tmp_columns = self.df.columns.tolist()

        columns.extend(tmp_columns)
        return [(x, i) for (i, x) in enumerate(columns)]
        # return [(x, i) for (i, x) in enumerate(self.df.columns)]

    def get_columns_with_annotations(self):
        """
        If results_annotations has not been set then
        :return:
        """

        if self.results_annotations is None or self.df is None:
            print "self.df and self.results_annotations must be a pandas dataframe. Currently they are None"
            return []

        columns = []
        columns.extend(self.df.columns.tolist())

        annotation_columns = self.results_annotations.columns.tolist()
        index = annotation_columns.index("annotationcode")
        annotation_code_column = annotation_columns[index]

        columns.append(annotation_code_column)

        return [(x, i) for (i, x) in enumerate(columns)]

    def getDataValuesforGraph(self, seriesID, noDataValue, startDate=None, endDate=None):
        return self.series_service.get_plot_values(seriesID, noDataValue, startDate, endDate)

    def getEditDataValuesforGraph(self):
        return self.mem_service.get_all_plot_values()

    def commit(self):
        self.mem_service._session.commit()
        # self.mem_service._session.commit()

    def rollback(self):
        self.mem_service._session.rollback()
        # self.mem_service._session_factory.engine.connect().connection.rollback()
        #self.updateDF()

    #TODO is there a way to do a single rollback
    def rollbacksingle(self):
        pass


    def update(self, updates):
        '''
        updates : list of dictionary that contains 2 items, id and value
        '''
        setSchema(self.mem_service._session_factory.engine)
        stmt = (TSRV.__table__.update().
                where(TSRV.ValueDateTime == bindparam('id')).
                values(datavalue=bindparam('value'))
                )

        self.mem_service._session.execute(stmt, updates)
        #self.mem_service._session.query(TSRV).filter_by

        # self.updateDF()


    def updateValue(self, ids, operator, value):
        # query = DataValue.data_value+value
        if operator == '+':
            query = TSRV.DataValue + value
        elif operator == '-':
            query = TSRV.DataValue - value
        elif operator == '*':
            query = TSRV.DataValue * value
        elif operator == '=':
            query = value


        #break into chunks to get around sqlites restriction. allowing user to send in only 999 arguments at once
        chunks=self.chunking(ids)
        setSchema(self.mem_service._session_factory.engine)
        for c in chunks:
            q=self.mem_service._session.query(TSRV).filter(TSRV.ValueDateTime.in_(c))
            q.update({TSRV.DataValue: query}, False)


        #self.updateDF()

    def chunking(self, data):
        if not isinstance(data, list):
            points = [data]
        return [data[x:x+998] for x in xrange(0, len(data), 998)]



    #break into chunks to get around sqlite's restriction. allowing user to send in only 999 arguments at once


    def updateFlag(self, ids, value):


        flags = pd.DataFrame(columns = ['AnnotationID', 'DateTime', 'ResultID', 'ValueID'])
        flags["DateTime"] = ids
        flags["AnnotationID"] = value
        flags["ResultID"] = self.series.ResultID
        flags["ValueID"] = None


        #what if the column already exists
        # chunks=self.chunking(ids)
        # for c in chunks:
        #     # add entry in the Timeseriesresultvalueannotations table
        #     self.mem_service._session.query(TSRV).filter(TSRV.ValueDateTime.in_(c))\
        #         .update({TSRV.qualifier_id: value}, False)

        frames = [self.annotation_list, flags]
        self.annotation_list=pd.concat(frames)
        print self.annotation_list
        #todo: remove duplicates before saving




    def delete(self, ids):
        chunks=self.chunking(ids)
        for c in chunks:
            self.mem_service.delete_dvs(c)
        #self.updateDF()


    def addPoints(self, points):
        """
        Takes in a list of points and loads each point into the database
        """
        stmt = TSRV.__table__.insert()

        if not isinstance(points, list):
            points = [points]

        for point in points:
            vals = {"datavalue": point[0], "valuedatetime": point[1],
                    "valuedatetimeutcoffset": point[3],
                    "censorcodecv": point[4], "qualitycodecv": point[5],
                    "timeaggregationinterval": point[6], "timeaggregationintervalunitsid": point[7],
                    "resultid":self.df["resultid"][0]
                    # todo: Add annotations
                    }
            if point[8] != 'NULL':
                print point[8]
                self.updateFlag([point[1]], [point[8]])

            setSchema(self.mem_service._session_factory.engine)
            self.mem_service._session.execute(stmt, vals)

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
        self.df = self.mem_service.get_values()


    def initEditValues(self, seriesID):
        """
        :param df: dataframe
        :return: nothing
        """
        if not self.editLoaded:

            logger.debug("Load series from db")

            self.series = self.series_service.get_series(seriesID)
            self.df = self.series_service.get_values(series_id=seriesID)

            self.editLoaded = True

            '''
            if self.taskserver:
                self.taskserver.setTasks([("InitEditValues", (self.mem_service._session_factory.engine, self.df))])
                self.taskserver.processTasks()
            # results = self.taskserver.getCompletedTasks()
            # self.conn = results["InitEditValues"]
            else:
            '''  #TODO: Thread this call
            if self.df is not None and len(self.df)<=0:
                logger.debug("no data in series")
            else:
                setSchema(self.mem_service._session_factory.engine)
                self.df.to_sql(name="timeseriesresultvalues", if_exists='replace', con=self.mem_service._session_factory.engine,
                               index=False)#,flavor='sqlite', chunksize=10000)
                logger.debug("done loading database")


