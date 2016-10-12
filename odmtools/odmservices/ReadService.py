from odmtools.odmdata import SessionFactory
from odmtools.odmdata import VerticalDatumCV
from odmtools.odmdata import ValueTypeCV
from odmtools.odmdata import GeneralCategoryCV
from odmtools.odmdata import Unit
from sqlalchemy import not_
from odm2api.ODM2.services.readService import ReadODM2


class ReadService:
    # Accepts a string for creating a SessionFactory, default uses odmdata/connection.cfg
    def __init__(self, connection_string="", debug=False):
        self._session_factory = SessionFactory(connection_string, debug)
        self._edit_session = self._session_factory.getSession()
        self._debug = debug
        self.read_service = ReadODM2(self._session_factory, debug=self._debug)

    # Controlled Vocabulary get methods
    #return a list of all terms in the cv
    def get_vertical_datum_cvs(self):
        result = self._edit_session.query(VerticalDatumCV).order_by(VerticalDatumCV.term).all()
        return result

    def get_samples(self):
        return self.read_service.getSamplingFeatures(ids=None, codes=None, uuids=None, type=None, wkt=None)

    def get_site_type_cvs(self):
        return self.read_service.getCVs(type="Site Type")  # OR return self.read_service.getCVs(type="Sampling Feature Type")

    def get_variable_name_cvs(self):
        return self.read_service.getCVs(type="Variable Name")

    def get_offset_type_cvs(self):
        return self.read_service.getCVs(type="Spatial Offset Type")

    def get_speciation_cvs(self):
        return self.read_service.getCVs(type="Speciation")

    def get_sample_medium_cvs(self):
        return self.read_service.getCVs(type="Medium")

    def get_value_type_cvs(self):
        result = self._edit_session.query(ValueTypeCV).order_by(ValueTypeCV.term).all()
        return result

    def get_data_type_cvs(self):
        return self.read_service.getCVs(type="dataset type")

    def get_general_category_cvs(self):
        result = self._edit_session.query(GeneralCategoryCV).order_by(GeneralCategoryCV.term).all()
        return result

    def get_censor_code_cvs(self):
        return self.read_service.getCVs(type="censorcode")

    def get_sample_type_cvs(self):
        return self.read_service.getCVs(type="Sampling Feature Type")

    def get_units(self):
        return self.read_service.getUnits(ids=None, name=None, type=None)

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

    def get_annotation_by_code(self, code):
        return self.read_service.getAnnotations(type=code)

    def get_all_annotations(self):
        return self.read_service.getAnnotations(type=None)

