import logging
from sqlalchemy import not_, bindparam, distinct, func, exists
from odm2api.ODM2.services import ReadODM2,  UpdateODM2, DeleteODM2, CreateODM2
from odm2api import serviceBase
from odm2api.ODM2.models import *
from odmtools.odmservices.to_sql_newrows import clean_df_db_dups, delete, update
import datetime
from odmtools.common.logger import LoggerTool
import pandas as pd
logger =logging.getLogger('main')


class SeriesService(serviceBase):
    # Accepts a string for creating a SessionFactory, default uses odmdata/connection.cfg
    def __init__(self, connection, debug=False):

        serviceBase.__init__(self, connection, debug)
        self.read = ReadODM2(self._session_factory)
        self.update = UpdateODM2(self._session_factory)
        self.delete = DeleteODM2(self._session_factory)
        self.create = CreateODM2(self._session_factory)
        #send in engine
        setSchema(self._session_factory.engine)


    def reset_session(self):
        self.read.reset_session()
        self.update.reset_session()
        self.delete.reset_session()
        self.create.reset_session()

#####################
#
#  Get functions
#
#####################

    def get_used_sites(self):
        """
        Return a list of all sites that are being referenced in the Series Catalog Table
        :return: List[Sites]
        """
        try:
            fas=[x[0] for x in self._session.query(distinct(Results.FeatureActionID)).all()]
        except:
            return None

        sf=[x[0] for x in self._session.query(distinct(FeatureActions.SamplingFeatureID)).filter(FeatureActions.FeatureActionID.in_(fas)).all()]

        sites = self.read.getSamplingFeatures(type = "site", ids = sf)
        return sites

    def get_used_variables(self):
        """
        #get list of used variable ids
        :return: List[Variables]
        """
        try:
            ids= [x[0] for x in self._session.query(distinct(Results.VariableID)).all()]
        except:
            return None

        vars= self.read.getVariables(ids = ids)
        return vars



    # Query DetailedResultInfo/series object is for Display purposes
    def get_all_series(self, siteid = None):
        """
        Returns all series as a modelObject
        :return: List[Series]
        """

        setSchema(self._session_factory.engine)


        return self.read.getDetailedResultInfo('Time Series Coverage', sfID=siteid)

    def get_series(self, series_id=None):
        """
        :param series_id: int
        :return: Series
        """
        # try:
        #     return self.read.getDetailedResultInfo('Time Series Coverage', resultID = series_id)[0]
        # except Exception as e:
        #     print e
        #     return None
        setSchema(self._session_factory.engine)
        return self.read.getResults(ids=[series_id])[0]

    # Query result objects for data purposes
    def get_result_dates(self, result_id):
        q = self.read._session.query(
            func.max(TimeSeriesResultValues.ValueDateTime), func.min(TimeSeriesResultValues.ValueDateTime)
            ).filter(TimeSeriesResultValues.ResultID == result_id)
        return q.all()[0]

    def get_variables_by_site_code(self, site_code):
        """
            Finds all of variables at a site
            :param site_code: str
            :return: List[Variables]
        """
        try:
            var_ids = [x[0] for x in
                       self._session.query(distinct(Results.VariableID))
                       .filter(Results.FeatureActionID == FeatureActions.FeatureActionID)
                       .filter(FeatureActions.SamplingFeatureID == SamplingFeatures.SamplingFeatureID)
                       .filter(SamplingFeatures.SamplingFeatureCode == site_code).all()
            ]
        except:
            var_ids = None

        q = self._session.query(Variables).filter(Variables.VariableID.in_(var_ids))
        return q.all()

        # Data Value Methods
    def get_values(self, series_id=None):
        '''

        :param series_id:  Series id
        :return: pandas dataframe
        '''

        setSchema(self._session_factory.engine)
        q = self.read._session.query(TimeSeriesResultValues)
        if series_id:
            q = q.filter_by(ResultID=series_id)
        q = q.order_by(TimeSeriesResultValues.ValueDateTime)
        query = q.statement.compile(dialect=self._session_factory.engine.dialect)
        data = pd.read_sql_query(sql=query,
                                 con=self._session_factory.engine,
                                 params=query.params)
        data.set_index(data['valuedatetime'], inplace=True)
        return data

