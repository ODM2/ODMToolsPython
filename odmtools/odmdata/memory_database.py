

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
    def __init__(self, taskserver=None ):

        self.editLoaded = False
        self.df = None

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
        return self.mem_service.get_all_values()
    
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
        #self.mem_service._session_factory.engine.connect().connection.rollback()
        #self.updateDF()

    def update(self, updates):

        stmt = (DataValue.__table__.update().
            where(DataValue.id == bindparam('id')).
            values(DataValue=bindparam('value'))
        )

        self.mem_service._edit_session.execute(stmt, updates)

        # self.updateDF()


    def updateValue(self, ids, operator, value):
        #query = DataValue.data_value+value
        if operator == '+':
            query = DataValue.data_value+value
        elif operator == '-':
            query = DataValue.data_value-value
        elif operator == '*':
            query = DataValue.data_value*value
        elif operator == '=':
            query = value

        q=self.mem_service._edit_session.query(DataValue).filter(DataValue.id.in_(ids))
        q.update({DataValue.data_value: query}, False)
        #self.updateDF()

    def updateFlag(self, ids, value):
        self.mem_service._edit_session.query(DataValue).filter(DataValue.id.in_(ids))\
            .update({DataValue.qualifier_id: value}, False)


    def delete(self, ids):
        self.mem_service.delete_dvs(ids)
        #self.updateDF()

    def addPoints(self, points):
        stmt = DataValue.__table__.insert()

        vals= {"DataValue": points[0][0], "ValueAccuracy":points[0][1], "LocalDateTime":points[0][2], "UTCOffset":points[0][3],
               "DateTimeUTC:":points[0][4], "OffsetValue":points[0][5], "OffsetTypeID":points[0][6],"CensorCode":points[0][7],
               "QualifierID":points[0][8], "SampleID":points[0][9], "SiteID":points[0][10], "VariableID":points[0][11],
               "MethodID":points[0][12], "SourceID":points[0][13], "QualityControlLevelID":points[0][14]}
        self.mem_service._edit_session.execute(stmt, vals)


    def stopEdit(self):
        self.editLoaded = False
        self.df = None


    def setConnection(self, service):
        self.mem_service= service

    #TODO multiprocess this function
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
            '''#TODO: Thread this call
            logger.debug("Load series from db")
            self.df.to_sql(name="DataValues", if_exists='replace', con=self.mem_service._session_factory.engine,
                           flavor='sqlite', index=False)#, chunksize=10000)
            logger.debug("done loading database")



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

    '''
    def updateSeries(self, var=None, method=None, qcl=None, is_new_series=False):
        """

        :param var:
        :param method:
        :param qcl:
        :param is_new_series:
        :return:
        """
        dvs = []

        ''
        if var is not None:
            logger.debug(var.id)
            self._cursor.execute("UPDATE DataValues SET VariableID = %s" % (var.id))

        if method is not None:
            logger.debug(method.id)
            self._cursor.execute("UPDATE DataValues SET MethodID = %s" % (method.id))
        # check that the code is not zero
        # if qcl is not None and qcl.code != 0:
        if qcl is not None:
            self._cursor.execute("UPDATE DataValues SET QualityControlLevelID = %s" % (qcl.id))
        # else:
        #    raise ValueError("Quality Control Level cannot be zero")


        self._cursor.execute("SELECT * FROM DataValues ORDER BY LocalDateTime")
        results = self._cursor.fetchall()
        ''

        self.memDb.newSeries(var, method, qcl)
        results = self.memDB.getDataValues

        # ValueID, DataValue, ValueAccuracy, LocalDateTime, UTCOffset, DateTimeUTC, SiteID, VariableID,
        # OffsetValue, OffsetTypeID, CensorCode, QualifierID, MethodID, SourceID, SampleID, DerivedFromID, QualityControlLevelID
        for row in results:
            dv = self._build_dv_from_tuple(row)

            if is_new_series:
                dv.id = None
            dvs.append(dv)

        series = self._series_service.get_series_by_id(self._series_id)
        logger.debug("original editing series id: %s" % str(series.id))
        #        testseries = self._series_service.get_series_by_id_quint(series.site_id, var if var else series.var_id
        #                                                             , method if method else series.method_id, series.source_id
        #                                                             , qcl if qcl else series.qcl_id)
        #        print "test query series id:",testseries.id
        #print a if b else 0
        if (var or method or qcl ):
            tseries = self._series_service.get_series_by_id_quint(site_id=int(series.site_id),
                                                                  var_id=var.id if var else int(series.variable_id),
                                                                  method_id=method.id if method else int(
                                                                      series.method_id),
                                                                  source_id=series.source_id,
                                                                  qcl_id=qcl.id if qcl else int(
                                                                      series.quality_control_level_id))
            if tseries:
                logger.debug("Save existing series ID: %s" % str(series.id))
                series = tseries
            else:
                print "Series doesn't exist (if you are not, you should be running SaveAs)"

        if is_new_series:
            series = series_module.copy_series(series)
            if var:
                series.variable_id = var.id
                series.variable_code = var.code
                series.variable_name = var.name
                series.speciation = var.speciation
                series.variable_units_id = var.variable_unit.id
                series.variable_units_name = var.variable_unit.name
                series.sample_medium = var.sample_medium
                series.value_type = var.value_type
                series.time_support = var.time_support
                series.time_units_id = var.time_unit.id
                series.time_units_name = var.time_unit.name
                series.data_type = var.data_type
                series.general_category = var.general_category
            if method:
                series.method_id = method.id
                series.method_description = method.description
            if qcl:
                series.quality_control_level_id = qcl.id
                series.quality_control_level_code = qcl.code

        series.begin_date_time = dvs[0].local_date_time
        series.end_date_time = dvs[-1].local_date_time
        series.begin_date_time_utc = dvs[0].date_time_utc
        series.end_date_time_utc = dvs[-1].date_time_utc
        series.value_count = len(dvs)

        ## Override previous save
        if not is_new_series:
            # delete old dvs
            self._series_service.delete_values_by_series(series)

        series.data_values = dvs
        #logger.debug("series.data_values: %s" % ([x for x in series.data_values]))

        return series
    '''





