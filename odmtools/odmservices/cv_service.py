# CV imports
# from odmtools.odmdata import SessionFactory
from odmtools.odmdata import VerticalDatumCV
from odmtools.odmdata import SiteTypeCV
from odmtools.odmdata import VariableNameCV
from odmtools.odmdata import SpeciationCV
from odmtools.odmdata import SampleMediumCV
from odmtools.odmdata import ValueTypeCV
from odmtools.odmdata import DataTypeCV
from odmtools.odmdata import GeneralCategoryCV
from odmtools.odmdata import CensorCodeCV
from odmtools.odmdata import TopicCategoryCV
from odmtools.odmdata import SampleTypeCV
from odmtools.odmdata import OffsetType
from odmtools.odmdata import Sample
from odmtools.odmdata import Qualifier
from odmtools.odmdata import Unit
from sqlalchemy import not_
from odm2api.ODMconnection import SessionFactory
from odm2api.ODM2.services.readService import ReadODM2


class CVService():  # change to readSerivice()
    # Accepts a string for creating a SessionFactory, default uses odmdata/connection.cfg
    def __init__(self, connection_string="", debug=False):
        self._session_factory = SessionFactory(connection_string=connection_string, echo=debug)
        self._edit_session = self._session_factory.getSession()
        self._debug = debug
        self.read_service = ReadODM2(session_factory=self._session_factory, debug=self._debug)

    # Controlled Vocabulary get methods

    # From ODM1 -> ODM2 Qualifier was changed to Annotations
    def get_annotations(self, type):
        return self.read_service.getAnnotations(type=type)

    def get_censor_code_cvs(self):
        result = self._edit_session.query(CensorCodeCV).order_by(CensorCodeCV.term).all()
        return result

    def get_data_type_cvs(self):
        result = self._edit_session.query(DataTypeCV).order_by(DataTypeCV.term).all()
        return result

    def get_general_category_cvs(self):
        result = self._edit_session.query(GeneralCategoryCV).order_by(GeneralCategoryCV.term).all()
        return result

    def get_offset_type_cvs(self):
        return self.read_service.getCVs(type="Spatial Offset Type")

    # From ODM1 -> ODM2 Quality Controlled Level was changed to Processing Level
    def get_all_processing_levels(self):
        self.read_service.getProcessingLevels()

    def get_all_method(self): # Rename to get_method_all
        return self.read_service.getMethods(ids=None, codes=None, type=None)

    def get_method_by_id(self, method_id):
        return self.read_service.getMethods(ids=method_id)

    def get_method_by_description(self, code):
        return self.read_service.getMethods(codes=code)

    def get_processing_level_by_id(self, id):
        self.read_service.getProcessingLevels(ids=id)

    def get_processing_level_by_code(self, code):
        self.read_service.getProcessingLevels(codes=code)

    def get_samples(self):
        result = self._edit_session.query(Sample).order_by(Sample.lab_sample_code).all()
        return result

    def get_sample_medium_cvs(self):
        return  self.read_service.getCVs(type="Medium")

    def get_site_type_cvs(self):
        return self.read_service.getCVs(type="Site Type")

    def get_speciation_cvs(self):
        return self.read_service.getCVs(type="Speciation")

    def get_sample_type_cvs(self):
        result = self._edit_session.query(SampleTypeCV).order_by(SampleTypeCV.term).all()
        return result

    # From ODM1 -> ODM2 Site was changed to Sampling Feature
    def get_all_sites(self):
        return self.read_service.getSamplingFeatures(ids=None, codes=None, uuids=None, type=None, wkt=None)

    def get_site_by_id(self, site_id):
        return self.read_service.getSamplingFeatures(ids=site_id)

    def get_timeseries_result_values(self, type):
        return self.read_service.getAnnotations(type=type)

    def get_units(self):
        self.read_service.getUnits(ids=None, name=None, type=None)

    def get_units_not_uni(self):
        result = self._edit_session.query(Unit).filter(not_(Unit.name.contains('angstrom'))).all()
        return result

    def get_units_names(self):
        result = self._edit_session.query(Unit.name).all()
        return result

    # return a single cv
    def get_unit_by_name(self, unit_name):
        return self.read_service.getUnits(name=unit_name)

    def get_unit_by_id(self, unit_id):
        return self.read_service.getUnits(ids=unit_id)

    def get_value_type_cvs(self):
        result = self._edit_session.query(ValueTypeCV).order_by(ValueTypeCV.term).all()
        return result

    def get_variable_name_cvs(self):
        return self.read_service.getCVs(type="Variable Name")

    def get_vertical_datum_cvs(self):
        return self.read_service.getCVs("Elevation Datum")

    def get_all_variables(self):
        return self.read_service.getVariables()

    def get_variable_by_id(self, id):
        return self.read_service.getVariables(ids=id)

    def get_variable_by_code(self, code):
        return self.read_service.getVariables(codes=code)





