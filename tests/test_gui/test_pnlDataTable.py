from odmtools.controller.frmDataTable import FrmDataTable
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
        #set up remote Database
        self.connection_string = "sqlite:///:memory:"
        self.series_service = SeriesService(connection_string=self.connection_string, debug=False)
        self.session = self.series_service._session_factory.get_session()
        engine = self.series_service._session_factory.engine
        test_util.build_db(engine)

        self.dvs_size = 100
        self.series = test_util.add_series_bulk_data(self.session, dvs_size=self.dvs_size)
        assert self.series
        assert len(self.series.data_values) == self.dvs_size

        self.memory_database = MemoryDatabase()
        self.memory_database.set_series_service(self.series_service)
        self.memory_database.initEditValues(self.series.id)

        self.app = wx.App()
        self.frame = wx.Frame(None)
        self.dataTable = FrmDataTable(self.frame)

    def test_build_series(self):
        dvs = self.session.query(DataValue).all()
        assert len(dvs) == self.dvs_size
        dvs = self.memory_database.mem_service._edit_session.query(DataValue).all()
        assert len(dvs) == self.dvs_size

    def test_get_data_values_data_frame(self):
        df = self.memory_database.getDataValuesDF()
        assert not df.empty

    def test_init_pnlDataTable(self):
        assert self.frame
        assert self.dataTable
        self.dataTable.init(self.memory_database)

    def test_selecting_points(self):
        self.dataTable.init(self.memory_database)
        values = self.dataTable.olvDataTable.dataframe
        assert not values.empty

        self.dataTable.onChangeSelection(values)
        myOlv = self.dataTable.olvDataTable

        count = 0

        selected_item = myOlv.GetFirstSelected()
        assert selected_item != -1

        # loop through selected items
        while selected_item != -1:
            selected_item = myOlv.GetNextSelected(selected_item)
            count += 1

        assert count == self.dvs_size
    def test_deselecting_all(self):
        self.dataTable.init(self.memory_database)
        assert self.dataTable.olvDataTable.GetItemCount() == self.dvs_size
        values = self.dataTable.olvDataTable.dataframe

        self.dataTable.onChangeSelection(values)
        self.dataTable.olvDataTable.onDeselectAll()
        selected_item = self.dataTable.olvDataTable.GetFirstSelected()
        assert selected_item == -1

    def test_clear_data_table(self):
        self.dataTable.init(self.memory_database)
        assert self.dataTable.olvDataTable.GetItemCount() == self.dvs_size
        self.dataTable.clear()
        assert not self.dataTable.olvDataTable.dataframe
        assert self.dataTable.olvDataTable.GetItemCount() == 0








