import pytest
import sqlalchemy.orm.exc

from odmdata import *
from odmservices import SeriesService

from odmtests import test_util

class TestSeriesService:
	def setup(self):
		self.connection_string = "sqlite:///:memory:"
		self.series_service = SeriesService(self.connection_string, debug=False)
		self.session = self.series_service._session_factory.get_session()
		engine = self.series_service._session_factory.engine
		test_util.build_db(engine)

	def test_get_test_data(self):
		version = test_util.add_version(self.session)
		db_version = self.series_service.get_test_data()
		assert version.version_number == db_version.version_number

	def test_get_all_sites_empty(self):
		sites = self.series_service.get_all_sites()
		assert len(sites) == 0
		assert sites == []

	def test_get_all_sites(self):
		assert self.series_service.get_all_sites() == []
		site = test_util.add_site(self.session)
		sites = self.series_service.get_all_sites()
		assert len(sites) == 1
		assert site.code == sites[0].code

	def test_get_site_by_id_fail(self):
		assert self.series_service.get_site_by_id(0) == None

		site = test_util.add_site(self.session)
		db_site = self.series_service.get_site_by_id(10)
		assert db_site == None

	def test_get_site_by_id(self):
		site = test_util.add_site(self.session)
		db_site = self.series_service.get_site_by_id(site.id)
		assert db_site != None
		assert site.code == db_site.code

	def test_get_all_variables(self):
		assert self.series_service.get_all_variables() == []
		variable = test_util.add_variable(self.session)
		variables = self.series_service.get_all_variables()
		assert len(variables) == 1
		assert variable.code == variables[0].code

	def test_get_variable_by_id(self):
		assert self.series_service.get_variable_by_id(10) == None

		variable = test_util.add_variable(self.session)
		db_var = self.series_service.get_variable_by_id(variable.id)

		assert db_var != None
		assert db_var.code == variable.code

	def test_get_variables_by_site_code(self):
		assert self.series_service.get_variables_by_site_code('ABC123') == []

		series = test_util.add_series(self.session)
		variable = series.variable

		db_variables = self.series_service.get_variables_by_site_code(series.site_code)
		assert db_variables != None
		assert variable.code == db_variables[0].code

	def test_get_all_units(self):
		assert self.series_service.get_all_units() == []

		unit = test_util.add_unit(self.session)
		units = self.series_service.get_all_units()

		assert len(units) == 1
		assert unit.name == units[0].name

	def test_get_unit_by_name(self):
		assert self.series_service.get_unit_by_name("FAIL") == None

		unit = test_util.add_unit(self.session)
		db_unit = self.series_service.get_unit_by_name(unit.name)

		assert unit.id == db_unit.id

	def test_get_unit_by_id(self):
		assert self.series_service.get_unit_by_id(10) == None

		unit = test_util.add_unit(self.session)
		db_unit = self.series_service.get_unit_by_id(unit.id)

		assert unit.name == db_unit.name

	def test_get_all_series(self):
		assert self.series_service.get_all_series() == []

		series = test_util.add_series(self.session)
		all_series = self.series_service.get_all_series()

		assert all_series != []
		assert series.id == all_series[0].id

	def test_get_series_by_id(self):
		assert self.series_service.get_series_by_id(10) == None

		series = test_util.add_series(self.session)
		db_series = self.series_service.get_series_by_id(series.id)

		assert series.id == db_series.id

	def test_get_series_by_id_quint(self):
		assert self.series_service.get_series_by_id_quint(10, 10, 10, 10, 10) == None

		series = test_util.add_series(self.session)
		db_series = self.series_service.get_series_by_id_quint(
			series.site_id, series.variable_id, series.method_id,
			series.source_id, series.quality_control_level_id)

		assert series.id == db_series.id

	def test_series_exists(self):
		assert self.series_service.series_exists(10,10,10,10,10) == False

		series = test_util.add_series(self.session)
		site_id = series.site_id
		var_id = series.variable_id
		method_id = series.method_id
		source_id = series.source_id
		qcl_id = series.quality_control_level_id

		assert self.series_service.series_exists(site_id,var_id,method_id,source_id,qcl_id) == True

	def test_save_series(self):
		series = Series()
		site = test_util.add_site(self.session)
		variable = test_util.add_variable(self.session)
		method = test_util.add_method(self.session)
		source = test_util.add_source(self.session)
		qcl = test_util.add_qcl(self.session)

		series.site_id = site.id
		series.site_code = site.code
		series.variable_id = variable.id
		series.variable_code = variable.code
		series.method_id = method.id
		series.source_id = source.id
		series.quality_control_level_id = qcl.id

		dvs = []
		for val in range(10):
			dv = DataValue()
			dv.data_value = val
			dv.site_id = site.id
			dv.variable_id = variable.id
			dv.method_id = method.id
			dv.source_id = source.id
			dv.quality_control_level_id = qcl.id
			dvs.append(dv)

		print series.variable_code
		assert self.series_service.save_series(series, dvs) == True
		assert self.series_service.series_exists(site.id, variable.id, method.id, source.id, qcl.id) == True
		assert self.series_service.save_series(series, dvs) == False