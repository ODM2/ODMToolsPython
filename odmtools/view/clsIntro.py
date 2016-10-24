# # -*- coding: utf-8 -*-
#
# # ##########################################################################
# ## Python code generated with wxFormBuilder (version Feb 26 2014)
# ## http://www.wxformbuilder.org/
# ##
# ## PLEASE DO "NOT" EDIT THIS FILE!
# ###########################################################################
#
# import wx
# import wx.xrc
# import wx.aui
#
# ###########################################################################
# ## Class pnlIntro
# ###########################################################################
#
# class pnlIntro(wx.Panel):
# #	id=wxID_PNLINTRO, name=u'pnlIntro',
# #              pos=wx.Point(536, 285), size=wx.Size(439, 357), style=wx.TAB_TRAVERSAL
#     def __init__(self, parent):#, id, pos, size, style, name):
#         #wx.Panel.__init__(self, parent=parent), id=id, pos=pos, size=size, style=style, name=name)
#         wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL )
#
#         self.m_mgr = wx.aui.AuiManager()
#         self.m_mgr.SetManagedWindow(self)
#         self.m_mgr.SetFlags(wx.aui.AUI_MGR_DEFAULT)
#
#         self.m_panel2 = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
#         self.m_mgr.AddPane(self.m_panel2,
#                            wx.aui.AuiPaneInfo().Center().CaptionVisible(False).CloseButton(False).PaneBorder(
#                                False).Movable(False).Dock().Resizable().FloatingSize(wx.DefaultSize).BottomDockable(
#                                False).TopDockable(False).LeftDockable(False).RightDockable(False).Floatable(False))
#
#         bSizer2 = wx.BoxSizer(wx.VERTICAL)
#
#         self.lblHow = wx.StaticText(self.m_panel2, wx.ID_ANY, u"How would you like to save the series_service?",
#                                     wx.DefaultPosition, wx.DefaultSize, 0)
#         self.lblHow.Wrap(-1)
#         bSizer2.Add(self.lblHow, 0, wx.ALL, 15)
#
#         bSizer3 = wx.BoxSizer(wx.HORIZONTAL)
#
#         self.m_panel3 = wx.Panel(self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
#         bSizer3.Add(self.m_panel3, 10, wx.EXPAND | wx.ALL, 5)
#
#         self.rbSave = wx.RadioButton(self.m_panel2, wx.ID_ANY,
#                                      u"Save (Save the data using the same Series Catalog Entry)", wx.DefaultPosition,
#                                      wx.DefaultSize, wx.RB_GROUP)
#         self.rbSave.SetValue(True)
#         bSizer3.Add(self.rbSave, 90, wx.ALL, 5)
#
#         bSizer2.Add(bSizer3, 1, wx.EXPAND, 5)
#
#         bSizer4 = wx.BoxSizer(wx.HORIZONTAL)
#
#         self.m_panel4 = wx.Panel(self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
#         bSizer4.Add(self.m_panel4, 10, wx.EXPAND | wx.ALL, 5)
#
#         self.rbSaveAs = wx.RadioButton(self.m_panel2, wx.ID_ANY, u"Save As.. (Create a new Series Catalog Entry)",
#                                        wx.DefaultPosition, wx.DefaultSize, 0)
#         bSizer4.Add(self.rbSaveAs, 90, wx.ALL, 5)
#
#         bSizer2.Add(bSizer4, 1, wx.EXPAND, 0)
#
#         bSizer5 = wx.BoxSizer(wx.HORIZONTAL)
#
#         self.m_panel5 = wx.Panel(self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
#         bSizer5.Add(self.m_panel5, 10, wx.EXPAND | wx.ALL, 5)
#
#         self.rbSaveExisting = wx.RadioButton(self.m_panel2, wx.ID_ANY,
#                                              u"Save As Existing.. (Save to an Existing Series Catalog Entry)",
#                                              wx.DefaultPosition, wx.DefaultSize, 0)
#         bSizer5.Add(self.rbSaveExisting, 90, wx.ALL, 5)
#
#         bSizer2.Add(bSizer5, 1, wx.EXPAND, 5)
#
#         bSizer2.AddSpacer(( 10, 150), 1, wx.EXPAND, 5)
#
#         self.m_panel2.SetSizer(bSizer2)
#         self.m_panel2.Layout()
#         bSizer2.Fit(self.m_panel2)
#
#         self.m_mgr.Update()
#
#         # Connect Events
#         self.rbSave.Bind(wx.EVT_RADIOBUTTON, self.OnBtnSaveRadiobutton)
#         self.rbSaveAs.Bind(wx.EVT_RADIOBUTTON, self.OnBtnSaveAsRadiobutton)
#         self.rbSaveExisting.Bind(wx.EVT_RADIOBUTTON, self.OnBtnSaveExistingRadiobuton)
#
#     def __del__(self):
#         self.m_mgr.UnInit()
#
#
#     # Virtual event handlers, overide them in your derived class
#     def OnBtnSaveRadiobutton(self, event):
#         print "in parent"
#         event.Skip()
#
#     def OnBtnSaveAsRadiobutton(self, event):
#         print "in parent"
#         event.Skip()
#
#     def OnBtnSaveExistingRadiobuton(self, event):
#         print "in parent"
#         event.Skip()
#
# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Jun  5 2014)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.aui

