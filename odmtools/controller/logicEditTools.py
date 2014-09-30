import logging

from wx.lib.pubsub import pub as Publisher
#from odmtools.odmservices import ServiceManager
from odmtools.odmdata import Qualifier
from odmtools.common.logger import LoggerTool


tool = LoggerTool()
logger = tool.setupLogger(__name__, __name__ + '.log', 'w', logging.DEBUG)


class EditTools():
    # Script header (imports etc.) will be set up in Main when record is clicked.
    def __init__(self, parent, script, edit_service, connection_string,  record=False):
        self._script = script
        # logger.debug(dir(self._script))sr
        self._edit_service = edit_service
        self._connection_string = connection_string
        self._record = record
        self._serv_man = parent

        self._edit_error = "no series selected for editing"
        self._add_point_req_error = "A required field was left empty"
        self._add_point_format_error = "A date is not formatted correctly"

        #self._record_service = record_service

    def get_series_service(self):
        return self._edit_service._series_service


    # ##################
    # Filters
    ###################
    def filter_value(self, value, operator):
        self._edit_service.filter_value(value, operator)
        self.refresh_plot()
        if self._record:
            self._script("edit_service.filter_value(%s, '%s')\n" % (value, operator), 'black')
            Publisher.sendMessage("scroll")
        else:
            return "Cannot filter: %s" % (self._edit_error)



    def filter_date(self, endDate, startDate):
        self._edit_service.filter_date(endDate, startDate)
        self.refresh_plot()
        if self._record:
            self._script("edit_service.filter_date(%s, %s)\n" % (repr(endDate), repr(startDate)), 'black')
            Publisher.sendMessage("scroll")
        else:
            return "Cannot filter: %s" % (self._edit_error)


    def data_gaps(self, value, time_period):

        self._edit_service.data_gaps(value, time_period)
        self.refresh_plot()
        if self._record:
            self._script("edit_service.data_gaps(%s, '%s')\n" % (value, time_period), 'black')
            Publisher.sendMessage("scroll")


    def value_change_threshold(self, value, operator):
        self._edit_service.value_change_threshold(value, operator)
        self.refresh_plot()
        if self._record:
            self._script("edit_service.value_change_threshold(%s,'%s')\n" % (value, operator), 'black')
            Publisher.sendMessage("scroll")


    def filter_from_previous(self, value):
        '''

        :param value: boolean
        :return:
        '''
        if self._edit_service._filter_from_selection is not value:
            self._edit_service.filter_from_previous(value)
            if self._record:
                self._script("edit_service.filter_from_previous(%s)\n" % value , 'black')
                Publisher.sendMessage("scroll")

    def get_toggle(self):
        '''

        :return: boolean
        '''
        return self._edit_service.get_toggle()


    def select_points_tf(self, tf_list):
        self._edit_service.select_points_tf(tf_list)
        self.refresh_plot()
        if self._record:
            self._script(
                "points = [\n\t{list}][0]\n".format(list=[x[2] for x in self._edit_service.get_filtered_points()]))
            self._script("edit_service.select_points(points)\n")
            Publisher.sendMessage("scroll")

    def select_points(self, id_list=[], datetime_list=[]):
        self._edit_service.select_points(id_list, datetime_list)
        self.refresh_plot()
        if self._record:
            self._script(
                "points = [\n\t{list}][0]\n".format(list=[x[2] for x in self._edit_service.get_filtered_points()]))
            self._script("edit_service.select_points({id}, points)\n".format(id=id_list))
            Publisher.sendMessage("scroll")
            #print self._edit_service.get_filtered_points()


    ###################
    # Editing
    ###################
    def add_points(self, points):
        self._edit_service.add_points(points)
        self.refresh_plot()
        #print points
        if self._record:
            self._script(
                "points = [\n\t{list}][0]\n".format(list=points))
            self._script("edit_service.add_points(points)\n")
            Publisher.sendMessage("scroll")

    def delete_points(self):
        self._edit_service.delete_points()
        self.refresh_plot()
        if self._record:
            self._script("edit_service.delete_points()\n", 'black')
            Publisher.sendMessage("scroll")


    def change_value(self, operator, value):
        self._edit_service.change_value(operator, value)
        self.refresh_plot()
        if self._record:
            self._script("edit_service.change_value(%s, '%s')\n" % (operator, value), 'black')
            Publisher.sendMessage("scroll")


    def interpolate(self):
        #print "Interpolate"
        self._edit_service.interpolate()
        self.refresh_plot()
        if self._record:
            self._script("edit_service.interpolate()\n", 'black')
            Publisher.sendMessage("scroll")


    def drift_correction(self, gap_width):
        ret = self._edit_service.drift_correction(gap_width)
        self.refresh_plot()
        if self._record:
            self._script("edit_service.drift_correction(%s)\n" % (gap_width), 'black')
            Publisher.sendMessage("scroll")

        return ret

    def reset_filter(self):
        self._edit_service.reset_filter()
        self.refresh_plot()
        if self._record:
            self._script("edit_service.reset_filter()\n", 'black')
            Publisher.sendMessage("scroll")


    def flag(self, qualifier_id):
        self._edit_service.flag(qualifier_id)
        self.refresh_plot()
        if self._record:
            self._script("edit_service.flag(%s)\n" % qualifier_id, 'black')
            Publisher.sendMessage("scroll")


    def restore(self):
        self._edit_service.restore()
        self.refresh_plot()
        if self._record:
            self._script("edit_service.restore()\n", 'black')
            Publisher.sendMessage("scroll")

    def saveFactory(self, var=None, method=None, qcl=None):
        """

        :param var:
        :param method:
        :param qcl:
        :param isSave:
        :return:
        """
        values = {}
        values['var'] = ("new_variable" if var else None)
        values['method'] = ("new_method" if method else None)
        values['qcl'] = ("new_qcl" if qcl else None)
        #values['override'] = override
        return values['var'], values['method'], values['qcl']#, values['isSave']

    # TODO Create save_as & save_existing
    def save(self, var=None, method=None, qcl=None):
        """

        :param var:
        :param method:
        :param qcl:
        :param override:
        :return:
        """
        result = self._edit_service.save()
        if self._record:
            self._script(
                "edit_service.save()\n" ,
                'black')
            #self._script("edit_service.save(%s, %s, %s, saveAs=%s)\n" % (var, method, qcl, isSave), 'black')
            Publisher.sendMessage("scroll")
        return result

    def save_as(self, var=None, method=None, qcl=None):
        """

        :param var:
        :param method:
        :param qcl:
        :param override:
        :return:
        """
        result = self._edit_service.save_as(var=var, method=method, qcl=qcl)
        if self._record:
            self._script(
                "edit_service.save_as(%s, %s, %s)\n" % (self.saveFactory(var, method, qcl)),
                'black')
            #self._script("edit_service.save(%s, %s, %s, saveAs=%s)\n" % (var, method, qcl, isSave), 'black')
            Publisher.sendMessage("scroll")
        return result

    def save_existing(self, var=None, method=None, qcl=None):
        """

        :param var:
        :param method:
        :param qcl:
        :param override:
        :return:
        """
        result = self._edit_service.save_existing(var=var, method=method, qcl=qcl)
        if self._record:
            self._script(
                "edit_service.save_existing(%s, %s, %s)\n" % (self.saveFactory(var, method, qcl)),
                'black')
            #self._script("edit_service.save(%s, %s, %s, saveAs=%s)\n" % (var, method, qcl, isSave), 'black')
            Publisher.sendMessage("scroll")
        if result:
            print "Save worked!"
        else:
            print "Save didn't work!"
        return result


    ###################
    # Gets
    ###################
    def get_series(self):
        return self._edit_service.get_series()

    def get_series_points(self):
        return self._edit_service.get_series_points()

    def get_filtered_points(self):
        return self._edit_service.get_filtered_points()

    def get_filter_list(self):
        return self._edit_service.get_filter_list()

    def get_filtered_dates(self):
        return self._edit_service.get_filtered_dates()

    def get_selection_groups(self):
        return self._edit_service.get_selection_groups()

    def get_qcl(self, q):
        qcl = self._edit_service.get_qcl(q.id)
        if self._record:
            self._script('new_qcl = series_service.get_qcl_by_id(%s)\n' % (qcl.id))
            Publisher.sendMessage("scroll")

        return qcl

    def get_method(self, m):
        method = self._edit_service.get_method(m.id)
        logger.debug("method: %s %s" % (type(method), method))
        if self._record:
            self._script('new_method = series_service.get_method_by_id(%s)\n' % (method.id))
            Publisher.sendMessage("scroll")

        return method

    def get_variable(self, v):
        var = self._edit_service.get_variable(v.id)
        if self._record:
            self._script('new_variable = series_service.get_variable_by_id(%s)\n' % (var.id))
            Publisher.sendMessage("scroll")

        return var


    def toggle_record(self):
        if self._record:
            self._record = False
        else:
            self._record = True

    ###################
    # Creates
    ###################
    def create_qcl(self, code, definition, explanation):
        qcl = self._edit_service.create_qcl(code, definition, explanation)
        if self._record:
            self._script('new_qcl = series_service.get_qcl_by_id(%s)\n' % (qcl.id))
            Publisher.sendMessage("scroll")

        return qcl

    def create_qualifer(self, code, description):


        cv_service = self.serv_man.get_cv_service()
        q = Qualifier()
        q.code = code
        q.description = description
        cv_service.create_qualifer(q)
        return q.id

    def create_method(self, m):
        method = self._edit_service.create_method(m.description, m.link)
        if self._record:
            self._script('new_method = series_service.get_method_by_id(%s)\n' % (method.id))
            Publisher.sendMessage("scroll")

        return method

    def create_variable(self, v):
        var = self._edit_service.create_variable(v.code, v.name, v.speciation, v.variable_unit_id, v.sample_medium,
                                                 v.value_type, v.is_regular, v.time_support, v.time_unit_id,
                                                 v.data_type, v.general_category, v.no_data_value)
        if self._record:
            self._script('new_variable = series_service.get_variable_by_id(%s)\n' % (var.id))
            Publisher.sendMessage("scroll")

        return var

    def write_header(self):
        self._script("#Uncomment the following commands when running outside ODMTools\n", 'black')
        self._script("#from odmtools.odmservices import EditService, SeriesService\n", 'black')
        self._script("#edit_service  = EditService(series_id={id}, connection_string='{con}')\n".format(
            id=self._edit_service._series_id, con=self._connection_string), 'black')
        self._script("#series_service = SeriesService(connection_string='%s')\n" % (self._connection_string), 'black')

        Publisher.sendMessage("scroll")


 ###############
# Export methods
###############
    def export_series_data(self, series_id, filename):

        export_service = self.serv_man.get_export_service()
        export_service.export_series_data(series_id, filename, True, True, True, True, True, True, True)


    def export_series_metadata(self, series_id, filename):

        export_service = self.serv_man.get_export_service()
        export_service.export_series_metadata(series_id, filename)



###############
# UI methods
###############
    def refresh_plot(self):
        Publisher.sendMessage("updateValues", event=None)
        Publisher.sendMessage("changePlotSelection", sellist=[], datetime_list=self.get_filtered_dates())
        Publisher.sendMessage("changeTableSelection", sellist=[], datetime_list=self.get_filtered_dates())
