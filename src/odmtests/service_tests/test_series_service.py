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