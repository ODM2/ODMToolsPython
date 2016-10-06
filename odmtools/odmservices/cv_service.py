# CV imports
from odmtools.odmdata import SessionFactory
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
from odm2api.ODM2.services.readService import ReadODM2


class CVService(): # Rename to ReadService
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
        result = self._edit_session.query(Sample).order_by(Sample.lab_sample_code).all()
        return result

    def get_site_type_cvs(self):
        result = self._edit_session.query(SiteTypeCV).order_by(SiteTypeCV.term).all()
        return result

    def get_variable_name_cvs(self):
        result = self._edit_session.query(VariableNameCV).order_by(VariableNameCV.term).all()
        return result

    def get_offset_type_cvs(self):
        result = self._edit_session.query(OffsetType).order_by(OffsetType.id).all()
        return result

    def get_speciation_cvs(self):
        result = self._edit_session.query(SpeciationCV).order_by(SpeciationCV.term).all()
        return result
        # return self.read_service.getCVs(type="Speciation") # Returns Error running Query,

    def get_sample_medium_cvs(self):
        result = self._edit_session.query(SampleMediumCV).order_by(SampleMediumCV.term).all()
        return result

    def get_value_type_cvs(self):
        result = self._edit_session.query(ValueTypeCV).order_by(ValueTypeCV.term).all()
        return result

    def get_data_type_cvs(self):
        result = self._edit_session.query(DataTypeCV).order_by(DataTypeCV.term).all()
        return result

    def get_general_category_cvs(self):
        result = self._edit_session.query(GeneralCategoryCV).order_by(GeneralCategoryCV.term).all()
        return result

    def get_censor_code_cvs(self):
        result = self._edit_session.query(CensorCodeCV).order_by(CensorCodeCV.term).all()
        return result

    def get_sample_type_cvs(self):
        result = self._edit_session.query(SampleTypeCV).order_by(SampleTypeCV.term).all()
        return result

    def get_units(self):
        result = self._edit_session.query(Unit).all()
        return result

    def get_units_not_uni(self):
        result = self._edit_session.query(Unit).filter(not_(Unit.name.contains('angstrom'))).all()
        return result

    def get_units_names(self):
        result = self._edit_session.query(Unit.name).all()
        return result

    # return a single cv
    def get_unit_by_name(self, unit_name):
        result = self._edit_session.query(Unit).filter_by(name=unit_name).first()
        return result

    def get_unit_by_id(self, unit_id):
        result = self._edit_session.query(Unit).filter_by(id=unit_id).first()
        return result

    def get_annotation_by_code(self, code):
        self.read_service.getAnnotations(type=code)
        return

    def get_all_annotations(self):
        return self.read_service.getAnnotations(type=None)

