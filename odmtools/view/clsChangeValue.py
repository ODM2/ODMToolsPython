# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Oct  2 2014)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class clsChangeValue
###########################################################################

class clsChangeValue(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"Change Value", pos=wx.DefaultPosition,
                           size=wx.DefaultSize,
                           style=wx.CAPTION | wx.CLOSE_BOX | wx.DEFAULT_DIALOG_STYLE | wx.STAY_ON_TOP)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        bsMain = wx.BoxSizer(wx.VERTICAL)

        bsTop = wx.BoxSizer(wx.VERTICAL)

        self.stMessage = wx.StaticText(self, wx.ID_ANY,
                                       u"Selected data values on the plot will be "
                                       u"\nmodified by the following method and value",
                                       wx.DefaultPosition, wx.DefaultSize, 0)
        self.stMessage.Wrap(-1)
        bsTop.Add(self.stMessage, 0, wx.ALL | wx.EXPAND, 5)

        bsMain.Add(bsTop, 0, wx.EXPAND, 5)

        fgSizerMiddle = wx.FlexGridSizer(2, 2, 5, 15)
        fgSizerMiddle.AddGrowableCol(1)
        fgSizerMiddle.SetFlexibleDirection(wx.BOTH)
        fgSizerMiddle.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.stMethod = wx.StaticText(self, wx.ID_ANY, u"Method", wx.DefaultPosition, wx.DefaultSize, 0)
        self.stMethod.Wrap(-1)
        fgSizerMiddle.Add(self.stMethod, 0, wx.ALL, 5)

        cbValueChoices = [wx.EmptyString, u"Add", u"Subtract", u"Multiply", u"Set to"]
        self.cbValue = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cbValueChoices, 0)
        self.cbValue.SetSelection(0)
        fgSizerMiddle.Add(self.cbValue, 1, wx.ALL | wx.EXPAND, 5)

        self.stValue = wx.StaticText(self, wx.ID_ANY, u"Value", wx.DefaultPosition, wx.DefaultSize, 0)
        self.stValue.Wrap(-1)
        fgSizerMiddle.Add(self.stValue, 0, wx.ALL, 5)

        self.txtValue = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizerMiddle.Add(self.txtValue, 1, wx.ALL | wx.EXPAND, 5)

        bsMain.Add(fgSizerMiddle, 1, wx.ALL | wx.EXPAND, 5)

        bsBottom = wx.BoxSizer(wx.HORIZONTAL)

        self.btnOk = wx.Button(self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0)
        bsBottom.Add(self.btnOk, 1, wx.ALL, 5)

        self.btnCancel = wx.Button(self, wx.ID_ANY, u"CANCEL", wx.DefaultPosition, wx.DefaultSize, 0)
        bsBottom.Add(self.btnCancel, 1, wx.ALL, 5)

        bsMain.Add(bsBottom, 0, wx.EXPAND, 5)

        self.SetSizer(bsMain)
        self.Layout()
        bsMain.Fit(self)

        self.Centre(wx.BOTH)

        # Connect Events
        self.btnOk.Bind(wx.EVT_BUTTON, self.OnBtnOk)
        self.btnCancel.Bind(wx.EVT_BUTTON, self.OnBtnCancel)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def OnBtnOk(self, event):
        event.Skip()

    def OnBtnCancel(self, event):
        event.Skip()

