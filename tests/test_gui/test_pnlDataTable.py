from odmtools.odmdata import MemoryDatabase, DataValue
from odmtools.gui.pnlDataTable import pnlDataTable
from odmtools.odmdata import SessionFactory
from odmtools.odmservices import SeriesService
from tests import test_util
import wx
from tests.test_util import build_db

__author__ = 'jmeline'

class TestPnlDataTable:
    def setup(self):
        # self.connection_string = "sqlite:///:memory:"
        # self.series_service = SeriesService(connection_string=self.connection_string, debug=False)
        # self.session = self.series_service._session_factory.get_session()

        # engine = self.series_service._session_factory.engine
        # test_util.build_db(engine)

        self.memory_database = MemoryDatabase()
        self.session_factory = self.memory_database.mem_service._session_factory
        engine = self.session_factory.engine
        self.session = self.session_factory.get_session()

        test_util.build_db(engine)

        self.app = wx.App()
        self.frame = wx.Frame(None)
        self.dataTable = pnlDataTable(self.frame)

    def test_build_series(self):
        self.series = test_util.add_series_bulk_data(self.session)
        assert self.series
        assert len(self.series.data_values) == 700

        self.memory_database.initEditValues(self.series.id)

        dvs = self.session.query(DataValue).all()
        assert len(dvs) == 700

        dvs = self.memory_database.mem_service._edit_session.query(DataValue).all()
        assert len(dvs) == 700


    def test_get_data_values_data_frame(self):
        df = self.memory_database.getDataValuesDF()
        assert not df.empty

    def test_init_pnlDataTable(self):
        assert self.frame
        assert self.dataTable
        self.dataTable.init(self.memory_database)

