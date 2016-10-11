# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc


###########################################################################
## Class dlgFill
###########################################################################

class dlgFill(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                           size=wx.Size(315, 217), style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHintsSz(wx.Size(315, 217), wx.Size(315, 217))

        bsForm = wx.BoxSizer(wx.VERTICAL)

        self.lblInstructions = wx.StaticText(self, wx.ID_ANY,
                                             u"This function fills any gaps less than the gap duration with a no-data value at the fill frequency",
                                             wx.DefaultPosition, wx.DefaultSize, 0)
        self.lblInstructions.Wrap(300)
        bsForm.Add(self.lblInstructions, 0, wx.ALL, 5)

        fgSizer1 = wx.FlexGridSizer(0, 3, 0, 0)
        fgSizer1.SetFlexibleDirection(wx.BOTH)
        fgSizer1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.lblGap = wx.StaticText(self, wx.ID_ANY, u"Gap Duration:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.lblGap.Wrap(-1)
        fgSizer1.Add(self.lblGap, 0, wx.ALL, 5)

        self.txtGap = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer1.Add(self.txtGap, 0, wx.ALL, 5)

        cbGapChoices = [u"second", u"minute", u"hour", u"days", u"week", u"month", u"day", u"year"]
        self.cbGap = wx.ComboBox(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, cbGapChoices, 0)
        self.cbGap.SetSelection(1)
        fgSizer1.Add(self.cbGap, 1, wx.ALL, 5)

        self.lblFill = wx.StaticText(self, wx.ID_ANY, u"Fill Frequency:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.lblFill.Wrap(-1)
        fgSizer1.Add(self.lblFill, 0, wx.ALL, 5)

        self.txtFill = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer1.Add(self.txtFill, 0, wx.ALL, 5)

        cbFillChoices = [u"second", u"minute", u"hour", u"day", u"week", u"month", u"year"]
        self.cbFill = wx.ComboBox(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, cbFillChoices, 0)
        self.cbFill.SetSelection(1)
        fgSizer1.Add(self.cbFill, 1, wx.ALL, 5)

        bsForm.Add(fgSizer1, 1, wx.EXPAND, 5)

        m_sdbSizer1 = wx.StdDialogButtonSizer()
        self.m_sdbSizer1OK = wx.Button(self, wx.ID_OK)
        m_sdbSizer1.AddButton(self.m_sdbSizer1OK)
        self.m_sdbSizer1Cancel = wx.Button(self, wx.ID_CANCEL)
        m_sdbSizer1.AddButton(self.m_sdbSizer1Cancel)
        m_sdbSizer1.Realize();

        bsForm.Add(m_sdbSizer1, 1, wx.EXPAND, 5)

        self.SetSizer(bsForm)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.m_sdbSizer1Cancel.Bind(wx.EVT_BUTTON, self.OnCancelBtn)
        self.m_sdbSizer1OK.Bind(wx.EVT_BUTTON, self.onOKBtn)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def OnCancelBtn(self, event):
        event.Skip()

    def onOKBtn(self, event):
        event.Skip()


