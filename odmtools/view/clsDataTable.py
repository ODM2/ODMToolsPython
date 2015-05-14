from controller.olvDataTable import OLVDataTable

__author__ = 'jmeline'

import wx
class DataTable(wx.Panel):
    def __init__(self, parent, **kwargs):
        kwargs['name'] = u'pnlDataTable'
        kwargs['parent'] = parent
        kwargs['size'] = wx.Size(677, 449)
        kwargs['style'] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, **kwargs)

        self.olvDataTable = OLVDataTable(self)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_2.Add(self.olvDataTable, 1, wx.ALL | wx.EXPAND, 4)
        self.SetSizer(sizer_2)
        self.Layout()


    # Overridden in base class
    def onItemSelected(self, event):
        event.Skip()
