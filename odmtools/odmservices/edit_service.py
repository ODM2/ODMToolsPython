import sqlite3


# from odmtools.odmdata import DataValue
from series_service import SeriesService

# from odmtools.odmdata import series as series_module

import pandas as pd
import datetime
import numpy as np
from odm2api.ODM2.models import *

import logging
from odmtools.common.logger import LoggerTool

# tool = LoggerTool()
# logger = tool.setupLogger(__name__, __name__ + '.log', 'w', logging.DEBUG)
logger =logging.getLogger('main')

class time(object):
    time_units = {
        'second': 's',
        'minute': 'm',
        'hour': 'h',
        'day': 'D',
        'week': 'W',
        'month': 'M',
        'year': 'Y'
    }

    def __init__(self, value, time_period):
        self.value = value
        self.time_period = time_period

class EditService():
    # Mutual exclusion: cursor, or connection_string
    def __init__(self, series_id, connection=None, connection_string="", debug=False):
        '''

        :param series_id:
        :param connection: memory database,  contains connection to remote database
        :param connection_string: connection to remote database
        :param debug:
        :return:
        '''

        self._series_id = series_id
        self._filter_from_selection = False
        self._debug = debug

        if connection_string is "" and connection is not None:
            self.memDB = connection

        elif connection_string is not "" and connection is None:
            from odmtools.odmdata import MemoryDatabase
            self.memDB = MemoryDatabase()
            # todo Stephanie: does not accept a string for the connection anymore
            self.memDB.set_series_service(SeriesService(connection_string, False))


        else:
            logger.error("must send in either a remote db connection string or a memory database object")

        logger.debug("Initializing Memory Database")
        self.memDB.initEditValues(series_id)
        logger.debug("Finished Initializing Memory Database")
        self._populate_series()
        self.reset_filter()

    def get_series_service(self):
        return self.memDB.series_service

    def _populate_series(self):
        # [(ID, value, datetime), ...]
        #self._cursor.execute("SELECT ValueID, DataValue, LocalDateTime FROM DataValues ORDER BY LocalDateTime")

        self._series_points_df = self.memDB.getDataValuesDF()


    def _test_filter_previous(self):

        '''
        if not self._filter_from_selection:
            self.reset_filter()
        '''

        df = None

        if not self._filter_from_selection:
            df = self._series_points_df
        else:
            df = self.filtered_dataframe

        # Ensure that we're not working with an empty dataframe

        if isinstance(df, pd.DataFrame):
            if df.empty:
                return self._series_points_df
        else:
            if not df:
                return self._series_points_df

        return df


    def datetime2dataframe(self, datetime_list):
        """ Converts datetime_list to a pandas Dataframe


        :param datetime_list:
        :return Pandas.DataFrame:
        """

        result = None

        if isinstance(datetime_list, list):

            result = pd.DataFrame(datetime_list, columns=["valuedatetime"])

            result.set_index("valuedatetime", inplace=True)

        return result

    ###################
    # Stubs
    ###################
    def selectPointsStub(self):
        """
        :param filtered_dataframe:
        :return:
        """

        ## Convert dataframe into list of datetimes

        filtered_dataframe = self.get_filtered_points()
        if isinstance(filtered_dataframe, pd.DataFrame):
            if not filtered_dataframe.empty:
                datetime_list = filtered_dataframe.index.to_pydatetime()
                return datetime_list.tolist()
        return []

    ###################
    # Filters
    ###################
    # operator is a character, either '<' or '>'
    def filter_value(self, value, ops):
        df = self._test_filter_previous()

        if ops == '>':
            self.filtered_dataframe = df[df['datavalue'] > value]

        if ops == '<':
            self.filtered_dataframe = df[df['datavalue'] < value]


    def filter_date(self, before, after):
        df = self._test_filter_previous()
        if before and after:
            self.filtered_dataframe = df[(df.index < before) & (df.index > after)]

    def fill_gap(self, gap, fill):

        df = self.memDB.getDataValuesDF()
        gaps= self.find_gaps(df, gap[0], gap[1])
        points = []
        series= self.memDB.series
        timegap = np.timedelta64(fill[0], self.time_units[fill[1]])

        #if gaps is not of type dataframe- put it in a dataframe
        #if not isinstance(gaps, pd.DataFrame
        for g in gaps.iterrows():
            row = g[1]
            e = row.datetime
            s = row.dateprev

            #prime the loop
            s = s + timegap
            # for each gap time period in the larger gap ( until datetime = prev value)
            while s < e:
                utc_offset = (series.begin_date_time-series.begin_date_time_utc).total_seconds()/3600
                points.append((-9999, None, s, utc_offset, s, None, None, u'nc', None, None, series.site_id, series.variable_id, series.method_id, series.source_id, series.quality_control_level_id))
                #('-9999', None, DATE, series.begin_date_time_utc, UTCDATE, None, None, u'nc', None, None,
                #       series.site_id, series.variable_id, series.method_id, series.source_id,
                #       series.quality_control_level_id

                s = s + timegap
        #print points
        self.add_points(points)

    time_units = {
        'second': 's',
        'minute': 'm',
        'hour': 'h',
        'day': 'D',
        'week': 'W',
        'month': 'M',
        'year': 'Y'
    }

    # Data Gaps


    def find_gaps(self, df, value, time_period):



        # make a copy of the dataframe in order to modify it to be in the form we need to determine data gaps
        copy_df = df
        copy_df['datetime'] = df.index
        copy_df['dateprev'] = copy_df['datetime'].shift()

        # ensure that 'value' is an integer
        if not isinstance(value, int):
            value = int(value)

        # create a bool column indicating which rows meet condition
        filtered_results = copy_df['datetime'].diff() > np.timedelta64(value, self.time_units[time_period])

        # filter on rows that passed previous condition
        return copy_df[filtered_results]




    def data_gaps(self, value, time_period):
        df = self._test_filter_previous()
        copy_df = self.find_gaps(df, value, time_period)
        print (copy_df)
        # merge values and remove duplicates. this hack allows for both values to be marked when selecting data gaps
        newdf = pd.concat([copy_df['datetime'], copy_df['dateprev']], join='inner')

        # clean up
        del copy_df


        self.filtered_dataframe= df[df.index.isin(newdf.drop_duplicates().dropna())]


    def change_value_threshold(self, value, operator):

        df = self._test_filter_previous()

        # make a copy of the dataframe in order to modify it to be in the form we need to determine data gaps
        copy_df = df
        copy_df['values'] = df['datavalue']
        copy_df['diff'] = copy_df['values'].shift()
        copy_df["diff_date"] = copy_df['valuedatetime'].shift()
        copy_df['change_threshold'] = abs(df['values'] - df['diff'])

        if not isinstance(value, float):
            logger.error("Need to have a float")
            return

        copy_df['threshold'] = value

        if operator == ">":
            copy_df['matches'] = df['change_threshold'] >= copy_df['threshold']

        if operator == "<":
            copy_df['matches'] = df['change_threshold'] <= copy_df['threshold']

        filtered_df = copy_df[copy_df['matches']]
        tmplist = filtered_df['diff_date'].tolist() + filtered_df.index.tolist()
        del copy_df
        self.filtered_dataframe = df[df.index.isin(tmplist)]

    #Duplicate values filter
    def duplicate_value_filter(self):
        df = self._test_filter_previous()
        #self.filtered_dataframe= df[df.index.get_duplicates()]
        self.filtered_dataframe= df[df.index.isin(df.index.get_duplicates())]
        #self.filtered_dataframe = df[df['DataValue'] < value]


    def select_points_tf(self, tf_list):
        self._filter_list = tf_list

    #def select_points(self, id_list=[], datetime_list=[]):
    def select_points(self, id_list=[], dataframe=[]):
        #self.reset_filter()

        # This should be either one or the other. If it's both, id is used first.
        # If neither are set this function does nothing.

        if len(id_list) > 0:
            for i in range(len(self._series_points)):
                if self._series_points[i][0] in id_list:
                    self._filter_list[i] = True

        if isinstance(dataframe, pd.DataFrame):
            result = dataframe.index.astype(datetime.datetime)
            self.filtered_dataframe = self._series_points_df[self._series_points_df.index.isin(dataframe.index)]


    def reset_filter(self):
        self.filtered_dataframe = None

    def filter_from_previous(self, value):
        self._filter_from_selection = value

    def get_toggle(self):
        return self._filter_from_selection


    ###################
    # Gets
    ###################
    def get_series(self):
        return self.memDB.series_service.get_series(self._series_id)

    def get_series_points(self):
        # all point in the series_service
        return self._series_points

    def get_series_points_df(self):
        """
        :return Pandas DataFrame:
        """
        return self._series_points_df

    def get_filtered_points(self):
        """
        :return Pandas DataFrame:
        """
        if isinstance(self.filtered_dataframe, pd.DataFrame):
            if self.filtered_dataframe.empty:
                return None
        else:
            if not self.filtered_dataframe:
                return None
        if len(self.filtered_dataframe) > 0:
            return self.filtered_dataframe
        return None

    def get_filtered_dates(self):
        return self.filtered_dataframe

    def get_filter_list(self):
        # true or false list the length of the entire series_service. true indicate the point is selected
        return self._filter_list

    def get_qcl(self, qcl_id):
        return self.memDB.series_service.get_processing_level_by_id(qcl_id)

    def get_method(self, method_id):
        return self.memDB.series_service.get_method_by_id(method_id)

    def get_variable(self, variable_id):
        logger.debug(variable_id)
        return self.memDB.series_service.get_variable_by_id(variable_id)


    #################
    # Edits
    #################

    def change_value(self, value, operator):
        filtered_points = self.get_filtered_points()

        ids = filtered_points.index.tolist()
        self.memDB.updateValue(ids, operator, float(value))
        self._populate_series()

        ## update filtered_dataframe
        self.filtered_dataframe = self._series_points_df[self._series_points_df.index.isin(ids)]

    def add_points(self, points):
        # todo: add the ability to send in multiple datetimes to a single 'point'
        self.memDB.addPoints(points)

        self._populate_series()
        self.reset_filter()

    def delete_points(self):
        filtered_points = self.get_filtered_points()
        if not filtered_points.empty:
            values = filtered_points.index.tolist()

            self.memDB.delete(values)
            self._populate_series()
            self.filtered_dataframe = None

    def interpolate(self):
        '''
        In [75]: ser = Series(np.sort(np.random.uniform(size=100)))
        # interpolate at new_index
        In [76]: new_index = ser.index | Index([49.25, 49.5, 49.75, 50.25, 50.5, 50.75])
        In [77]: interp_s = ser.reindex(new_index).interpolate(method='pchip')
        '''

        tmp_filter_list =self.get_filtered_points()
        df = self._series_points_df
        issel = df.index.isin(tmp_filter_list.index)

        mdf = df["datavalue"].mask(issel)
        mdf.interpolate(method = "time", inplace=True)
        tmp_filter_list["datavalue"]=mdf[issel]
        ids = tmp_filter_list.index.tolist()

        #update_list = [(row["DataValue"], row["ValueID"]) for index, row in tmp_filter_list.iterrows()]
        update_list = [{"value": row["datavalue"], "id": index} for index, row in tmp_filter_list.iterrows()]

        self.memDB.update(update_list)

        self._populate_series()

        self.filtered_dataframe = self._series_points_df[self._series_points_df.index.isin(ids)]


    def drift_correction(self, gap_width):

        if self.isOneGroup():
            tmp_filter_list =self.get_filtered_points()
            startdate =tmp_filter_list.index[0]
            x_l = (tmp_filter_list.index[-1]-startdate).total_seconds()

            nodv = self.memDB.series.VariableObj.NoDataValue

            # y_n = y_0 + G(x_i / x_l)
            # f = lambda row :  row["datavalue"]+(gap_width * ((row.name-startdate).total_seconds() / x_l))


            f = lambda row :  row["datavalue"]+(gap_width * ((row.name-startdate).total_seconds() / x_l)) if row["datavalue"] != nodv else row["datavalue"]
            tmp_filter_list["datavalue"]=tmp_filter_list.apply(f, axis = 1)

            update_list = [{"value": row["datavalue"], "id":index} for index, row in tmp_filter_list.iterrows()]

            ids = tmp_filter_list.index.tolist()
            self.memDB.update(update_list)


            self._populate_series()

            self.filtered_dataframe = self._series_points_df[self._series_points_df.index.isin(ids)]
            return True
        return False




    def isOneGroup(self):

        issel = self._series_points_df.index.isin(self.get_filtered_points().index)

        found_group = False
        count = 0

        for x in issel:
            if x:
                if not found_group:
                    found_group=True
                    count =count+1
            else:
                found_group = False

            if count >1:
                return False
        if count == 1:
            return True


    def flag(self, qualifier_id):

        filtered_points = self.get_filtered_points()
        '''
        query = "UPDATE DataValues SET QualifierID = %s WHERE ValueID = ?" % (qualifier_id)
        #self._cursor.executemany(query, [(str(x[0]),) for x in filtered_points])
        self._cursor.executemany(query, [(str(x),) for x in filtered_points["ValueID"].astype(int).tolist()])
        '''
        self.memDB.updateFlag(filtered_points.index.tolist(), qualifier_id)

    def updateValues(self, values):
        """

        :param values: pandas Dataframe - must contain a "datavalues" column and a date time as the index
        :return:
        """
        if values is None:
            print("please send in a valid DataFrame object")
            return
        update_list = [{"value": row["DataValue"], "id": index} for index, row in values.iterrows()]

        ids = values.index.tolist()
        self.memDB.update(update_list)
        self._populate_series()

        self.filtered_dataframe = self._series_points_df[self._series_points_df.index.isin(ids)]

    ###################
    # Save/Restore
    ###################

    def restore(self):
        self.memDB.rollback()

        self._populate_series()
        self.reset_filter()

    def save(self,  result=None):
        try:
            values = self.memDB.getDataValuesDF()

            if not result:
                result = self.memDB.series_service.get_series(series_id = values['resultid'][0])
            else:
                values["resultid"] = result.ResultID

            # update result
            result.ValueCount = 0
            self.updateResult(result)
            # upsert values
            self.memDB.series_service.upsert_values(values)
            # save new annotations
            if len(self.memDB.annotation_list >0):
                self.add_annotations(self.memDB.annotation_list)
            return result
        except Exception as e:
            logger.error("Exception encountered while saving: {}".format(e))
            raise e
        return None

    def save_existing(self, result):
        result = self.save(result)
        return result

    def save_appending(self, result, overwrite=True):
        try:

            values = self.memDB.getDataValuesDF()

            # get value count
            vc = result.ValueCount
            # set in df
            values["resultid"] = result.ResultID

            # count = overlap calc
            count = self.overlapcalc(result, values, overwrite)
            # set value count = res.vc+valuecount-count
            valuecount = result.ValueCount + vc - count
            # update result
            self.updateResult(result, valuecount)
            # insert values
            self.memDB.series_service.upsert_values(values)
            # save new annotations
            if len(self.memDB.annotation_list >0):
                self.add_annotations(self.memDB.annotation_list)
            return result
        except Exception as e:
            logger.error("Exception encountered while performing a save as: {}".format(e))
            raise e
        return None

    def save_as(self, variable, method, proc_level, action, action_by):

        try:
            #save as new series
            values = self.memDB.getDataValuesDF()
            # get all annotations for series
            annolist= self.memDB.series_service.get_annotations_by_result(str(values["resultid"][0]))
            annolist['valueid'] = None

            # create series
            result = self.getResult(variable, method, proc_level, action, action_by)

            # set in df
            values["valueid"] = None
            values["resultid"] = result.ResultID
            # insert values
            self.memDB.series_service.insert_values(values)

            #combine all of the annotations new annotations with the existing
            frames = [self.memDB.annotation_list, annolist]
            annolist = pd.concat(frames)
            # save all annotations
            if len(annolist > 0):
                self.add_annotations(annolist)

            return result
        except Exception as e:
            logger.error("Exception encountered while performing a save as: {}".format(e))
            raise e


    def getResult(self, var, meth, proc, action, action_by):
        id = self.memDB.getDataValuesDF()["resultid"]

        # copy old
        # what is my original result
        result = self.memDB.series_service.get_series(str(id[0]))

        sfid = result.FeatureActionObj.SamplingFeatureID
        aggcv = result.AggregationStatisticCV
        itsp = result.IntendedTimeSpacing
        itspunit = result.IntendedTimeSpacingUnitsID
        status = result.StatusCV
        type = result.ResultTypeCV
        units = result.UnitsID
        medium = result.SampledMediumCV


        self.memDB.series_service._session.expunge(result)
        # change var, meth proc, in df #intend ts, agg sta
        if var:
            result.VariableID = var.VariableID


        if proc:
            result.ProcessingLevelID = proc.ProcessingLevelID

        result.ResultID=None
        result.ResultUUID = None


        #if result does not exist
        if not self.memDB.series_service.resultExists(result):
            try:

                #create Action
                if meth:
                    id = meth.MethodID
                    # new_action.MethodObj = meth.MethodOb
                else:
                    id = action.MethodID
                new_action, action_by = self.memDB.series_service.create_action(id, action.ActionDescription, action.ActionFileLink, action.BeginDateTime, action.BeginDateTimeUTCOffset, action_by)

                # create FeatureAction (using current sampling feature id)
                feature_action = self.memDB.series_service.createFeatureAction(sfid, new_action.ActionID)

                if var:
                    varid = var.VariableID
                else:
                    varid = result.VariableID

                if proc:
                    procid= proc.ProcessingLevelID
                else:
                    procid= result.ProcessingLevelID
                result = self.memDB.series_service.create_result(varid, procid,  feature_action.FeatureActionID,
                                                                     aggcv, itsp, itspunit, status, type, units, medium)

            except Exception as ex:
                self.memDB.series_service._session.rollback()
                print ex
                raise ex
        else:
            #if saveas called me throw an error that this series already exists
            import inspect
            (frame, filename, line_number,
             function_name, lines, index) = inspect.getouterframes(inspect.currentframe())[1]

            if function_name =='save_as':
                raise Exception("this series already exists, but you have chosen to create a new series")
            else:
                #it already exists, so get it
                result = self.memDB.series_service.get_series_by_meta(result)

        return self.updateResult(result)

    def updateResult(self, result, valuecount=-10):
        form = "%Y-%m-%d %H:%M:%S"
        # get pd
        values = self.memDB.getDataValuesDF()

        # update count, dates,
        action = result.FeatureActionObj.ActionObj
        action.BeginDateTime = datetime.datetime.strptime(str(np.min(values["valuedatetime"])), form)
        action.EndDateTime = datetime.datetime.strptime(str(np.max(values["valuedatetime"])), form)

        #TODO how does valuecount change, when do i send it in
        if valuecount > 0:
            result.ValueCount = valuecount
        else:
            result.ValueCount = len(values)

        self.memDB.series_service.update_result(result=result)
        self.memDB.series_service.update_action(action=action)
        return result

    def overlapcalc(self, result, values,  overwrite):
        form = "%Y-%m-%d %H:%M:%S"

        # is there any overlap
        dbend = result.FeatureActionObj.ActionObj.EndDateTime
        dfstart = datetime.datetime.strptime(str(np.min(values["valuedatetime"])), form)
        overlap = dbend >= dfstart
        # number of overlapping values
        overlapdf = values[(values["valuedatetime"] <= dfstart) & (values["valuedatetime"] >= dbend)]
        count = len(overlapdf)

        # if not overwrite. remove any overlapping values from df
        if overlap:
            if not overwrite:
                # delete overlapping from the data frame before saving to the database
                values = values[values["valuedatetime"] > dbend]

            else:
                # delete overlapping values from the series database
                count = self.memDB.series_service.delete_values_by_series(str(values["resultid"]), dfstart)


        # return the number of overlapping values
        return count

    def add_annotations(self, annolist):
        # match up with existing values and get value id

        engine = self.memDB.series_service._session_factory.engine

        q =self.memDB.series_service._session.query(TimeSeriesResultValues) \
            .filter(TimeSeriesResultValues.ResultID == int(min(annolist["resultid"])))

        query = q.statement.compile(dialect=engine.dialect)
        # data = pd.read_sql_query(sql=query, con=self._session_factory.engine,
        #                          params=query.params)
        # query = "SELECT ValueID, ResultID, ValueDateTime  FROM TimeSeriesResultValues Where ResultID="+annolist["ResultID"][0]

        vals = pd.read_sql_query(sql=query, con=engine, params=query.params)
        # remove any duplicates
        annolist.drop_duplicates(["resultid", "annotationid", "valuedatetime"], keep='last', inplace=True)
        newdf = pd.merge(annolist, vals, how='left', on=["resultid", "valuedatetime"], indicator=True)

        # get only AnnotationID and ValueID
        mynewdf= newdf[["valueid_y","annotationid"]]
        mynewdf.columns = ["ValueID", "AnnotationID"]


        # save df to db
        self.memDB.series_service.add_annotations(mynewdf)



    def create_qcl(self, code, definition, explanation):
        return self.memDB.series_service.create_processing_level(code, definition, explanation)

    def create_method(self, description, link):
        return self.memDB.series_service.create_method(description, link)

    def create_qualifier(self, code, definition):
        return self.memDB.series_service.create_annotation(code, definition)

    def create_variable(self, code, name, speciation, variable_unit_id, sample_medium,
                        value_type, is_regular, time_support, time_unit_id, data_type, general_category, no_data_value):

        return self.memDB.series_service.create_variable(code, name, speciation, variable_unit_id, sample_medium,
                                                    value_type, is_regular, time_support, time_unit_id, data_type,
                                                    general_category, no_data_value)

    def reconcile_dates(self, parent_series_id):
        # FUTURE FEATURE: pull in new field data from another series_service and add to this series_service
        # (i.e one series_service contains new field data of an edited series_service at a higher qcl)
        pass


