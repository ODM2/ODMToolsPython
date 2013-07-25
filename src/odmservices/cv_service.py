# CV imports
from odmdata.session_factory import SessionFactory
from odmdata.vertical_datum_cv import VerticalDatumCV
from odmdata.site_type_cv import SiteTypeCV
from odmdata.variable_name_cv import VariableNameCV
from odmdata.speciation_cv import SpeciationCV
from odmdata.sample_medium_cv import SampleMediumCV
from odmdata.value_type_cv import ValueTypeCV
from odmdata.data_type_cv import DataTypeCV
from odmdata.general_category_cv import GeneralCategoryCV
from odmdata.censor_code_cv import CensorCodeCV
from odmdata.topic_category_cv import TopicCategoryCV
from odmdata.sample_type_cv import SampleTypeCV
from odmdata.offset_type import OffsetType
# from odmdata.lab_method import LabMethod
from odmdata.sample import Sample
from odmdata.qualifier import Qualifier
from odmdata.unit import Unit


class CVService():
	# Accepts a string for creating a SessionFactory, default uses odmdata/connection.cfg
	def __init__(self, connection_string="", debug=False):
		self._session_factory = SessionFactory(connection_string, debug)
		self._edit_session = self._session_factory.get_session()
		self._debug = debug

		# getverdcv

	# Controlled Vocabulary get methods
	def get_vertical_datum_cvs(self):
		session = self._session_factory.get_session()
		result = session.query(VerticalDatumCV).order_by(VerticalDatumCV.term).all()
		session.close()
		return result

	def get_lab_methods(self):
		session = self._session_factory.get_session()
		result = session.query(Sample).order_by(Sample.lab_sample_code).all()
		session.close()
		return result

	def get_qualifiers(self):
		session = self._session_factory.get_session()
		result = session.query(Qualifier).order_by(Qualifier.code).all()
		session.close()
		return result

	def create_qualifier(self, qualifier):
		session = self._session_factory.get_session()
		session.add(qualifier)

		session.commit()

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

	def get_units(self):
		session = self._session_factory.get_session()
		result =  self._edit_session.query(Unit).all()
		session.close()
		return result


