import wx
from odmtools.controller.frmSeriesSelector import FrmSeriesSelector
from odmtools.odmservices import ServiceManager


__author__ = 'Jacob'

class TestFrmSeriesSelector:
    def setup(self):
        self.app = wx.App()

        self.service_manager = ServiceManager()
        #self.sc = self.service_manager.get_series_service(conn_dict=conn_dict)
        self.sc = None

        self.wxFrame = wx.Frame(None)
        self.pnlDocking = wx.Panel(self.wxFrame)

        self.frame = FrmSeriesSelector(name=u'pnlSelector', parent=self.pnlDocking,
                                             size=wx.Size(770, 388), style=wx.TAB_TRAVERSAL, dbservice=self.sc,
                                             serviceManager=self.service_manager)
        assert self.frame


    #def test_issue_166(self):
    #    pass