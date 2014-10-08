# -*- coding: utf-8 -*- 

# ##########################################################################
# # Python code generated with wxFormBuilder (version Feb 26 2014)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
from odmtools.lib.ObjectListView import FastObjectListView as objectListView, ColumnDefn

###########################################################################
## Class pnlExisting
###########################################################################

class pnlExisting(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(500, 300),
                          style=wx.TAB_TRAVERSAL)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        self.lblExisting = wx.StaticText(self, wx.ID_ANY, u"Select an Existing Series:", wx.DefaultPosition,
                                         wx.DefaultSize, 0)
        self.lblExisting.Wrap(-1)
        bSizer1.Add(self.lblExisting, 0, wx.ALL, 5)

        #self.olvSeriesList = wx.ListCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_ICON)

        self.olvSeriesList = objectListView(self, wx.ID_ANY, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
       # self.myOlv = FastObjectListView(self, -1, style=wx.LC_REPORT)

        bSizer1.Add(self.olvSeriesList, 100, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        # Connect Events
        self.olvSeriesList.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnOLVItemSelected)


    def __del__(self):
        pass



    # Virtual event handlers, overide them in your derived class
    def OnOLVItemSelected(self, event):
        event.Skip()


