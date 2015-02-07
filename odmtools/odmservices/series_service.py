import logging

import wx
from sqlalchemy import distinct
from odmtools.odmdata import SessionFactory
from odmtools.odmdata import Site
from odmtools.odmdata import Variable
from odmtools.odmdata import Unit
from odmtools.odmdata import Series
from odmtools.odmdata import DataValue
from odmtools.odmdata import Qualifier
from odmtools.odmdata import OffsetType
from odmtools.odmdata import Sample
from odmtools.odmdata import Method
from odmtools.odmdata import QualityControlLevel
from odmtools.odmdata import ODMVersion
from odmtools.common.logger import LoggerTool

tool = LoggerTool()
logger = tool.setupLogger(__name__, __name__ + '.log', 'w', logging.DEBUG)


class SeriesService():
    # Accepts a string for creating a SessionFactory, default uses odmdata/connection.cfg
    def __init__(self, connection_string="", debug=False):
        self._session_factory = SessionFactory(connection_string, debug)
        self._edit_session = self._session_factory.get_session()
        self._debug = debug




    def get_db_version(self):
        return self._edit_session.query(ODMVersion).first().version_number

    # Site methods
    def get_all_sites(self):
        return self._edit_session.query(Site).order_by(Site.code).all()

    def get_all_used_sites(self):

        try:
            site_ids = [x[0] for x in self._edit_session.query(distinct(Series.site_id)).all()]
        except:
            site_ids = None

        if not site_ids:
            return None

        Sites = []
        for site_id in site_ids:
            Sites.append(self._edit_session.query(Site).filter_by(id=site_id).first())

        return Sites


    def get_site_by_id(self, site_id):
        try:
            return self._edit_session.query(Site).filter_by(id=site_id).first()
        except:
            return None

    # Variables methods
    def get_all_used_variables(self):
        #get list of used variable ids
        try:
            var_ids = [x[0] for x in self._edit_session.query(distinct(Series.variable_id)).all()]
        except:
            var_ids = None

        Variables = []

        #create list of variables from the list of ids
        for var_id in var_ids:
            Variables.append(self._edit_session.query(Variable).filter_by(id=var_id).first())

        return Variables

    def get_all_variables(self):
        return self._edit_session.query(Variable).all()

    def get_variable_by_id(self, variable_id):
        try:
            return self._edit_session.query(Variable).filter_by(id=variable_id).first()
        except:
            return None

    def get_variable_by_code(self, variable_code):
        try:
            return self._edit_session.query(Variable).filter_by(code=variable_code).first()
        except:
            return None

    def get_variables_by_site_code(self, site_code):  # covers NoDV, VarUnits, TimeUnits
        try:
            var_ids = [x[0] for x in self._edit_session.query(distinct(Series.variable_id)).filter_by(
                site_code=site_code).all()]
        except:
            var_ids = None

        variables = []
        for var_id in var_ids:
            variables.append(self._edit_session.query(Variable).filter_by(id=var_id).first())

        return variables

    # Unit methods
    def get_all_units(self):
        return self._edit_session.query(Unit).all()

    def get_unit_by_name(self, unit_name):
        try:
            return self._edit_session.query(Unit).filter_by(name=unit_name).first()
        except:
            return None

    def get_unit_by_id(self, unit_id):
        try:
            return self._edit_session.query(Unit).filter_by(id=unit_id).first()
        except:
            return None

    def get_offset_types_by_series_id(self, series_id):
        subquery = self._edit_session.query(DataValue.offset_type_id).outerjoin(
            Series.data_values).filter(Series.id == series_id, DataValue.offset_type_id != None).distinct().subquery()
        return self._edit_session.query(OffsetType).join(subquery).distinct().all()

    def get_qualifiers_by_series_id(self, series_id):
        subquery = self._edit_session.query(DataValue.qualifier_id).outerjoin(
            Series.data_values).filter(Series.id == series_id, DataValue.qualifier_id != None).distinct().subquery()
        return self._edit_session.query(Qualifier).join(subquery).distinct().all()

    def get_samples_by_series_id(self, series_id):
        subquery = self._edit_session.query(DataValue.sample_id).outerjoin(
            Series.data_values).filter(Series.id == series_id, DataValue.sample_id != None).distinct().subquery()
        return self._edit_session.query(Sample).join(subquery).distinct().all()

    # Series Catalog methods
    def get_all_series(self):
        """Returns all series as a modelObject"""
        #logger.debug("%s" % self._edit_session.query(Series).order_by(Series.id).all())
        return self._edit_session.query(Series).order_by(Series.id).all()

    def reset_session(self):
        self._edit_session = self._session_factory.get_session()  # Reset the session in order to prevent memory leaks

    def get_series_by_site(self , site_id):
        try:
            selectedSeries = self._edit_session.query(Series).filter_by(site_id=site_id).order_by(Series.id).all()
            return selectedSeries
        except:
            return None

    def get_series_by_id(self, series_id):
        try:
            selectedSeries = self._edit_session.query(Series).filter_by(id=series_id).order_by(Series.id).first()
            return selectedSeries
        except:
            return None

    def get_series_by_id_quint(self, site_id, var_id, method_id, source_id, qcl_id):
        try:
            return self._edit_session.query(Series).filter_by(
                site_id=site_id, variable_id=var_id, method_id=method_id,
                source_id=source_id, quality_control_level_id=qcl_id).first()
        except:
            return None

    def get_series_from_filter(self):
        # Pass in probably a Series object, match it against the database
        pass


    def save_series(self, series):
        """ Save to an Existing Series
        :param series:
        :param data_values:
        :return:
        """

        if self.does_exist(series):
            self._edit_session.add(series)
            self._edit_session.add_all(series.data_values)
            self._edit_session.commit()
            logger.debug("Existing File was overwritten with new information")
            return True
        else:
            logger.debug("There wasn't an existing file to overwrite, please select 'Save As' first")
            # there wasn't an existing file to overwrite
            raise Exception("Series does not exist, unable to save. Please select 'Save As'")

    def save_new_series(self, series):
        """ Create as a new catalog entry
        :param series:
        :param data_values:
        :return:
        """
        # Save As case
        if self.does_exist(series):
            msg = "There is already an existing file with this information. Please select 'Save' or 'Save Existing' to overwrite"
            logger.debug(msg)
            raise Exception(msg)
        else:
            self._edit_session.add(series)
            self._edit_session.add_all(series.data_values)
            self._edit_session.commit()
        logger.debug("A new series was added to the database")
        return True

    def does_exist(self, series):
        return self.series_exists(
            series.site_id,
            series.variable_id,
            series.method_id,
            series.source_id,
            series.quality_control_level_id
        )

    def series_exists(self, site_id, var_id, method_id, source_id, qcl_id):
        try:
            result = self._edit_session.query(Series).filter_by(
                site_id=site_id,
                variable_id=var_id,
                method_id=method_id,
                source_id=source_id,
                quality_control_level_id=qcl_id
            ).one()

            return True
        except:
            return False

    def get_data_value_by_id(self, id):
        try:
            return self._edit_session.query(DataValue).filter_by(id=id).first()
        except:
            return None

    def get_all_qcls(self):
        return self._edit_session.query(QualityControlLevel).all()

    def get_qcl_by_id(self, qcl_id):
        try:
            return self._edit_session.query(QualityControlLevel).filter_by(id=qcl_id).first()
        except:
            return None

    def get_qcl_by_code(self, qcl_code):
        try:
            return self._edit_session.query(QualityControlLevel).filter_by(code=qcl_code).first()
        except:
            return None

    # Method methods
    def get_all_methods(self):
        return self._edit_session.query(Method).all()

    def get_method_by_id(self, method_id):
        try:
            result = self._edit_session.query(Method).filter_by(id=method_id).first()
        except:
            result = None
        return result

    def get_method_by_description(self, method_code):
        try:
            result = self._edit_session.query(Method).filter_by(description=method_code).first()
        except:
            result = None
        return result

    # Edit/delete methods
    def delete_dvs(self, dv_list):
        dlg = wx.ProgressDialog("Delete Progress", "Deleting %s values" % len(dv_list), maximum=len(dv_list),
                                parent=None,
                                style=0 | wx.PD_APP_MODAL | wx.PD_ELAPSED_TIME |
                                      wx.PD_ESTIMATED_TIME | wx.PD_REMAINING_TIME | wx.PD_AUTO_HIDE)
        length = len(dv_list)
        for i, dv in enumerate(dv_list):
            dlg.Update(i, "%s/%s Objects Deleted" % (i, length))
            merged_dv = self._edit_session.merge(dv)
            self._edit_session.delete(merged_dv)
        dlg.Update(length, "Commiting to database")
        self._edit_session.commit()
        dlg.Destroy()

    def delete_values_by_series(self, series):
        try:
            return self._edit_session.query(DataValue).filter_by(site_id = series.site_id,
                                                                 variable_id = series.variable_id,
                                                                 method_id = series.method_id,
                                                                 source_id = series.source_id,
                                                                 quality_control_level_id = series.quality_control_level_id).delete()
        except:
            return None

    def update_dvs(self, dv_list):
        merged_dv_list = map(self._edit_session.merge, dv_list)
        self._edit_session.add_all(merged_dv_list)
        self._edit_session.commit()

    def create_new_series(self, data_values, site_id, variable_id, method_id, source_id, qcl_id):
        self.update_dvs(data_values)
        series = Series()
        series.site_id = site_id
        series.variable_id = variable_id
        series.method_id = method_id
        series.source_id = source_id
        series.quality_control_level_id = qcl_id

        self._edit_session.add(series)
        self._edit_session.commit()
        return series

    def update_series(self, series):
        merged_series = self._edit_session.merge(series)
        self._edit_session.add(merged_series)
        self._edit_session.commit()

    def create_method(self, description, link):
        meth = Method()
        meth.description = description
        if link is not None:
            meth.link = link

        self._edit_session.add(meth)
        self._edit_session.commit()
        return meth

    def create_variable_by_var(self, var):
        try:
            self._edit_session.add(var)
            self._edit_session.commit()
            return var
        except:
            return None

    def create_variable(
            self, code, name, speciation, variable_unit_id, sample_medium,
            value_type, is_regular, time_support, time_unit_id, data_type,
            general_category, no_data_value):
        var = Variable()
        var.code = code
        var.name = name
        var.speciation = speciation
        var.variable_unit_id = variable_unit_id
        var.sample_medium = sample_medium
        var.value_type = value_type
        var.is_regular = is_regular
        var.time_support = time_support
        var.time_unit_id = time_unit_id
        var.data_type = data_type
        var.general_category = general_category
        var.no_data_value = no_data_value

        self._edit_session.add(var)
        self._edit_session.commit()
        return var

    def create_qcl(self, code, definition, explanation):
        qcl = QualityControlLevel()
        qcl.code = code
        qcl.definition = definition
        qcl.explanation = explanation

        self._edit_session.add(qcl)
        self._edit_session.commit()
        return qcl

    def delete_series(self, series):
        self.delete_dvs(series.data_values)

        delete_series = self._edit_session.merge(series)
        self._edit_session.delete(delete_series)
        self._edit_session.commit()

    def qcl_exists(self, q):
        try:
            result = self._edit_session.query(QualityControlLevel).filter_by(code=q.code, definition=q.definition).one()
            return True
        except:

            return False

    def method_exists(self, m):
        try:
            result = self._edit_session.query(Method).filter_by(description=m.description).one()
            return True
        except:
            return False

    def variable_exists(self, v):
        try:
            result = self._edit_session.query(Variable).filter_by(code=v.code,
                                                                  name=v.name, speciation=v.speciation,
                                                                  variable_unit_id=v.variable_unit_id,
                                                                  sample_medium=v.sample_medium,
                                                                  value_type=v.value_type, is_regular=v.is_regular,
                                                                  time_support=v.time_support,
                                                                  time_unit_id=v.time_unit_id, data_type=v.data_type,
                                                                  general_category=v.general_category,
                                                                  no_data_value=v.no_data_value).one()
            return result
        except:
            return None