###########################################################################
## Class pnlIntro
###########################################################################

class pnlIntro(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(500, 300),
                          style=wx.TAB_TRAVERSAL)

        self.m_mgr = wx.aui.AuiManager()
        self.m_mgr.SetManagedWindow(self)
        self.m_mgr.SetFlags(wx.aui.AUI_MGR_DEFAULT)

        self.m_panel2 = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.m_mgr.AddPane(self.m_panel2,
                           wx.aui.AuiPaneInfo().Center().CaptionVisible(False).CloseButton(False).PaneBorder(
                               False).Movable(False).Dock().Resizable().FloatingSize(wx.DefaultSize).BottomDockable(
                               False).TopDockable(False).LeftDockable(False).RightDockable(False).Floatable(False))

        bSizer2 = wx.BoxSizer(wx.VERTICAL)

        self.lblHow = wx.StaticText(self.m_panel2, wx.ID_ANY, u"How would you like to save the series_service?",
                                    wx.DefaultPosition, wx.DefaultSize, 0)
        self.lblHow.Wrap(-1)
        bSizer2.Add(self.lblHow, 0, wx.ALL, 15)

        bSizer3 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_panel3 = wx.Panel(self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer3.Add(self.m_panel3, 10, wx.EXPAND | wx.ALL, 5)

        self.rbSave = wx.RadioButton(self.m_panel2, wx.ID_ANY, u"Save ", wx.DefaultPosition, wx.DefaultSize,
                                     wx.RB_GROUP)
        self.rbSave.SetValue(True)
        bSizer3.Add(self.rbSave, 90, wx.ALL, 5)

        bSizer2.Add(bSizer3, 1, wx.EXPAND, 5)

        bSizer4 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_panel4 = wx.Panel(self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer4.Add(self.m_panel4, 10, wx.EXPAND | wx.ALL, 5)

        self.rbSaveAsOption = wx.StaticText(self.m_panel2, wx.ID_ANY, u"Save As.. ", wx.DefaultPosition,
                                             wx.DefaultSize, 0)
        # self.rbSaveAsOption.Enable(False)

        bSizer4.Add(self.rbSaveAsOption, 90, wx.ALL, 5)

        bSizer2.Add(bSizer4, 1, wx.EXPAND, 0)

        bSizer5 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_panel5 = wx.Panel(self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer5.Add(self.m_panel5, 20, wx.EXPAND | wx.ALL, 5)

        self.rbSaveExisting = wx.RadioButton(self.m_panel2, wx.ID_ANY, u"Existing Series", wx.DefaultPosition,
                                             wx.DefaultSize, 0)
        bSizer5.Add(self.rbSaveExisting, 90, wx.ALL, 5)

        bSizer2.Add(bSizer5, 1, wx.EXPAND, 5)

        bSizer51 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_panel51 = wx.Panel(self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer51.Add(self.m_panel51, 20, wx.EXPAND | wx.ALL, 5)

        self.rbSaveAs = wx.RadioButton(self.m_panel2, wx.ID_ANY, u"New Series", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer51.Add(self.rbSaveAs, 90, wx.ALL, 5)

        bSizer2.Add(bSizer51, 1, wx.EXPAND, 5)

        bSizer2.AddSpacer(( 10, 150), 1, wx.EXPAND, 5)

        self.m_panel2.SetSizer(bSizer2)
        self.m_panel2.Layout()
        bSizer2.Fit(self.m_panel2)

        self.m_mgr.Update()

        # Connect Events
        self.rbSave.Bind(wx.EVT_RADIOBUTTON, self.OnBtnSaveRadiobutton)
        self.rbSaveAsOption.Bind(wx.EVT_RADIOBUTTON, self.OnBtnSaveAsRadiobutton)
        self.rbSaveExisting.Bind(wx.EVT_RADIOBUTTON, self.OnBtnSaveExistingRadiobuton)
        self.rbSaveAs.Bind(wx.EVT_RADIOBUTTON, self.OnBtnSaveExistingRadiobuton)

    def __del__(self):
        self.m_mgr.UnInit()


    # Virtual event handlers, overide them in your derived class
    def OnBtnSaveRadiobutton(self, event):
        print "in parent"
        event.Skip()

    def OnBtnSaveAsRadiobutton(self, event):
        print "in parent"
        event.Skip()

    def OnBtnSaveExistingRadiobuton(self, event):
        print "in parent"
        event.Skip()

