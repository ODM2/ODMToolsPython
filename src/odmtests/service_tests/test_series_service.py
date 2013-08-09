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
		site = test_util.add_site(self.session)
		sites = self.series_service.get_all_sites()
		assert len(sites) == 1
		assert site.code == sites[0].code

	def test_get_site_by_id_fail(self):
		with pytest.raises(sqlalchemy.orm.exc.NoResultFound):
			self.series_service.get_site_by_id(0)

		site = test_util.add_site(self.session)
		db_site = None
		with pytest.raises(sqlalchemy.orm.exc.NoResultFound):
			db_site = self.series_service.get_site_by_id(10)
		assert db_site == None

	def test_get_site_by_id(self):
		site = test_util.add_site(self.session)
		db_site = self.series_service.get_site_by_id(site.id)
		assert db_site != None
		assert site.code == db_site.code

	def test_get_all_variables_empty(self):
		variables = self.series_service.get_all_variables()
		assert len(variables) == 0
		assert variables == []

	def test_get_all_variables(self):
		variable = test_util.add_variable(self.session)
		variables = self.series_service.get_all_variables()
		assert len(variables) == 1
		assert variable.code == variables[0].code