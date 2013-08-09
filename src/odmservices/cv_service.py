# CV imports
from odmdata import SessionFactory
from odmdata import VerticalDatumCV
from odmdata import SiteTypeCV
from odmdata import VariableNameCV
from odmdata import SpeciationCV
from odmdata import SampleMediumCV
from odmdata import ValueTypeCV
from odmdata import DataTypeCV
from odmdata import GeneralCategoryCV
from odmdata import CensorCodeCV
from odmdata import TopicCategoryCV
from odmdata import SampleTypeCV
from odmdata import OffsetType
from odmdata import Sample
from odmdata import Qualifier
from odmdata import Unit


class CVService():
	# Accepts a string for creating a SessionFactory, default uses odmdata/connection.cfg
	def __init__(self, connection_string="", debug=False):
		self._session_factory = SessionFactory(connection_string, debug)
		self._edit_session = self._session_factory.get_session()
		self._debug = debug

	# Controlled Vocabulary get methods
	def get_vertical_datum_cvs(self):
		session = self._session_factory.get_session()
		result = session.query(VerticalDatumCV).order_by(VerticalDatumCV.term).all()
		session.close()
		return result

	def get_samples(self):
		session = self._session_factory.get_session()
		result = session.query(Sample).order_by(Sample.lab_sample_code).all()
		session.close()
		return result

	def get_qualifiers(self):
		result = self._edit_session.query(Qualifier).order_by(Qualifier.code).all()
		return result

	def create_qualifier(self, qualifier):
		session = self._session_factory.get_session()
		self._edit_session.add(qualifier)

		self._edit_session.commit()

	def get_site_type_cvs(self):
		session = self._session_factory.get_session()
		result = session.query(SiteTypeCV).order_by(SiteTypeCV.term).all()
		session.close()
		return result

	def get_variable_name_cvs(self):
		session = self._session_factory.get_session()
		result = session.query(VariableNameCV).order_by(VariableNameCV.term).all()
		session.close()
		return result

	def get_offset_type_cvs(self):
		session = self._session_factory.get_session()
		result = session.query(OffsetType).order_by(OffsetType.id).all()
		session.close()
		return result

	def get_speciation_cvs(self):
		session = self._session_factory.get_session()
		result = session.query(SpeciationCV).order_by(SpeciationCV.term).all()
		session.close()
		return result

	def get_sample_medium_cvs(self):
		session = self._session_factory.get_session()
		result = session.query(SampleMediumCV).order_by(SampleMediumCV.term).all()
		session.close()
		return result

	def get_value_type_cvs(self):
		session = self._session_factory.get_session()
		result = session.query(ValueTypeCV).order_by(ValueTypeCV.term).all()
		session.close()
		return result

	def get_data_type_cvs(self):
		session = self._session_factory.get_session()
		result = session.query(DataTypeCV).order_by(DataTypeCV.term).all()
		session.close()
		return result

	def get_general_category_cvs(self):
		session = self._session_factory.get_session()
		result = session.query(GeneralCategoryCV).order_by(GeneralCategoryCV.term).all()
		session.close()
		return result

	def get_censor_code_cvs(self):
		session = self._session_factory.get_session()
		result = session.query(CensorCodeCV).order_by(CensorCodeCV.term).all()
		session.close()
		return result

	def get_sample_type_cvs(self):
		session = self._session_factory.get_session()
		result = session.query(SampleTypeCV).order_by(SampleTypeCV.term).all()
		session.close()
		return result

	def get_units(self):
		session = self._session_factory.get_session()
		result =  self._edit_session.query(Unit).all()
		session.close()
		return result

	def get_unit_by_name(self, unit_name):
		session = self._session_factory.get_session()
		result =  self._edit_session.query(Unit).filter_by(name=unit_name).one()
		session.close()
		return result

	def get_unit_by_id(self, unit_id):
		session = self._session_factory.get_session()
		result =  self._edit_session.query(Unit).filter_by(id=unit_id).one()
		session.close()
		return result