# Series Catalog methods
    def get_series_by_site(self , site_id):
        # try:
        #     selectedSeries = self._edit_session.query(Series).filter_by(site_id=site_id).order_by(Series.id).all()
        #     return selectedSeries
        # except:
        #     return None
        """
        :param site_id: type(Int)
        :return: list[Series]
        """

        # return self.read.getResults(type="timeSeries", ids=[site_id])
        # return self.read.getResults(type="site", ids= [site_id])[0]
        return self.read.getResults(ids=[site_id])



    # Site methods
    def get_all_sites(self):
        """
        :return: List[Sites]
        """
        #return self._edit_session.query(Site).order_by(Site.code).all()
        return self.read.getResults(type="site")


    def get_site_by_id(self, site_id):
        """
        return a Site object that has an id=site_id
        :param site_id: integer- the identification number of the site
        :return: Sites
        """
#         try:
#             return self._edit_session.query(Site).filter_by(id=site_id).first()
#         except:
#             return None

        return self.read.getSampling(ids = [site_id])[0]


    def get_all_variables(self):
        """
        :return: List[Variables]
        """
        #return self._edit_session.query(Variable).all()
        return self.read.getVariables()

    def get_variable_by_id(self, variable_id):
        """
        :param variable_id: int
        :return: Variables
        """
#         try:
#             return self._edit_session.query(Variable).filter_by(id=variable_id).first()
#         except:
#             return None
        return self.read.getVariables(ids = [variable_id])[0]
#
    def get_variable_by_code(self, variable_code):
        """

        :param variable_code:  str
        :return: Variables
        """
        # try:
        #     return self._edit_session.query(Variable).filter_by(code=variable_code).first()
        # except:
        #     return None
        return self.read.getVariables(codes = [variable_code])[0]
#

#
    # Unit methods
    def get_all_units(self):
        """

        :return: List[Units]
        """
        # return self._edit_session.query(Unit).all()
        return self.read.getUnits()
#
    def get_unit_by_name(self, unit_name):
        """
        :param unit_name: str
        :return: Units
        """
        # try:
        #     return self._edit_session.query(Unit).filter_by(name=unit_name).first()
        # except:
        #     return None
        return self.read.getUnits(name=[unit_name])[0]
#
    def get_unit_by_id(self, unit_id):
        """

        :param unit_id: int
        :return: Units
        """
        # try:
        #     return self._edit_session.query(Unit).filter_by(id=unit_id).first()
        # except:
        #     return None
        return self.read.getUnits(ids=[unit_id])[0]

#
    def get_all_qualifiers(self):
        """

        :return: List[Qualifiers]
        """
        # result = self._edit_session.query(Qualifier).order_by(Qualifier.code).all()
        # return result
        ann= self.read.getAnnotations()
        return ann
#
    def get_qualifier_by_code(self, code):
        """

        :return: Qualifiers
        # """
        # result = self._edit_session.query(Qualifier).filter(Qualifier.code==code).first()
        # return result
        return self.read.getAnnotations(codes=[code])[0] ##todo: CHECK ON THIS
#
    def get_qualifiers_by_series_id(self, series_id):
        return self.read.getAnnotations(ids=[series_id])[0] ##todo: check on this

    def get_all_processing_levels(self):
        return self.read.getProcessingLevels(ids=None, codes=None)

#         """
#
#         :param series_id:
#         :return:
#         """
#         subquery = self._edit_session.query(DataValue.qualifier_id).outerjoin(
#             Series.data_values).filter(Series.id == series_id, DataValue.qualifier_id != None).distinct().subquery()
#         return self._edit_session.query(Qualifier).join(subquery).distinct().all()
#


    def get_processing_level_by_id(self, qcl_id):
        try:
            return self.read.getProcessingLevels(ids = [qcl_id])[0]
            #return self._edit_session.query(QualityControlLevel).filter_by(id=qcl_id).first()
        except:
            return None
