from odmtools.odmdata import SessionFactory, Series
from odmtools.odmservices import SeriesService
from tests import test_util

__author__ = 'jmeline'

"""
Sample ODM Database connection and data insertion for unittesting against
"""

class TestPandasMemoryDB:
    """
    Test to Load up a series_service from a dataframe and load it into an in memory database
    """
    def setup(self):
        self.connection_string = "sqlite:///:memory:"
        self.session_factory = SessionFactory(self.connection_string, echo=False)
        self.session = self.session_factory.get_session()

        self.series_service = SeriesService(connection_string=self.connection_string)
        engine = self.session_factory.engine
        test_util.build_db(engine)

    def test_build_series(self):
        dvs = 100
        self.series = test_util.add_series_bulk_data(self.session, dvs_size=dvs)
        assert self.series
        assert len(self.series.data_values) == dvs






