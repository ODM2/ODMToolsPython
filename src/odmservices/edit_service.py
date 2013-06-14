from odmdata import SessionFactory
from odmdata import Site
from odmdata import Variable
from odmdata import Unit
from odmdata import Series
from odmdata import DataValue
from odmdata import QualityControlLevel
from odmdata import Qualifier

from series_service import SeriesService

import sqlite3

class EditService():
    # Mutual exclusion: cursor, or connection_string
    def __init__(self, series_id, connection=None, connection_string="",  debug=False):
        # print "Series id: ", series_id
        self._connection = connection
        self._series_id = series_id
        self._filter_from_selection = False
        self._debug = debug

        if (connection_string is not ""):
            self._session_factory = SessionFactory(connection_string, debug)
            self._series_service = SeriesService(connection_string, debug)
        elif (factory is not None):
            self._session_factory = factory
            service_manager = ServiceManager()
            self._series_service = service_manager.get_series_service()
        else:
            # One or the other must be set
            print "Must have either a connection string or session factory"
            # TODO throw an exception
        
        self._edit_session = self._session_factory.get_session()

        if self._connection == None:
            series_service = SeriesService(connection_string, False)
            series = series_service.get_series_by_id(series_id)
            DataValues = series.get_data_values_tuples()
            self._connection = sqlite3.connect(":memory:", detect_types= sqlite3.PARSE_DECLTYPES)
            tmpCursor = self._connection.cursor()
            self.init_table(tmpCursor)
            tmpCursor.executemany("INSERT INTO DataValuesEdit VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", DataValues)

        self._connection.commit()
        self._cursor = self._connection.cursor()

        self._populate_series()

    def _populate_series(self):
        # [(ID, value, datetime), ...]
        self._cursor.execute("SELECT ValueID, DataValue, LocalDateTime FROM DataValuesEdit ORDER BY LocalDateTime")
        results = self._cursor.fetchall()

        self._series_points = results
        self.reset_filter()

    def _test_filter_previous(self):
        if not self._filter_from_selection:
            self.reset_filter()

    ###################
    # Filters
    ###################
    # operator is a character, either '<' or '>'
    def filter_value(self, value, operator):
        self._test_filter_previous()

        if operator == '<': # less than
            for i in range(len(self._series_points)):
                # If it's not already in the selection, skip it
                if (self._filter_from_selection and not self._filter_list[i]):
                    continue
                if self._series_points[i][1] < value:
                    self._filter_list[i] = True
                else:
                    self._filter_list[i] = False
        if operator == '>': # greater than
            for i in range(len(self._series_points)):
                if (self._filter_from_selection and not self._filter_list[i]):
                    continue
                if self._series_points[i][1] > value:
                    self._filter_list[i] = True
                else:
                    self._filter_list[i] = False

    def filter_date(self, before, after):
        self._test_filter_previous()

        previous_date_filter = False
        if before != None:
            tmp = []
            for i in range(len(self._series_points)):
                if (self._filter_from_selection and not self._filter_list[i]):
                    continue
                if self._series_points[i][2] < before:
                    self._filter_list[i] = True
                else:
                    self._filter_list[i] = False
            previous_date_filter = True        # We've done a previous date filter
        if after != None:
            for i in range(len(self._series_points)):
                if ((previous_date_filter or self._filter_from_selection)
                     and not self._filter_list[i]):
                    continue
                if self._series_points[i][2] > after:
                    self._filter_list[i] = True
                else:
                    self._filter_list[i] = False

    # Data Gaps
    def data_gaps(self, value, time_period):
        length = len(self._series_points)

        value_sec = 0

        if time_period == 'second':
            value_sec = value
        if time_period == 'minute':
            value_sec = value * 60
        if time_period == 'hour':
            value_sec = value * 60 * 60
        if time_period == 'day':
            value_sec = value * 60 * 60 * 24

        tmp = {}

        for i in xrange(length):
            if (self._filter_from_selection and 
                not self._filter_list[i]):
                continue

            if i + 1 < length:      # make sure we stay in bounds
                point1 = self._series_points[i]
                point2 = self._series_points[i+1]
                interval = point2[2] - point1[2]
                interval_total_sec = interval.total_seconds()

                if interval_total_sec >= value_sec:
                    tmp[i] = True
                    tmp[i+1] = True
        
        self.reset_filter()
        for key in tmp.keys():
            self._filter_list[key] = True

    def value_change_threshold(self, value):

        length = len(self._series_points)
        tmp = {}
        for i in xrange(length):
            if (self._filter_from_selection and 
                not self._filter_list[i]):
                continue

            if i + 1 < length:         # make sure we stay in bounds
                point1 = self._series_points[i]
                point2 = self._series_points[i+1]
                if abs(point1[1] - point2[1]) >= value:
                    tmp[i] = True
                    tmp[i + 1] = True

        self.reset_filter()
        for key in tmp.keys():
            self._filter_list[key] = True

    def select_points_tf(self, tf_list):
        self._filter_list = tf_list

    def select_points(self, id_list=[], datetime_list=[]):
        self.reset_filter()

        # This should be either one or the other. If it's both, id is used first.
        # If neither are set this function does nothing.
        if id_list != None:
            for i in range(len(self._series_points)):
                if self._series_points[i][0] in id_list:
                    self._filter_list[i] = True
        elif datetime_list != None:
            for i in range(len(self._series_points)):
                if self._series_points[i][2] in datetime_list:
                    self._filter_list[i] = True
        else:
            pass


    def reset_filter(self):
        self._filter_list = [False] * len(self._series_points)

    def toggle_filter_previous(self):
        self._filter_from_selection = not self._filter_from_selection


    ###################
    # Gets
    ###################
    def get_series(self):
        return self._series_service.get_series_by_id(self._series_id)

    def get_series_points(self):
        return self._series_points

    def get_filtered_points(self):
        tmp = []
        for i in range(len(self._series_points)):
            if self._filter_list[i]:
                tmp.append(self._series_points[i])

        return tmp

    def get_filter_list(self):
        return self._filter_list

    
    #################
    # Edits
    #################

    def change_value(self, value, operator):
        filtered_points = self.get_filtered_points()
        tmp_filter_list = self._filter_list
        query = "UPDATE DataValuesEdit SET DataValue = "
        if operator == '+':
            query += " DataValue + %s " % (value)

        if operator == '-':
            query += " DataValue - %s " % (value)

        if operator == '*':
            query += " DataValue * %s " % (value)

        if operator == '=':
            query += "%s " % (value)

        query += "WHERE ValueID IN ("
        for i in range(len(filtered_points) - 1):
            query += "%s," % (filtered_points[i][0])
        query += "%s)" % (filtered_points[-1][0])
        self._cursor.execute(query)

        self._populate_series()
        self._filter_list = tmp_filter_list

    def add_points(self, points):
        print points
        query = "INSERT INTO DataValuesEdit (DataValue, ValueAccuracy, LocalDateTime, UTCOffset, DateTimeUTC, OffsetValue, OffsetTypeID, "
        query += "CensorCode, QualifierID, SampleID, SiteID, VariableID, MethodID, SourceID, QualityControlLevelID) "
        query += "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
        self._cursor.executemany(query, points)
        self._populate_series()

    def delete_points(self):
        query = "DELETE FROM DataValuesEdit WHERE ValueID IN ("
        filtered_points = self.get_filtered_points()
        num_filtered_points = len(filtered_points)
        if num_filtered_points > 0:
            for i in range(num_filtered_points-1):        # loop through the second-to-last active point
                query += "%s," % (filtered_points[i][0])   # append its ID
            query += "%s)" % (filtered_points[-1][0])  # append the final point's ID and close the set

            # Delete the points from the cursor
            self._cursor.execute(query)

            self._populate_series()
    
    def interpolate(self):
        tmp_filter_list = self._filter_list
        groups = self.get_selection_groups()

        for group in groups:
            # determine first and last point for the interpolation
            first_index = group[0] - 1
            last_index  = group[-1] + 1
            # ignore this group (which is actually the whole set)
            # if it includes the first or last point of the series
            if first_index <= 0 or last_index == len(self._series_points):
                continue

            first_point = self._series_points[first_index]
            last_point  = self._series_points[last_index]
            a = 0
            c = (last_point[2] - first_point[2]).total_seconds()
            f_a = first_point[1]
            f_c = last_point[1]
            update_list = []
            for i in group:
                b = (self._series_points[i][2] - first_point[2]).total_seconds()
                # linear interpolation formula: f(b) = f(a) + ((b-a)/(c-a))*(f(c) - f(a))
                new_val = f_a + ((b - a)/(c-a))*(f_c - f_a)
                point_id = self._series_points[i][0]
                update_list.append((new_val, point_id))
            query = "UPDATE DataValuesEdit SET DataValue = ? WHERE ValueID = ?"
            self._cursor.executemany(query, update_list)

        self._populate_series()
        self._filter_list = tmp_filter_list

    def drift_correction(self, gap_width):
        tmp_filter_list = self._filter_list
        groups = self.get_selection_groups()

        # only perform a drift correction if there's a single group
        if len(groups) == 1:
            group = groups[0]
            first_index = group[0]
            last_index  = group[-1]
            first_point = self._series_points[first_index]
            last_point = self._series_points[last_index]
            x_l = (last_point[2] - first_point[2]).total_seconds()

            update_list = []
            for i in group:
                point = self._series_points[i]
                x_i = (point[2] - first_point[2]).total_seconds()
                # y_n = y_0 + G(x_i / x_l)
                new_val = point[1] + gap_width * (x_i / x_l)
                update_list.append((new_val, point[0]))
            query = "UPDATE DataValuesEdit SET DataValue = ? WHERE ValueID = ?"
            self._cursor.executemany(query, update_list)

            self._populate_series()
            self._filter_list = tmp_filter_list
            
            return True
        else:
            return False

    def get_selection_groups(self):
        length = len(self._series_points)
        found_group = False
        groups = []
        cur_group = []
        for i in range(length):
            if self._filter_list[i]:
                if not found_group:
                    found_group = True
                cur_group.append(i)         # Append the actual index to the point
                if i == length - 1:
                    groups.append(cur_group)
            elif not self._filter_list[i] and found_group:
                found_group = False
                groups.append(cur_group)
                cur_group = []
            else:
                continue
        
        return groups

    def flag(self, qualifier_id):
        filtered_points = self.get_filtered_points()
        query = "UPDATE DataValuesEdit SET QualifierID = %s WHERE ValueID = ?" % (qualifier_id)
        self._cursor.executemany(query, [(str(x[0]),) for x in filtered_points])

    ###################
    # Save/Restore
    ###################

    def restore(self):
        self._connection.rollback()
        self._populate_series()

    def save(self, var_id=None, method_id=None, qcl_id=None):
        # These can change when saving a series
        # VariableID
        # MethodID
        # QualityControlLevelID     (cannot be saved as a zero)

        dvs = []
        self._cursor.execute("DELETE FROM DataValues")
        self._cursor.execute("SELECT * FROM DataValuesEdit ORDER BY LocalDateTime")
        results = self._cursor.fetchall()

        query = "INSERT INTO DataValues (ValueID, DataValue, ValueAccuracy, LocalDateTime, UTCOffset, DateTimeUTC, SiteID, VariableID, "
        query += "OffsetValue, OffsetTypeID, CensorCode, QualifierID, MethodID, SourceID, SampleID, DerivedFromID, QualityControlLevelID) "
        query += "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
        self._cursor.executemany(query, results)

        if var_id:
            self._cursor.execute("UPDATE DataValues SET VariableID = %s" % (var_id))
        if method_id:
            self._cursor.execute("UPDATE DataValues SET MethodID = %s" % (method_id))
        if qcl_id:
            # get qcl and check that the code is not zero
            qcl = self._series_service.get_qcl(qcl_id)
            if qcl.code > 0:
                self._cursor.execute("UPDATE DataValues SET QualityControlLevelID = %s" % (qcl_id))
            else:
                raise ValueError("Quality Control Level cannot be zero")

        self._connection.commit()

    def write_to_db(self, var_id=None, method_id=None, qcl_id=None):
        dvs = []
        self._cursor.execute("SELECT * FROM DataValuesEdit ORDER BY LocalDateTime")
        results = self._cursor.fetchall()

        # ValueID, DataValue, ValueAccuracy, LocalDateTime, UTCOffset, DateTimeUTC, SiteID, VariableID, 
        # OffsetValue, OffsetTypeID, CensorCode, QualifierID, MethodID, SourceID, SampleID, DerivedFromID, QualityControlLevelID
        for row in results:
            dv = DataValue()

            if row[0]:
                dv.id = row[0]
            dv.data_value               = row[1]
            dv.value_accuracy           = row[2]
            dv.local_date_time          = row[3]
            dv.utc_offset               = row[4]
            dv.date_time_utc            = row[5]
            dv.site_id                  = row[6]
            if var_id == None:
                dv.variable_id = row[7]
            else:
                dv.variable_id = var_id
            dv.offset_value             = row[8]
            dv.offset_type_id           = row[9]
            dv.censor_code              = row[10]
            dv.qualifier_id             = row[11]
            if method_id == None:
                dv.method_id = row[12]
            else:
                dv.method_id = method_id
            dv.source_id                = row[13]
            dv.sample_id                = row[14]
            dv.derived_from_id          = row[15]
            if qcl_id == None:
                dv.quality_control_level_id = row[16]
            else:
                dv.quality_control_level_id = qcl_id

            # make sure the qcl is not zero
            qcl = self._series_service.get_qcl(dv.quality_control_level_id)
            if qcl.code <= 0:
                raise ValueError("Quality Control Level cannot be zero")

            dvs.add(dv)

        series = self._series_service.get_series_by_id(self._series_id)
        series.data_values = dvs

    def reconcile_dates(self, parent_series_id):
        # append new data to this series
        pass

    def init_table(self, cursor):
        cursor.execute("""CREATE TABLE DataValuesEdit
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
                UNIQUE (DataValue, LocalDateTime, SiteID, VariableID, MethodID, SourceID, QualityControlLevelID))
               """)