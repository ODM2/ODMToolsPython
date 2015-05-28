from odmtools.odmdata import *
from odmtools.odmservices import SeriesService, EditService

from tests import test_util


class TestSeriesService:
    def setup(self):

        self.connection_string = "sqlite:///:memory:"
        self.series_service = SeriesService(connection_string=self.connection_string, debug=False)

        engine = self.series_service._session_factory.engine
        test_util.build_db(engine)

        self.memory_database = MemoryDatabase()
        self.memory_database.set_series_service(self.series_service)
        self.session = self.memory_database.series_service._session_factory.get_session()

        self.series = test_util.add_series_bulk_data(self.session)
        #assert len(self.series.data_values) == 100

        self.edit_service =EditService(1, connection= self.memory_database)


    ## TODO Unittest save_series, save_as, save_as_existing

    def test_save_series(self):
        assert self.edit_service.save()

    def test_save_as_series(self):
        var = test_util.add_variable(self.session)
        print var
        assert self.edit_service.save_as(var= var)
        ##assert self.edit_service.memDB.series_service.series_exists(self.series.site.id, var, self.series.method.id,
        #                                         self.series.source.id, self.series.qcl.id)


    def test_save_as_existing_series(self):
        var = test_util.add_variable(self.session)
        assert self.edit_service.save_existing(var = var)