#
    def get_processing_level_by_code(self, codes):
        try:
            return self.read.getProcessingLevels(codes=[codes])[0]
        except:
            return None

#     # Method methods
    def get_all_methods(self):
        #return self._edit_session.query(Method).all()
        return self.read.getMethods()
#
    def get_method_by_id(self, method_id):
        return self.read.getMethods(ids=[method_id])[0]
        # try:
        #     result = self._edit_session.query(Method).filter_by(id=method_id).first()
        # except:
        #     result = None
        # return result
#
    def get_method_by_code(self, method_code):
        try:
            return self.read.getMethods(codes=[method_code])[0]
        except:
            return None

        # try:
        #     result = self._edit_session.query(Method).filter_by(description=method_code).first()
        # except:
        #     result = None
        #     logger.error("method not found")
        # return result
#

#todo: Take another look at this


    # Series Catalog methods
    def resultExists(self, result):
        """

        :param site_id:
        :param var_id:
        :param method_id:
        :param source_id:
        :param qcl_id:
        :return: Series
        """
        # unique Result
        # FeatureActionID, ResultTypeCV, VariableID, UnitsID, ProcessingLevelID, SampledMediumCV


        try:
            # return self._edit_session.query(Results).filter_by(
            #      VariableID=var_id, MethodID=method_id,
            #      AnnotationID=qcl_id).first()
            res = self._session.query(exists().where(Results.ResultTypeCV == result.ResultTypeCV).
                                           where(Results.VariableID == result.VariableID).
                                           where(Results.UnitsID == result.UnitsID).
                                           where(Results.ProcessingLevelID == result.ProcessingLevelID).
                                           where(Results.SampledMediumCV == result.SampledMediumCV)
                                      )
        # where(Results.FeatureActionID == result.FeatureActionID).


            return res
        except:
            return None



    def get_series_from_filter(self):
        # Pass in probably a Series object, match it against the database
        pass

#
    #Data Value Methods
    def get_values(self, series_id=None):
        '''
        :param series_id:  Series id
        :return: pandas dataframe
        '''
        #series= self.get_series_by_id(series_id)
        # if series:
        #     q = self._edit_session.query(DataValue).filter_by(
        #             site_id=series.site_id,
        #             variable_id=series.variable_id,
        #             method_id=series.method_id,
        #             source_id=series.source_id,
        #             quality_control_level_id=series.quality_control_level_id)
        #
        #     query=q.statement.compile(dialect=self._session_factory.engine.dialect)
        #     data= pd.read_sql_query(sql= query,
        #                       con = self._session_factory.engine,
        #                       params = query.params )
        #     #return data.set_index(data['LocalDateTime'])
        #     return data
        # else:
        #     return None

        q = self.read._session.query(TimeSeriesResultValues)
        if series_id:
            q=q.filter_by(ResultID=series_id)
        q= q.order_by(TimeSeriesResultValues.ValueDateTime)
        query = q.statement.compile(dialect=self._session_factory.engine.dialect)
        data = pd.read_sql_query(sql=query,
                                 con=self._session_factory.engine,
                                 params=query.params)
        data.set_index(data['valuedatetime'], inplace=True)
        return data

    def get_all_values_df(self):

        """

        :return: Pandas DataFrame object
        """
        q = self.read._session.query(TimeSeriesResultValues).order_by(TimeSeriesResultValues.ValueDateTime)
        query = q.statement.compile(dialect=self._session_factory.engine.dialect)
        data = pd.read_sql_query(sql=query, con=self._session_factory.engine,
                          params=query.params)
        #columns = list(data)

        # columns.insert(0, columns.pop(columns.index("DataValue")))
        # columns.insert(1, columns.pop(columns.index("ValueDateTime")))
        #columns.insert(2, columns.pop(columns.index("QualifierID")))

        #data = data.ix[:, columns]
        return data.set_index(data['ValueDateTime'])
        # q = self._edit_session.query(TimeSeriesResultValues).order_by(TimeSeriesResultValues.ValueDateTime)
        # query = q.statement.compile(dialect = self._session_factory.engine.dialect)
        # data = pd.read_sql_query(sql= query,
        #                          con= self._session_factory.engine,
        #                          params=query.params)
