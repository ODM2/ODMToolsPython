# -*- coding: utf-8 -*- 

# ##########################################################################
## Python code generated with wxFormBuilder (version Feb 26 2014)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.lib.masked as masked

###########################################################################
## Class clsDataFilters
###########################################################################

class clsDataFilters(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"Data Filter", pos=wx.Point(599, 384),
                           size=wx.Size(367, 452), style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHintsSz(wx.Size(358, 452), wx.DefaultSize)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        bSizer3 = wx.BoxSizer(wx.VERTICAL)

        bsValueThresh = wx.BoxSizer(wx.HORIZONTAL)

        self.rbThreshold = wx.RadioButton(self, wx.ID_ANY, wx.EmptyString, wx.Point(10, 8), wx.DefaultSize, wx.RB_GROUP)
        self.rbThreshold.SetValue(True)
        bsValueThresh.Add(self.rbThreshold, 0, wx.ALL, 5)

        sbThreshold = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Value Threshold"), wx.VERTICAL)

        fgSizer1 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer1.SetFlexibleDirection(wx.HORIZONTAL)
        fgSizer1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.lblChangegt = wx.StaticText(self, wx.ID_ANY, u"Value >", wx.DefaultPosition, wx.DefaultSize, 0)
        self.lblChangegt.Wrap(-1)
        fgSizer1.Add(self.lblChangegt, 0, wx.ALL, 5)

        self.txtThreshValGT = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(248, -1), 0)
        fgSizer1.Add(self.txtThreshValGT, 0, wx.ALL, 5)

        self.lblChangelt = wx.StaticText(self, wx.ID_ANY, u"Value <", wx.DefaultPosition, wx.DefaultSize, 0)
        self.lblChangelt.Wrap(-1)
        fgSizer1.Add(self.lblChangelt, 0, wx.ALL, 5)

        self.txtThreshValLT = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(248, -1), 0)
        fgSizer1.Add(self.txtThreshValLT, 0, wx.ALL, 5)

        sbThreshold.Add(fgSizer1, 1, wx.EXPAND, 5)

        bsValueThresh.Add(sbThreshold, 1, wx.EXPAND, 5)

        bSizer3.Add(bsValueThresh, 1, wx.EXPAND, 5)

        bsGaps = wx.BoxSizer(wx.HORIZONTAL)

        self.rbDataGaps = wx.RadioButton(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize)
        self.rbDataGaps.SetValue(False)
        bsGaps.Add(self.rbDataGaps, 0, wx.ALL, 5)


        sbGaps = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Data Gaps"), wx.VERTICAL)

        fgSizer2 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer2.SetFlexibleDirection(wx.HORIZONTAL)
        fgSizer2.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.lblGapsVal = wx.StaticText(self, wx.ID_ANY, u"Value:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.lblGapsVal.Wrap(-1)
        fgSizer2.Add(self.lblGapsVal, 0, wx.ALL, 5)

        self.txtGapsVal = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(230, -1), 0)
        fgSizer2.Add(self.txtGapsVal, 0, wx.ALL, 5)

        self.lblGapsTime = wx.StaticText(self, wx.ID_ANY, u"Time Period:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.lblGapsTime.Wrap(-1)
        fgSizer2.Add(self.lblGapsTime, 0, wx.ALL, 5)

        cbGapTimeChoices = [ u"second", u"minute", u"hour", u"day" ]
        self.cbGapTime = wx.ComboBox( self, wx.ID_ANY, u"second", wx.DefaultPosition, wx.Size( 230,-1 ), cbGapTimeChoices, wx.CB_READONLY )
        fgSizer2.Add(self.cbGapTime, 0, wx.ALL, 5)

        sbGaps.Add(fgSizer2, 1, wx.EXPAND, 5)

        bsGaps.Add(sbGaps, 1, wx.EXPAND, 5)

        bSizer3.Add(bsGaps, 1, wx.EXPAND, 5)

        bsDate = wx.BoxSizer(wx.HORIZONTAL)

        self.rbDate = wx.RadioButton(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize)
        self.rbDate.SetValue(False)
        bsDate.Add(self.rbDate, 0, wx.ALL, 5)

        sbDate = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Date"), wx.VERTICAL)

        fgSizer3 = wx.FlexGridSizer(0, 4, 0, 0)
        fgSizer3.SetFlexibleDirection(wx.HORIZONTAL)
        fgSizer3.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.lblDateBefore = wx.StaticText(self, wx.ID_ANY, u"Before: ", wx.DefaultPosition, wx.DefaultSize, 0)
        self.lblDateBefore.Wrap(-1)
        fgSizer3.Add(self.lblDateBefore, 0, wx.ALL, 5)

        self.dpBefore = wx.DatePickerCtrl(self, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.Size(150, -1),
                                          wx.DP_DEFAULT|wx.DP_DROPDOWN)
        fgSizer3.Add(self.dpBefore, 0, wx.ALL, 5)

        self.sbBefore = wx.SpinButton(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(15, -1), 0)
        self.tpBefore = masked.TimeCtrl(self, wx.ID_ANY, pos=wx.DefaultPosition, size= wx.Size(80, -1), name="24 hour control",
                                        fmt24hr=True, spinButton=self.sbBefore, oob_color = 'White')
        #self.tpBefore = wx.StaticText( self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.Size( 80,-1 ), 0 )

        fgSizer3.Add(self.tpBefore, 0, wx.TOP, 5)
        fgSizer3.Add(self.sbBefore, 0, wx.TOP, 5)

        self.lblDateAfter = wx.StaticText(self, wx.ID_ANY, u"After:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.lblDateAfter.Wrap(-1)


        self.dpAfter = wx.DatePickerCtrl(self, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.Size(150, -1),
                                         wx.DP_DEFAULT|wx.DP_DROPDOWN)
        fgSizer3.Add(self.lblDateAfter, 0, wx.ALL, 5)
        fgSizer3.Add(self.dpAfter, 0, wx.ALL, 5)
        self.sbAfter = wx.SpinButton(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(15, -1), 0)

        #self.tpAfter = wx.StaticText( self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.Size( 80,-1 ), 0 )
        self.tpAfter = masked.TimeCtrl(self, wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(80, -1), name="24 hour control",
                                       fmt24hr=True, spinButton=self.sbAfter,  oob_color = "White")
        fgSizer3.Add(self.tpAfter, 0, wx.TOP, 5)
        fgSizer3.Add(self.sbAfter, 0, wx.TOP, 5)

        sbDate.Add(fgSizer3, 1, wx.EXPAND, 5)

        bsDate.Add(sbDate, 1, wx.EXPAND, 5)

        bSizer3.Add(bsDate, 1, wx.EXPAND, 5)

        bsValChange = wx.BoxSizer(wx.HORIZONTAL)

        self.rbVChangeThresh = wx.RadioButton(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize)
        self.rbVChangeThresh.SetValue(False)
        bsValChange.Add(self.rbVChangeThresh, 0, wx.ALL, 5)

        sbValChange = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Value Change Threshold"), wx.VERTICAL)

        fgSizer4 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer4.SetFlexibleDirection(wx.HORIZONTAL)
        fgSizer4.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.lblChangeGT = wx.StaticText(self, wx.ID_ANY, u"Value >", wx.DefaultPosition, wx.DefaultSize, 0)
        self.lblChangeGT.Wrap(-1)
        fgSizer4.Add(self.lblChangeGT, 0, wx.ALL, 5)

        self.txtVChangeGT = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(248, -1), 0)
        fgSizer4.Add(self.txtVChangeGT, 0, wx.ALL, 5)

        self.lblChangeLT = wx.StaticText(self, wx.ID_ANY, u"Value <", wx.DefaultPosition, wx.DefaultSize, 0)
        self.lblChangeLT.Wrap(-1)
        fgSizer4.Add(self.lblChangeLT, 0, wx.ALL, 5)

        self.txtVChangeLT = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(248, -1), 0)
        fgSizer4.Add(self.txtVChangeLT, 0, wx.ALL, 5)

        sbValChange.Add(fgSizer4, 1, wx.EXPAND, 5)

        bsValChange.Add(sbValChange, 1, wx.EXPAND, 5)

        bSizer3.Add(bsValChange, 1, wx.EXPAND, 5)

        self.chkToggleFilterSelection = wx.CheckBox(self, wx.ID_ANY, u"Filter from previous filter", wx.DefaultPosition,
                                                    wx.DefaultSize, 0)
        bSizer3.Add(self.chkToggleFilterSelection, 0, wx.ALL, 5)

        bsButtons = wx.BoxSizer(wx.HORIZONTAL)

        self.btnClear = wx.Button(self, wx.ID_ANY, u"Clear Filter", wx.DefaultPosition, wx.Size(64, 23), 0)
        bsButtons.Add(self.btnClear, 0, wx.ALL, 5)

        self.m_panel1 = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(-1, 23), wx.TAB_TRAVERSAL)
        bsButtons.Add(self.m_panel1, 1, wx.EXPAND | wx.ALL, 5)

        self.btnOK = wx.Button(self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.Size(64, 23), 0)
        bsButtons.Add(self.btnOK, 0, wx.ALL, 5)

        self.btnCancel = wx.Button(self, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.Size(64, 23), 0)
        bsButtons.Add(self.btnCancel, 0, wx.ALL, 5)

        self.btnApply = wx.Button(self, wx.ID_ANY, u"Apply", wx.DefaultPosition, wx.Size(64, 23), 0)
        bsButtons.Add(self.btnApply, 0, wx.ALL, 5)

        bSizer3.Add(bsButtons, 1, wx.EXPAND, 0)

        bSizer1.Add(bSizer3, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.txtThreshValGT.Bind(wx.EVT_SET_FOCUS, self.onSetFocus)
        self.txtThreshValLT.Bind(wx.EVT_SET_FOCUS, self.onSetFocus)
        self.txtGapsVal.Bind(wx.EVT_SET_FOCUS, self.onSetFocus)
        self.cbGapTime.Bind(wx.EVT_SET_FOCUS, self.onSetFocus)
        self.dpBefore.Bind(wx.EVT_SET_FOCUS, self.onSetFocus)
        self.dpAfter.Bind(wx.EVT_SET_FOCUS, self.onSetFocus)
        self.txtVChangeGT.Bind(wx.EVT_SET_FOCUS, self.onSetFocus)
        self.txtVChangeLT.Bind(wx.EVT_SET_FOCUS, self.onSetFocus)
        self.chkToggleFilterSelection.Bind(wx.EVT_CHECKBOX, self.onCheckBox)
        self.btnClear.Bind(wx.EVT_BUTTON, self.onBtnClearButton)
        self.btnOK.Bind(wx.EVT_BUTTON, self.onBtnOKButton)
        self.btnCancel.Bind(wx.EVT_BUTTON, self.onBtnCancelButton)
        self.btnApply.Bind(wx.EVT_BUTTON, self.onBtnApplyButton)


    def __del__(self):
        pass


    # Virtual event handlers, overide them in your derived class
    def onSetFocus(self, event):
        event.Skip()


    def onCheckBox(self, event):
        event.Skip()


    def onBtnClearButton(self, event):
        event.Skip()


    def onBtnOKButton(self, event):
        event.Skip()


    def onBtnCancelButton(self, event):
        event.Skip()


    def onBtnApplyButton(self, event):
        event.Skip()


