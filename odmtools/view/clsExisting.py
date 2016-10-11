

'''
Different from generated code
        from odmtools.lib.ObjectListView import FastObjectListView as objectListView, ColumnDefn
        #self.olvSeriesList = wx.ListCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_ICON)

        self.olvSeriesList = objectListView(self, wx.ID_ANY, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
       # self.myOlv = FastObjectListView(self, -1, style=wx.LC_REPORT)
'''




# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Jun  5 2014)
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

        self.olvSeriesList = objectListView(self, wx.ID_ANY, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        bSizer1.Add(self.olvSeriesList, 100, wx.ALL | wx.EXPAND, 5)

        self.m_panel1 = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer2 = wx.BoxSizer(wx.VERTICAL)

        self.rbOverwrite = wx.RadioButton(self.m_panel1, wx.ID_ANY, u"Overwrite Entire Series", wx.DefaultPosition,
                                          wx.DefaultSize, 0)
        bSizer2.Add(self.rbOverwrite, 0, wx.ALL, 5)

        self.rbAppend = wx.RadioButton(self.m_panel1, wx.ID_ANY, u"Append to Series (adds values to the end of a series)", wx.DefaultPosition,
                                       wx.DefaultSize, 0)
        bSizer2.Add(self.rbAppend, 0, wx.ALL, 5)

        bSizer5 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_panel2 = wx.Panel(self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer5.Add(self.m_panel2, 10, wx.EXPAND | wx.ALL, 5)

        bSizer3 = wx.BoxSizer(wx.VERTICAL)

        self.lblOverlap = wx.StaticText(self.m_panel1, wx.ID_ANY, u"If Data Overlaps:", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.lblOverlap.Wrap(-1)
        self.lblOverlap.Enable(False)

        bSizer3.Add(self.lblOverlap, 0, wx.ALL, 5)

        #Group 2
        self.rbNew = wx.RadioButton(self.m_panel1, wx.ID_ANY, u"Keep New", wx.DefaultPosition, wx.DefaultSize, style=wx.RB_GROUP)
        self.rbNew.Enable(False)

        bSizer3.Add(self.rbNew, 0, wx.ALL, 5)

        self.rbOriginal = wx.RadioButton(self.m_panel1, wx.ID_ANY, u"Keep Original", wx.DefaultPosition, wx.DefaultSize,
                                         0)
        self.rbOriginal.Enable(False)
        #
        bSizer3.Add(self.rbOriginal, 0, wx.ALL, 5)

        bSizer5.Add(bSizer3, 90, wx.EXPAND, 5)

        bSizer2.Add(bSizer5, 1, wx.EXPAND, 5)

        self.m_panel1.SetSizer(bSizer2)
        self.m_panel1.Layout()
        bSizer2.Fit(self.m_panel1)
        bSizer1.Add(self.m_panel1, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        # Connect Events
        # Connect Events
        self.olvSeriesList.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnOLVItemSelected)
        self.rbOverwrite.Bind(wx.EVT_RADIOBUTTON, self.onOverwrite)
        self.rbAppend.Bind(wx.EVT_RADIOBUTTON, self.onAppend)

    def __del__(self):
        pass


    # Virtual event handlers, overide them in your derived class
    def OnOLVItemSelected(self, event):
        event.Skip()


    def onOverwrite(self, event):
        event.Skip()


    def onAppend(self, event):
        event.Skip()