#


    def get_all_values_list(self):
        """

        :return:
        """
        result =self.read._session.query(TimeSeriesResultValues).order_by(TimeSeriesResultValues.ValueDateTime).all()
        return [x.list_repr() for x in result]

    def get_all_values(self):
        return self.read._session.query(TimeSeriesResultValues).order_by(TimeSeriesResultValues.ValueDateTime).all()
#
    @staticmethod
    def calcSeason(row):

        month = int(row["month"])

        if month in [1, 2, 3]:
            return 1
        elif month in[4, 5, 6]:
            return 2
        elif month in [7, 8, 9]:
            return 3
        elif month in [10, 11, 12]:
            return 4

    def get_plot_values(self, seriesID, noDataValue, startDate=None, endDate=None):
        """
        :param seriesID:
        :param noDataValue:
        :param startDate:
        :param endDate:
        :return:
        """
        setSchema(self._session_factory.engine)
        Values = self.get_values(seriesID)
        data = Values[['datavalue', 'censorcodecv', 'valuedatetime']]
        # data = data[data['datavalue'] != noDataValue]
        data = data[(data['datavalue'] != noDataValue) & (data['valuedatetime'] >= startDate) & (
            data['valuedatetime'] <= endDate)]

        data["month"] = data['valuedatetime'].apply(lambda x: x.month)
        data["year"] = data['valuedatetime'].apply(lambda x: x.year)
        data["season"] = data.apply(self.calcSeason, axis=1)
        # data.set_index(data['valuedatetime'], inplace=True)
        return data

    def get_all_plot_values(self):
        setSchema(self._session_factory.engine)
        Values = self.get_values()
        data = Values[['datavalue', 'censorcodecv', 'valuedatetime']]
        # data = data[data['datavalue'] != noDataValue]


        data["month"] = data['valuedatetime'].apply(lambda x: x.month)
        data["year"] = data['valuedatetime'].apply(lambda x: x.year)
        data["season"] = data.apply(self.calcSeason, axis=1)
        #data.set_index(data['valuedatetime'], inplace=True)
        return data






#     def get_data_value_by_id(self, id):
#         """
#
#         :param id:
#         :return:
#         """
#         try:
#             return self._edit_session.query(DataValue).filter_by(id=id).first()
#         except:
#             return None
#
#
#

#####################
#
#  Update functions
#
#####################
#     def update_series(self, series):
#         """
#
#         :param series:
#         :return:
#         """
#         merged_series = self._edit_session.merge(series)
#         self._edit_session.add(merged_series)
#         self._edit_session.commit()
#
#     def update_dvs(self, dv_list):
#         """
#
#         :param dv_list:
#         :return:
#         """
#         merged_dv_list = map(self._edit_session.merge, dv_list)
#         self._edit_session.add_all(merged_dv_list)
#         self._edit_session.commit()
#

#####################
#
#  Create functions
#
#####################



#new series
    def createResult(self, var, meth, proc):
        #also create an action
        #copy old
        #change var, meth proc, in df #intend ts, agg stat
        # Result = None
        # result = Results()
        result = Results()

        if isinstance(var, Variables):
            result.VariableID = var.VariableID
            result.VariableObj = var

        if isinstance(meth, Methods):
            # do something with meth
            pass

        if isinstance(proc, ProcessingLevels):
            result.ProcessingLevelID = proc.ProcessingLevelID
            result.ProcessingLevelObj = proc

        time, offset = self.get_current_time_and_utcoffset()
        result.ResultDateTime = time
        result.ResultDateTimeUTCOffset = offset

        return self.create.createResult(result=result)



    def get_current_time_and_utcoffset(self):
        current_time = datetime.datetime.now()
        utc_time = datetime.datetime.utcnow()

        difference_in_timezone = current_time - utc_time
        offset_in_hours = difference_in_timezone.total_seconds() / 3600

        return current_time, offset_in_hours





