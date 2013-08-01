import pytest
import sqlalchemy.orm.exc

from odmservices import CVService

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
from odmdata import LabMethod
from odmdata import Sample
from odmdata import Qualifier
from odmdata import Unit

from odmtests import build_db

session = None

class TestCVService:
	def setup(self):
		self.connection_string = "sqlite:///:memory:"
		self.cv_service = CVService(self.connection_string, debug=False)
		self.session = self.cv_service._session_factory.get_session()
		engine = self.cv_service._session_factory.engine
		build_db(engine)

	def test_get_vertical_datum_cvs(self):
		assert self.cv_service.get_vertical_datum_cvs() == []

		vert_dat = self._add_vertical_datum_cv()
		db_vert_dat = self.cv_service.get_vertical_datum_cvs()[0]
		assert vert_dat.term == db_vert_dat.term

	def test_get_samples(self):
		assert self.cv_service.get_samples() == []

		lab_method = self._add_lab_method()
		sample = self._add_sample(lab_method.id)

		db_sample = self.cv_service.get_samples()[0]
		assert sample.id == db_sample.id
		assert sample.lab_method_id == db_sample.lab_method_id

	def test_create_qualifier(self):
		qual = Qualifier()
		qual.code = "ABC123"
		qual.description = "This is a test"
		self.cv_service.create_qualifier(qual)

		assert qual.id is not None

	def test_get_qualifiers(self):
		assert self.cv_service.get_qualifiers() == []

		qual = Qualifier()
		qual.code = "ABC123"
		qual.description = "This is a test"
		self.cv_service.create_qualifier(qual)

		db_qual = self.cv_service.get_qualifiers()[0]
		assert qual.id == db_qual.id

	def test_get_site_type_cvs(self):
		assert self.cv_service.get_site_type_cvs() == []

		st_cv = self._add_site_type_cv()
		db_st_cv = self.cv_service.get_site_type_cvs()[0]
		assert st_cv.term == db_st_cv.term

	def test_get_variable_name_cvs(self):
		assert self.cv_service.get_variable_name_cvs() == []

		var_name_cv = self._add_variable_name_cv()
		db_var_name_cv = self.cv_service.get_variable_name_cvs()[0]
		assert var_name_cv.term == db_var_name_cv.term

	def test_get_offset_type_cvs(self):
		assert self.cv_service.get_offset_type_cvs() == []

		unit = self._add_unit()
		offset = self._add_offset_type_cv(unit.id)

		db_offset = self.cv_service.get_offset_type_cvs()[0]
		assert offset.id == db_offset.id
		assert offset.unit_id == db_offset.unit_id

	def test_get_speciation_cvs(self):
		assert self.cv_service.get_speciation_cvs() == []

		speciation = self._add_speciation_cv()
		db_speciation = self.cv_service.get_speciation_cvs()[0]
		assert speciation.term == db_speciation.term

	def test_get_sample_medium_cvs(self):
		assert self.cv_service.get_sample_medium_cvs() == []

		sample_medium = self._add_sample_medium_cv()
		db_sample_medium = self.cv_service.get_sample_medium_cvs()[0]
		assert sample_medium.term == db_sample_medium.term

	def test_get_value_type_cvs(self):
		assert self.cv_service.get_value_type_cvs() == []

		value_type = self._add_value_type_cv()
		db_val_type = self.cv_service.get_value_type_cvs()[0]
		assert value_type.term == db_val_type.term

	def test_get_data_type_cvs(self):
		assert self.cv_service.get_data_type_cvs() == []

		data_type = self._add_data_type_cv()
		db_data_type = self.cv_service.get_data_type_cvs()[0]
		assert data_type.term == db_data_type.term

	def test_get_general_category_cvs(self):
		assert self.cv_service.get_general_category_cvs() == []

		gen_cat = self._add_general_category_cv()
		db_gen_cat = self.cv_service.get_general_category_cvs()[0]
		assert gen_cat.term == db_gen_cat.term

	def test_get_censor_code_cvs(self):
		assert self.cv_service.get_censor_code_cvs() == []

		censor_code = self._add_censor_code_cv()
		db_censor_code = self.cv_service.get_censor_code_cvs()[0]
		assert censor_code.term == db_censor_code.term

	def test_get_sample_type_cvs(self):
		assert self.cv_service.get_sample_type_cvs() == []

		sample_type = self._add_sample_type_cv()
		db_sample_type = self.cv_service.get_sample_type_cvs()[0]
		assert sample_type.term == db_sample_type.term

	def test_get_units(self):
		assert self.cv_service.get_units() == []

		unit = self._add_unit()
		units = self.cv_service.get_units()
		assert len(units) == 1
		assert unit.id == units[0].id

	def test_get_unit_by_name(self):
		with pytest.raises(sqlalchemy.orm.exc.NoResultFound):
			self.cv_service.get_unit_by_name("Nothing")

		unit = self._add_unit()
		db_unit = self.cv_service.get_unit_by_name(unit.name)
		assert db_unit is not None
		assert unit.id == db_unit.id

	def test_get_unit_by_id(self):
		with pytest.raises(sqlalchemy.orm.exc.NoResultFound):
			self.cv_service.get_unit_by_id(0)

		unit = self._add_unit()
		db_unit = self.cv_service.get_unit_by_id(unit.id)
		assert db_unit is not None
		assert unit.name == db_unit.name

	def _add_vertical_datum_cv(self):
		vert_dat = VerticalDatumCV()
		vert_dat.term = "Test"
		vert_dat.definition = "This is a test"
		self.session.add(vert_dat)
		self.session.commit()
		return vert_dat

	def _add_lab_method(self):
		lab_method = LabMethod()
		lab_method.name = "Test Lab"
		lab_method.organization = "Test Org"
		lab_method.method_name = "Test Method"
		lab_method.method_description = "Test Description"
		lab_method.method_link = "Test Link"
		self.session.add(lab_method)
		self.session.commit()
		return lab_method

	def _add_sample(self, lab_method_id):
		sample = Sample()
		sample.type = "Test"
		sample.lab_sample_code = "ABC123"
		sample.lab_method_id = lab_method_id
		self.session.add(sample)
		self.session.commit()
		return sample

	def _add_site_type_cv(self):
		st_cv = SiteTypeCV()
		st_cv.term = "Test"
		st_cv.definition = "This is a test"
		self.session.add(st_cv)
		self.session.commit()
		return st_cv

	def _add_variable_name_cv(self):
		var_name_cv = VariableNameCV()
		var_name_cv.term = "Test"
		var_name_cv.definition = "This is a test"
		self.session.add(var_name_cv)
		self.session.commit()
		return var_name_cv

	def _add_unit(self):
		unit = Unit()
		unit.name = "Test"
		unit.type = "Test"
		unit.abbreviation = "T"
		self.session.add(unit)
		self.session.commit()
		return unit

	def _add_offset_type_cv(self, unit_id):
		offset = OffsetType()
		offset.unit_id = unit_id
		offset.description = "This is a test"
		self.session.add(offset)
		self.session.commit()
		return offset

	def _add_speciation_cv(self):
		spec = SpeciationCV()
		spec.term = "Test"
		spec.definition = "This is a test"
		self.session.add(spec)
		self.session.commit()
		return spec

	def _add_sample_medium_cv(self):
		samp_med = SampleMediumCV()
		samp_med.term = "Test"
		samp_med.definition = "This is a test"
		self.session.add(samp_med)
		self.session.commit()
		return samp_med

	def _add_value_type_cv(self):
		value_type = ValueTypeCV()
		value_type.term = "Test"
		value_type.definition = "This is a test"
		self.session.add(value_type)
		self.session.commit()
		return value_type

	def _add_data_type_cv(self):
		data_type = DataTypeCV()
		data_type.term = "Test"
		data_type.definition = "This is a test"
		self.session.add(data_type)
		self.session.commit()
		return data_type

	def _add_general_category_cv(self):
		gen_cat = GeneralCategoryCV()
		gen_cat.term = "Test"
		gen_cat.definition = "This is a test"
		self.session.add(gen_cat)
		self.session.commit()
		return gen_cat

	def _add_censor_code_cv(self):
		censor = CensorCodeCV()
		censor.term = "Test"
		censor.definition = "This is a test"
		self.session.add(censor)
		self.session.commit()
		return censor

	def _add_sample_type_cv(self):
		sample_type = SampleTypeCV()
		sample_type.term = "Test"
		sample_type.definition = "This is a test"
		self.session.add(sample_type)
		self.session.commit()
		return sample_type