import os.path
from odmtools.odmservices import SeriesService, ExportService

from tests import test_util


class TestExportService:
	def setup(self):		
		self.connection_string = "sqlite:///:memory:"
		self.series_service = SeriesService(self.connection_string, debug=False)

		self.session = self.series_service._connection.get_session()
		engine = self.series_service._connection.engine

		test_util.build_db(engine)
		self.series = test_util.add_series(self.session)

		self.export_service = ExportService(self.series_service)

	def test_export_series_data(self, tmpdir):
		f = tmpdir.join("export.csv")
		filename = f.dirname + f.basename

		self.export_service.export_series_data(self.series.id, filename, True,True,True,True,True,True,True)

		assert os.path.isfile(filename) == True

	def test_export_series_metadata(self, tmpdir):		
		f = tmpdir.join("export.xml")
		filename = f.dirname + f.basename

		ids = [self.series.id]
		self.export_service.export_series_metadata(ids, filename)

		assert os.path.isfile(filename) == True