#     def save_series(self, series, dvs):
#         """ Save to an Existing Series
#         :param series:
#         :param data_values:
#         :return:
#         """
#
#         if self.series_exists(series):
#
#             try:
#                 self._edit_session.add(series)
#                 self._edit_session.commit()
#                 self.save_values(dvs)
#             except Exception as e:
#                 self._edit_session.rollback()
#                 raise e
#             logger.info("Existing File was overwritten with new information")
#             return True
#         else:
#             logger.debug("There wasn't an existing file to overwrite, please select 'Save As' first")
#             # there wasn't an existing file to overwrite
#             raise Exception("Series does not exist, unable to save. Please select 'Save As'")
#
#
    # def save_new_series(self, series, dvs):
    #     """ Create as a new catalog entry
    #     :param series:
    #     :param data_values:
    #     :return:
    #     """
    #     # Save As case
    #     if self.series_exists(series):
    #         msg = "There is already an existing file with this information. Please select 'Save' or 'Save Existing' to overwrite"
    #         logger.info(msg)
    #         raise Exception(msg)
    #     else:
    #         try:
    #             self._edit_session.add(series)
    #             self._edit_session.commit()
    #             self.save_values(dvs)
    #             #self._edit_session.add_all(dvs)
    #         except Exception as e:
    #             self._edit_session.rollback()
    #             raise e
    #
    #     logger.info("A new series was added to the database, series id: "+str(series.id))
    #     return True


    def update_values(self, updates):
        '''
        updates : time series result values, pandas dataframe
        '''
        setSchema(self.mem_service._session_factory.engine)

        stmt = (TimeSeriesResultValues.__table__.update().
                where(TimeSeriesResultValues.ValueDateTime == bindparam('id')).
                values(datavalue=bindparam('value'))
                )

        self.create._session.execute(stmt, updates["datavalue"].to_dict(orient='dict'))
        #self.mem_service._session.query(TSRV).filter_by

        # self.updateDF()

    def insert_annotations(self, annotations):
        annotations.to_sql(name="timeseriesresultvalueannotations", if_exists='append', con=self._session_factory.engine, index=False)


    def upsert_values(self, values):
        setSchema(self._session_factory.engine)
        newvals= clean_df_db_dups(df = values, dup_cols = ["valuedatetime", "resultid"], tablename="timeseriesresultvalues", engine = self._session_factory.engine,
                                         filter_continuous_col="valuedatetime", filter_categorical_col="resultid")
        self.insert_values(newvals)
        delvals = delete(df = values, dup_cols = ["valuedatetime", "resultid"], tablename="timeseriesresultvalues", engine = self._session_factory.engine,
                        filter_continuous_col = "valuedatetime", filter_categorical_col = "resultid")
        self.delete_dvs(delvals["valuedatetime"])

        upvals = update(df = values,dup_cols = ["valuedatetime", "resultid"], tablename="timeseriesresultvalues", engine = self._session_factory.engine,
                               filter_continuous_col="valuedatetime", filter_categorical_col="resultid")
        self.update(upvals)

    def insert_values(self, values):
        """

        :param values: pandas dataframe
        :return:
        """
        values.to_sql(name="timeseriesresultvalues", if_exists='append', con=self._session_factory.engine, index=False)
