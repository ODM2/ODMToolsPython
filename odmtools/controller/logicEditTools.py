import logging
import pandas as pd
import timeit
from wx.lib.pubsub import pub as Publisher
from odmtools.common.logger import LoggerTool


# tool = LoggerTool()
# logger = tool.setupLogger(__name__, __name__ + '.log', 'w', logging.DEBUG)
logger =logging.getLogger('main')

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
        return self._edit_service.memDB.series_service


    # ##################
    # Filters
    ###################
    def filter_value(self, value, operator):
        self._edit_service.filter_value(value, operator)
        self.refresh_selection()
        if self._record:
            self._script("edit_service.filter_value(%s, '%s')\n" % (value, operator), 'black')
            Publisher.sendMessage("scroll")
        else:
            return "Cannot filter: %s" % (self._edit_error)

    def filter_date(self, endDate, startDate):
        self._edit_service.filter_date(endDate, startDate)
        self.refresh_selection()
        if self._record:
            self._script("edit_service.filter_date(%s, %s)\n" % (repr(endDate), repr(startDate)), 'black')
            Publisher.sendMessage("scroll")
        else:
            return "Cannot filter: %s" % (self._edit_error)

    def data_gaps(self, value, time_period):
        self._edit_service.data_gaps(value, time_period)
        self.refresh_selection()
        if self._record:
            self._script("edit_service.data_gaps(%s, '%s')\n" % (value, time_period), 'black')
            Publisher.sendMessage("scroll")


    def value_change_threshold(self, value, operator):
        self._edit_service.change_value_threshold(value, operator)
        self.refresh_selection()
        if self._record:
            self._script("edit_service.change_value_threshold(%s,'%s')\n" % (value, operator), 'black')
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
        self.refresh_selection()
        if self._record:
            self._script(
                "points = [\n\t{list}][0]\n".format(list=[x[2] for x in self._edit_service.get_filtered_points()]))
            self._script("edit_service.select_points(points)\n")
            Publisher.sendMessage("scroll")

    def _list2dataframestub(self, datetime_list):
        result = None
        if isinstance(datetime_list, list):
            result = pd.DataFrame(datetime_list)

        return result
        #elif isinstance(datetime_list, pd.DataFrame):
        #    result = datetime_list.


    def _dataframe2liststub(self, dataframe):
        result = None
        if isinstance(dataframe, pd.DataFrame):
            result = pd.DataFrame()


        ## return dataframe

    def select_points(self, id_list=[], dataframe=[]):
        """

        :param id_list:
        :param dataframe:
        :return:
        """

        """ Handle list to dataframe conversion """
        if isinstance(dataframe, list):
            dataframe = self._edit_service.datetime2dataframe(dataframe)
            #df = self._edit_list2dataframestub(datetime_list)
        self._edit_service.select_points(dataframe=dataframe)
        self.refresh_selection()

        if self._record:
            selectedpoints = self._edit_service.selectPointsStub()
            self._script("points = [\n\t{list}][0]\n".format(list=selectedpoints))
            self._script("edit_service.select_points({id}, points)\n".format(id=id_list))
            Publisher.sendMessage("scroll")
            #print self._edit_service.get_filtered_points()


    ###################
    # Editing
    ###################
    def _create_dataframe(self, points):
        return pd.DataFrame(points)

    def add_points(self, points):
        self._edit_service.add_points(points)
        self.refresh_edit()

        if self._record:
            self._script(
                "points = [\n\t{list}][0]\n".format(list=points))
            self._script("edit_service.add_points(points)\n")
            Publisher.sendMessage("scroll")

    def delete_points(self):
        self._edit_service.delete_points()
        self.refresh_edit()
        if self._record:
            self._script("edit_service.delete_points()\n", 'black')
            Publisher.sendMessage("scroll")

    def change_value(self, operator, value):
        self._edit_service.change_value(operator, value)
        self.refresh_edit()
        if self._record:
            self._script("edit_service.change_value(%s, '%s')\n" % (operator, value), 'black')
            Publisher.sendMessage("scroll")

    def interpolate(self):
        #print "Interpolate"
        self._edit_service.interpolate()
        self.refresh_edit()
        self.refresh_selection()

        if self._record:
            self._script("edit_service.interpolate()\n", 'black')
            Publisher.sendMessage("scroll")


    def drift_correction(self, gap_width):
        ret = self._edit_service.drift_correction(gap_width)
        self.refresh_edit()
        if self._record:
            self._script("edit_service.drift_correction(%s)\n" % (gap_width), 'black')
            Publisher.sendMessage("scroll")
        return ret

    def reset_filter(self):
        self._edit_service.reset_filter()
        self.refresh_selection()
        if self._record:
            self._script("edit_service.reset_filter()\n", 'black')
            Publisher.sendMessage("scroll")


    def flag(self, qualifier_id):
        self._edit_service.flag(qualifier_id)
        self.refresh_edit()
        if self._record:
            self._script("edit_service.flag(%s)\n" % qualifier_id, 'black')
            Publisher.sendMessage("scroll")

    def restore(self):
        self._edit_service.restore()
        self.refresh_edit()
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
                "edit_service.save()\n",
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

    def save_appending(self, var = None, method =None, qcl = None, overwrite = False):
        """

        :param var:
        :param method:
        :param qcl:
        :param override:
        :return:
        """
        result = self._edit_service.save_appending(var=var, method=method, qcl=qcl, overwrite= overwrite)
        if result:
            print "Save worked!"

            if self._record:

                self._script(
                    "edit_service.save_appending(%s, %s, %s, " % self.saveFactory(var, method, qcl)+str(overwrite )+")\n",
                    'black')
                #self._script("edit_service.save(%s, %s, %s, saveAs=%s)\n" % (var, method, qcl, isSave), 'black')
                Publisher.sendMessage("scroll")

        else:
            print "Save didn't work!"
            #self._edit_service.restore()
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
        if result:
            print "Save worked!"

            if self._record:

                self._script(
                    "edit_service.save_existing(%s, %s, %s)\n" % (self.saveFactory(var, method, qcl)),
                    'black')
                #self._script("edit_service.save(%s, %s, %s, saveAs=%s)\n" % (var, method, qcl, isSave), 'black')
                Publisher.sendMessage("scroll")

        else:
            print "Save didn't work!"
            #self._edit_service.restore()
        return result


    ###################
    # Gets
    ###################
    def get_series(self):
        return self._edit_service.get_series()

    def get_series_points(self):
        return self._edit_service.get_series_points_df()

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


    def toggle_record(self, value):
        self._record = value
        '''
        if self._record:
            self._record = False
        else:
            self._record = True
        '''

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
        qual = self._edit_service.create_annotation(code, description)
        if self._record:
            self._script('new_qual = series_service.get_qualifier_by_code(%s)\n' % (qual.code))
            Publisher.sendMessage("scroll")

        return qual

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



#TODO function to send in a list of datavalues  or tuple objects with the id and datavalues together
#TODO function to send in a function to apply to the selected datavalues




###############
# UI methods
###############
    def refresh_edit(self):
        start_time = timeit.default_timer()
        Publisher.sendMessage("updateValues", event=None)
        elapsed_time = timeit.default_timer() - start_time
        logger.debug("UpdateValues took: %s seconds" % elapsed_time)

        self.refresh_selection()

    def refresh_selection(self):
        start_time = timeit.default_timer()
        Publisher.sendMessage("changePlotSelection",  datetime_list=self.get_filtered_dates())
        elapsed_time = timeit.default_timer() - start_time
        logger.debug("Change Plot Selection: %s seconds" % elapsed_time)

        start_time = timeit.default_timer()
        Publisher.sendMessage("changeTableSelection",  datetime_list=self.get_filtered_dates())
        elapsed_time = timeit.default_timer() - start_time
        logger.debug("Change table took: %s seconds" % elapsed_time)

