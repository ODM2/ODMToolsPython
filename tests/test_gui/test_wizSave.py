from unittest import TestCase

__author__ = 'stephanie'

from odmtools.gui.wizSave import wizSave
from odmtools.odmdata import MemoryDatabase
from odmtools.odmservices import ServiceManager
from odmtools.odmservices import SeriesService

from tests import test_util
import wx




class TestWizSave:
    def setup(self):
        conn_dict = {'engine': 'sqlite', 'address': ':memory:'}
        self.sm = ServiceManager(conn_dict=conn_dict)
        # set up remote Database
        # self.connection_string = "sqlite:///:memory:"

        self.series_service = self.sm.get_series_service()  # SeriesService(connection_string=self.connection_string, debug=False)
        self.session = self.series_service._session_factory.get_session()
        engine = self.series_service._session_factory.engine
        test_util.build_db(engine)

        self.dvs_size = 100
        self.series = test_util.add_series_bulk_data(self.session, dvs_size=self.dvs_size)
        assert self.series
        assert len(self.series.data_values) == self.dvs_size

        self.memory_database = MemoryDatabase()
        self.memory_database.set_series_service(self.series_service)
        # self.memory_database.initEditValues(self.series.id)

        self.app = wx.App()
        self.frame = wx.Frame(None)
        self.wizard = wizSave(self.frame,self.sm, self.sm.get_edit_service(self.series.id, self.memory_database))
#TODO get wizard tests working
    # def test___init__(self):
    #     assert self.frame
    #     assert self.wizard
    #     self.wizard.init(self, self.sm, self.memory_database)
    #
    #
    # def test__init_ctrls(self):
    #     self.fail()
    #
    # def test_get_metadata(self):
    #     self.fail()
    #
    # def test_on_page_changed(self):
    #     self.fail()
    #
    # def test_on_page_changing(self):
    #     self.fail()
    #
    # def test_on_wizard_finishedtest(self):
    #     self.fail()
    #
    # def test_on_wizard_finished(self):
    #     self.fail()
