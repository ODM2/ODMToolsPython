# This class is intended for users to simplify console interaction

from wx.lib.pubsub import pub as Publisher
from odmservices import ServiceManager
from odmdata import Qualifier


class ConsoleTools(object):

    def __init__(self, ribbon, record_service=None):
        self._edit_error = "no series selected for editing"
        self._add_point_req_error = "A required field was left empty"
        self._add_point_req_error = "A date is not formatted correctly"

        self._ribbon = ribbon
        self._record_service = record_service

    

    ################
    # Set methods
    ################
    def set_record_service(self, rec_serv):
        self._record_service = rec_serv

    def toggle_recording(self):
        if self._record_service:
            self._record_service.toggle_record()
        else:
            return "Cannot record: %s" % (self._edit_error)

    def toggle_filter_previous(self):
        if self._record_service:
            self._record_service.toggle_filter_previous()

    def restore(self):
        if self._record_service:
            self._record_service.restore()

    ################
    # Filter methods
    ################
    def filter_value(self, value, operator):
        if self._record_service:
            self._record_service.filter_value(value, operator)
            self.refresh_plot()
        else:
            return "Cannot filter: %s" % (self._edit_error)

    def filter_dates(self, before, after):
        if self._record_service:
            self._record_service.filter_dates(before, after)
            self.refresh_plot()
        else:
            return "Cannot filter: %s" % (self._edit_error)

    def data_gaps(self, value, time_period):
        if self._record_service:
            self._record_service.data_gaps(value, time_period)
            self.refresh_plot()

    def value_change_threshold(self, value):
        if self._record_service:
            self._record_service.value_change_threshold(value)
            self.refresh_plot()

    def reset_filter(self):
        if self._record_service:
            self._record_service.reset_filter()
            self.refresh_plot()

    def get_series_points(self):
        if self._record_service:
            return self._record_service.get_series_points()

    def get_filtered_points(self):
        if self._record_service:
            return self._record_service.get_filtered_points()
    
    ################
    # Edit methods
    ################

    def change_value(self, value, operator):
        if self._record_service:
            self._record_service.change_value(value, operator)
            self.refresh_plot()

    def add_point(self, data_value, value_accuracy, local_datetime, utc_offset, datetime_utc, offset_value, offset_type, censor_code, qualifier_code, lab_sample_code):
        if (data_value == None or local_datetime == None or utc_offset == None or
            datetime_utc == None or censor_code == None or censor_code == ""):
            return "Error adding point: %s" % (self._add_point_req_error)

        point = (data_value, value_accuracy, local_datetime, utc_offset, datetime_utc, offset_value, offset_type, censor_code, qualifier_code, lab_sample_code)
        point_list = []
        point_list.append(point)
        if self._record_service:
            self._record_service.add_points(point_list)
            self.refresh_plot()

    def add_points(self, point_list):
        for point in point_list:
            #data_value, local_datetime, utc_offset, datetime_utc, censor_code
            if (point[0] == None or point[2] == None or point[3] == None or
                point[4] == None or point[7] == None or point[7] == ""):
                return "Error adding point: %s" % (self._add_point_req_error)

            if (type(point[2]) is not datetime or
                type(point[4]) is not datetime):
                return "Error adding point: %s" % (self._add_point_format_error)

        if self._record_service:
            self._record_service.add_points(point_list)
            self.refresh_plot()

    def flag(self, qualifier_id):
        if self._record_service:
            self._record_service.flag(qualifier_id)
            self.refresh_plot()

    def delete_points(self):
        if self._record_service:
            self._record_service.delete_points()
            self.refresh_plot()

    def interpolate(self):
        if self._record_service:
            self._record_service.interpolate()
            self.refresh_plot()

    def drift_correction(self, gap_width):
        if self._record_service:
            self._record_service.drift_correction(gap_width)
            self.refresh_plot()

    def restore(self):
        if self._record_service:
            self._record_service.restore()
            self.refresh_plot()

    ###############
    # Create stuffs
    ###############

    def create_qualifer(self, code, description):
        serv_man = ServiceManager()
        cv_service = serv_man.get_cv_service()
        q = Qualifier()
        q.code = code
        q.description = description
        cv_service.create_qualifer(q)
        return q.id

    def create_qcl(self, code, definition, explanation):
        qcl = self._record_service.create_qcl(code, definition, explanation)
        return qcl

    def create_method(self, method):
        method = self._record_service.create_method(method)
        return method

    def create_variable(self, var):
        var = self._record_service.create_variable(var)
        return var


    ###############
    # Export methods
    ###############
    def export_series_data(self, series_id, filename):
        serv_man = ServiceManager()
        export_service = serv_man.get_export_service()
        export_service.export_series_data(series_id, filename, True,True,True,True,True,True,True)

    def export_series_metadata(self, series_id, filename):
        serv_man = ServiceManager()
        export_service = serv_man.get_export_service()
        export_service.export_series_metadata(series_id, filename)


    ###############
    # UI methods
    ###############
    def refresh_plot(self):
        Publisher.sendMessage(("changePlotSelection"), sellist=self._record_service.get_filter_list())
        Publisher.sendMessage(("updateValues"), event=None)