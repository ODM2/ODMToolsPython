import sqlite3


from odmtools.odmdata import DataValue
from series_service import SeriesService

from odmtools.odmdata import series as series_module

import pandas as pd
import datetime
import numpy as np

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

        if connection_string is  "" and connection is not None:
            self.memDB= connection

        elif connection_string is not "" and connection is None:
            from odmtools.odmdata import MemoryDatabase
            self.memDB= MemoryDatabase()
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

            result = pd.DataFrame(datetime_list, columns=["LocalDateTime"])

            result.set_index("LocalDateTime", inplace=True)

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
            self.filtered_dataframe = df[df['DataValue'] > value]

        if ops == '<':
            self.filtered_dataframe = df[df['DataValue'] < value]


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
        copy_df['values'] = df['DataValue']
        copy_df['diff'] = copy_df['values'].shift()
        copy_df["diff_date"] = copy_df['LocalDateTime'].shift()
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
        return self.memDB.series_service.get_series_by_id(self._series_id)

    def get_series_points(self):
        # all point in the series
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
        # true or false list the length of the entire series. true indicate the point is selected
        return self._filter_list

    def get_source(self, src_id):
        return self.memDB.series_service.get_src_by_id(src_id)

    def get_qcl(self, qcl_id):
        return self.memDB.series_service.get_qcl_by_id(qcl_id)

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

        mdf = df["DataValue"].mask(issel)
        mdf.interpolate(method = "time", inplace=True)
        tmp_filter_list["DataValue"]=mdf[issel]
        ids = tmp_filter_list.index.tolist()

        #update_list = [(row["DataValue"], row["ValueID"]) for index, row in tmp_filter_list.iterrows()]
        update_list = [{"value": row["DataValue"], "id": index} for index, row in tmp_filter_list.iterrows()]

        self.memDB.update(update_list)

        self._populate_series()

        self.filtered_dataframe = self._series_points_df[self._series_points_df.index.isin(ids)]


    def drift_correction(self, gap_width):

        if self.isOneGroup():
            tmp_filter_list =self.get_filtered_points()
            startdate =tmp_filter_list.index[0]
            x_l = (tmp_filter_list.index[-1]-startdate).total_seconds()
            #nodv= self.memDB.series_service.get_variable_by_id(self.memDB.df["VariableID"][0])
            nodv = self.memDB.series.variable.no_data_value
            # y_n = y_0 + G(x_i / x_l)
            f = lambda row :  row["DataValue"]+(gap_width * ((row.name-startdate).total_seconds() / x_l)) if row["DataValue"] != nodv else row["DataValue"]
            tmp_filter_list["DataValue"]=tmp_filter_list.apply(f, axis = 1)

            update_list = [{"value": row["DataValue"], "id":index} for index, row in tmp_filter_list.iterrows()]

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

    def updateSeries(self, var=None, method=None, qcl=None, source =None, is_new_series=False, overwrite = True, append = False):
        """

        :param var:
        :param method:
        :param qcl:
        :param is_new_series:
        :return:
        """

        var_id = var.id if var is not None else None
        method_id = method.id if method is not None else None
        qcl_id = qcl.id if qcl is not None else None
        src_id = source.id if source is not None else None

        #self.memDB.changeSeriesIDs(var_id, method_id, qcl_id)
        dvs = self.memDB.getDataValuesDF()
        if var_id is not None:
            dvs["VariableID"] = var_id
        if method_id is not None:
            dvs["MethodID"] = method_id
        if qcl_id is not None:
            dvs["QualityControlLevelID"] = qcl_id
        if src_id is not None:
            dvs["SourceID"] = src_id



        #if is new series remove valueids
        #if is_new_series:
        dvs["ValueID"] = None
        '''
            for dv in dvs:
                dv.id = None
        '''

        series = self.memDB.series_service.get_series_by_id(self._series_id)
        logger.debug("original editing series id: %s" % str(series.id))

        if (var or method or qcl ):
            tseries = self.memDB.series_service.get_series_by_id_quint(site_id=int(series.site_id),
                                                                  var_id=var_id if var else int(series.variable_id),
                                                                  method_id=method_id if method else int(
                                                                      series.method_id),
                                                                  source_id= src_id if source else int(
                                                                      series.source_id),
                                                                  qcl_id=qcl_id if qcl else int(
                                                                      series.quality_control_level_id))
            if tseries:
                logger.debug("Save existing series ID: %s" % str(tseries.id))
                series = tseries
            else:
                print "Series doesn't exist (if you are not, you should be running SaveAs)"

        if is_new_series:
            series = series_module.copy_series(series)
            if var:
                series.variable_id = var_id
                series.variable_code = var.code
                series.variable_name = var.name
                series.speciation = var.speciation
                series.variable_units_id = var.variable_unit_id
                series.variable_units_name = var.variable_unit.name
                series.sample_medium = var.sample_medium
                series.value_type = var.value_type
                series.time_support = var.time_support
                series.time_units_id = var.time_unit_id
                series.time_units_name = var.time_unit.name
                series.data_type = var.data_type
                series.general_category = var.general_category

            if method:
                series.method_id = method_id
                series.method_description = method.description

            if qcl:
                series.quality_control_level_id = qcl_id
                series.quality_control_level_code = qcl.code
            if source:
                series.source_id = src_id
                series.organization = source.organization
                series.source_description = source.description
                series.citation = source.citation


        '''
        dvs["LocalDateTime"] = pd.to_datetime(dvs["LocalDateTime"])
        dvs["DateTimeUTC"] = pd.to_datetime(dvs["DateTimeUTC"])
        '''

        form = "%Y-%m-%d %H:%M:%S"

        if not append:

            series.begin_date_time = datetime.datetime.strptime(str(np.min(dvs["LocalDateTime"])), form)#np.min(dvs["LocalDateTime"])#dvs[c0].local_date_time
            series.end_date_time = datetime.datetime.strptime(str(np.max(dvs["LocalDateTime"])), form)#np.max(dvs["LocalDateTime"])#dvs[-1].local_date_time
            series.begin_date_time_utc = datetime.datetime.strptime(str(np.min(dvs["DateTimeUTC"])), form) #dvs[0].date_time_utc
            series.end_date_time_utc = datetime.datetime.strptime(str(np.max(dvs["DateTimeUTC"])), form) #dvs[-1].date_time_utc
            series.value_count = len(dvs)

            ## Override previous save
            if not is_new_series:
                # delete old dvs
                #pass
                self.memDB.series_service.delete_values_by_series(series)
        elif append:
            #if series end date is after  dvs startdate
            dbend = series.end_date_time
            dfstart = datetime.datetime.strptime(str(np.min(dvs["LocalDateTime"])), form)
            overlap = dbend>= dfstart
            #leave series start dates to those previously set
            series.end_date_time = datetime.datetime.strptime(str(np.max(dvs["LocalDateTime"])), form)
            series.end_date_time_utc = datetime.datetime.strptime(str(np.max(dvs["DateTimeUTC"])), form)
            #TODO figure out how to calculate the new value count
            series.value_count = len(dvs)

            if overlap:
                if overwrite:
                    #remove values from the database
                    self.memDB.series_service.delete_values_by_series(series, startdate=dfstart)
                else:
                    #remove values from df
                    dvs = dvs[dvs["LocalDateTime"] > dbend]



        #logger.debug("series.data_values: %s" % ([x for x in series.data_values]))
        dvs.drop('ValueID', axis=1, inplace=True)
        return series, dvs

    def save(self):
        """ Save to an existing catalog
        :param var:
        :param method:
        :param qcl:
        :return:
        """

        series, dvs = self.updateSeries(is_new_series=False)
        if self.memDB.series_service.save_series(series, dvs):
            logger.debug("series saved!")
            return True
        else:
            logger.debug("The Save was unsuccessful")
            return False

    def save_as(self, var=None, method=None, qcl=None, source =None):
        """
        :param var:
        :param method:
        :param qcl:
        :return:
        """
        series, dvs = self.updateSeries(var, method, qcl, source, is_new_series=True)

        if self.memDB.series_service.save_new_series(series, dvs):
            logger.debug("series saved!")
            return True
        else:
            logger.debug("The Save As Function was Unsuccessful")
            return False

    def save_appending(self, var= None, method = None, qcl=None, source=None, overwrite=False):
        series, dvs = self.updateSeries(var, method, qcl, source, is_new_series=False, append= True, overwrite=overwrite)

        if self.memDB.series_service.save_series(series, dvs):
            logger.debug("series saved!")
            return True
        else:
            logger.debug("The Append Existing Function was Unsuccessful")
            return False

    def save_existing(self, var=None, method=None, qcl=None, source=None):
        """
        :param var:
        :param method:
        :param qcl:
        :return:
        """
        series, dvs = self.updateSeries(var, method, qcl, source, is_new_series=False)
        if self.memDB.series_service.save_series(series, dvs):
            logger.debug("series saved!")
            return True
        else:
            logger.debug("The Save As Existing Function was Unsuccessful")
            return False

    def create_qcl(self, code, definition, explanation):
        return self.memDB.series_service.create_qcl(code, definition, explanation)

    def create_source(self, src):
        return self.memDB.series_service.create_source(src)

    def create_method(self, description, link):
        return self.memDB.series_service.create_method(description, link)

    def create_qualifier(self, code, definition):
        return self.memDB.series_service.create_qualifier(code, definition)

    def create_variable(self, code, name, speciation, variable_unit_id, sample_medium,
                        value_type, is_regular, time_support, time_unit_id, data_type, general_category, no_data_value):

        return self.memDB.series_service.create_variable(code, name, speciation, variable_unit_id, sample_medium,
                                                    value_type, is_regular, time_support, time_unit_id, data_type,
                                                    general_category, no_data_value)

    def reconcile_dates(self, parent_series_id):
        # FUTURE FEATURE: pull in new field data from another series and add to this series
        # (i.e one series contains new field data of an edited series at a higher qcl)
        pass