#
#     def create_new_series(self, data_values, site_id, variable_id, method_id, source_id, qcl_id):
#         """
#
#         :param data_values:
#         :param site_id:
#         :param variable_id:
#         :param method_id:
#         :param source_id:
#         :param qcl_id:
#         :return:
#         """
#         self.update_dvs(data_values)
#         series = Series()
#         series.site_id = site_id
#         series.variable_id = variable_id
#         series.method_id = method_id
#         series.source_id = source_id
#         series.quality_control_level_id = qcl_id
#
#         self._edit_session.add(series)
#         self._edit_session.commit()
#         return series


    def create_new_series(self, data_values, site_id, variable_id, method_id, source_id, qcl_id):
        # ToDo: create a Result, TimeSeriesResult and an Action object of type derivation
        """
        series_service -> Result in ODM2
        :param data_values:
        :param site_id:
        :param variable_id:
        :param method_id:
        :param source_id:
        :param qcl_id:
        :return:
        """
        self.update_dvs(data_values)
        series = Results()
        series.site_id = site_id
        series.variable_id = variable_id
        series.method_id = method_id
        series.source_id = source_id
        series.quality_control_level_id = qcl_id

        return self.create_service.getResult(series)

    def create_method(self, description, link):
        """
        :param description:
        :param link:
        :return:
        """
        method = Methods()
        method.MethodDescription = description
        if link is not None:
            method.MethodLink = link

        return self.create_service.createMethod(method=method)

    def create_variable(
            self, code, name, speciation,  no_data_value):
        """
        :param code:
        :param name:
        :param speciation:

        :param no_data_value:
        :return:
        """

        variable = Variables()
        variable.VariableCode = code
        variable.VariableNameCV = name
        variable.SpeciationCV = speciation

        variable.NoDataValue = no_data_value

        return self.create.createVariable(var=variable)

    def create_processing_level(self, code, definition, explanation):
        """
        qcl -> Processing Level in ODM2
        :param code:
        :param definition:
        :param explanation:
        :return:
        """
        procLevel = ProcessingLevels()
        procLevel.ProcessingLevelCode = code
        procLevel.Definition = definition
        procLevel.Explanation = explanation
        return self.create.createProcessingLevel(proclevel=procLevel)

    def create_annotation_by_anno(self, annotation):
        return self.create.createAnnotations(annotation)

    def create_annotation(self, code, text, link=None):
        """
        :param code:
        :param text:
        :return:
        """
        annotation = Annotations()
        annotation.AnnotationCode = code
        annotation.AnnotationText = text
        annotation.AnnotationTypeCV = "Time series result value annotation"

        time, offset = self.get_current_time_and_utcoffset()
        annotation.AnnotationDateTime = time
        annotation.AnnotationUTCOffset = offset

        annotation.AnnotationLink = link

        return self.create_annotation_by_anno(annotation)

    def add_annotations(self, anno_list):
        try:
            #tablename = TimeSeriesResultValueAnnotations.__tablename__
            #print ("I am TS saving name the table name", tablename)
            anno_list.to_sql(name="TimeSeriesResultValueAnnotations",
                              schema=TimeSeriesResultValueAnnotations.__table_args__['schema'],
                              if_exists='append',
                              chunksize=1000,
                              con=self._session_factory.engine,
                              index=False)
            self._session.commit()

            return anno_list
        except Exception as e:
            print(e)
            return None


    def get_vertical_datum_cvs(self):
        return self.read.getCVs(type="Elevation Datum")

    def get_samples(self):
        return self.read.getSamplingFeatures(ids=None, codes=None, uuids=None, type=None, wkt=None)

    def get_site_type_cvs(self):
        return self.read.getCVs(type="Site Type")  # OR return self.read.getCVs(type="Sampling Feature Type")

    def get_variable_name_cvs(self):
        return self.read.getCVs(type="Variable Name")

    def get_offset_type_cvs(self):
        return self.read.getCVs(type="Spatial Offset Type")

    def get_speciation_cvs(self):
        return self.read.getCVs(type="Speciation")

    def get_sample_medium_cvs(self):
        return self.read.getCVs(type="Medium")

    def get_value_type_cvs(self):
        return self.read.getCVs(type="Result Type")

    def get_data_type_cvs(self):
        return self.read.getCVs(type="dataset type")

    def get_general_category_cvs(self):
        return self.read.getAnnotations(type="categoricalresultvalue")

    def get_censor_code_cvs(self):
        return self.read.getCVs(type="censorcode")

    # def get_sample_type_cvs(self):
    #     return self.read.getCVs(type="Sampling Feature Type")

    def get_units(self):
        return self.read.getUnits(ids=None, name=None, type=None)

    def get_units_not_uni(self):
        return self._session.query(Units).filter(not_(Units.UnitsName.contains('angstrom'))).all()

    def get_units_names(self):
        return self._session.query(Units.UnitsName).all()

    def get_quality_code(self):
        return self.read.getCVs(type="Quality Code")

    def get_annotation_by_code(self, code):
        return self.read.getAnnotations(codes=[code])[0]

    def get_all_annotations(self):
        return self.read.getAnnotations(type=None)

    def get_annotations_by_result(self, resultid):
        setSchema(self._session_factory.engine)

        # ids = [x[0] for x in self.read._session.query(TimeSeriesResultValues.ValueID)\
        #         .filter(TimeSeriesResultValues.ResultID == resultid).all()]
        # q = self.read._session.query(TimeSeriesResultValueAnnotations)\
        #     .filter(TimeSeriesResultValueAnnotations.ValueID.in_(ids)).all()

        q =self.read._session.query(TimeSeriesResultValueAnnotations.AnnotationID, TimeSeriesResultValueAnnotations.ValueID,
                                    TimeSeriesResultValues.ResultID, TimeSeriesResultValues.ValueDateTime)\
                            .filter(TimeSeriesResultValues.ResultID == resultid)\
                            .filter(TimeSeriesResultValueAnnotations.ValueID == TimeSeriesResultValues.ValueID)

        query = q.statement.compile(dialect=self._session_factory.engine.dialect)
        data = pd.read_sql_query(sql=query, con=self._session_factory.engine,
                             params=query.params)
        return data

    def get_aggregation_statistic(self):
        return self.read.getCVs(type="aggregationstatistic")

    def get_all_affiliations(self):
        return self.read.getAffiliations(ids=None, personfirst=None, personlast=None, orgcode=None)

    #####################
    #
    #  Delete functions
    #
    #####################
    #
    #     def delete_series(self, series):
    #         """
    #
    #         :param series:
    #         :return:
    #         """
    #         try:
    #             self.delete_values_by_series(series)
    #
    #             delete_series = self._edit_session.merge(series)
    #             self._edit_session.delete(delete_series)
    #             self._edit_session.commit()
    #         except Exception as e:
    #             message = "series was not successfully deleted: %s" % e
    #             print message
    #             logger.error(message)
    #             raise e
    #
    #
    def delete_values_by_series(self, series, startdate=None):
        """

        :param series:
        :return:
        """
        # todo stephanie: add startdate stuff
        try:
            self.delete.deleteTSRValues(ids=[series.id])
        except Exception as ex:
            message = "Values were not successfully deleted: %s" % ex
            print message
            logger.error(message)
            raise ex
            #         try:
            #             q= self._edit_session.query(DataValue).filter_by(site_id = series.site_id,
            #                                                                  variable_id = series.variable_id,
            #                                                                  method_id = series.method_id,
            #                                                                  source_id = series.source_id,
            #                                                                  quality_control_level_id = series.quality_control_level_id)
            #             if startdate is not None:
            #                 #start date indicates what day you should start deleting values. the values will delete to the end of the series
            #                 return q.filter(DataValue.local_date_time >= startdate).delete()
            #             else:
            #                 return q.delete()
            #
            #         except Exception as ex:
            #             message = "Values were not successfully deleted: %s" % ex
            #             print message
            #             logger.error(message)
            #             raise ex
            #

    def delete_dvs(self, id_list):
        """

        :param id_list: list of datetimes
        :return:
        """
        setSchema(self._session_factory.engine)
        try:
            self.delete.deleteTSRValues(dates=id_list)
        except Exception as ex:
            message = "Values were not successfully deleted: %s" % ex
            print message
            logger.error(message)
            raise ex
