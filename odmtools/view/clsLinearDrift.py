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
## Class LinearDrift
###########################################################################

class clsLinearDrift(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"Linear Drift Correction", pos=wx.DefaultPosition,
                           size=wx.Size(293, 153), style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        bsMain = wx.BoxSizer(wx.VERTICAL)

        bsTop = wx.BoxSizer(wx.VERTICAL)

        self.stMessage = wx.StaticText(
            self, wx.ID_ANY, u"Enter a negative value to move points down "
                             u"\nEnter positive values to move points up", wx.DefaultPosition, wx.DefaultSize, 0)
        self.stMessage.Wrap(-1)
        bsTop.Add(self.stMessage, 1, wx.ALL, 5)

        bsMain.Add(bsTop, 1, wx.EXPAND, 5)

        bsMiddle = wx.BoxSizer(wx.HORIZONTAL)

        self.stFinalGap = wx.StaticText(self, wx.ID_ANY, u"Final Gap", wx.DefaultPosition, wx.DefaultSize, 0)
        self.stFinalGap.Wrap(-1)
        bsMiddle.Add(self.stFinalGap, 0, wx.ALL | wx.EXPAND, 5)

        self.txtFinalGapValue = wx.TextCtrl(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0)
        bsMiddle.Add(self.txtFinalGapValue, 1, wx.ALL | wx.EXPAND, 5)

        bsMain.Add(bsMiddle, 1, wx.EXPAND, 5)

        bsBottom = wx.BoxSizer(wx.HORIZONTAL)

        self.btnOK = wx.Button(self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0)
        bsBottom.Add(self.btnOK, 1, wx.ALL | wx.EXPAND, 5)

        self.btnCancel = wx.Button(self, wx.ID_ANY, u"CANCEL", wx.DefaultPosition, wx.DefaultSize, 0)
        bsBottom.Add(self.btnCancel, 1, wx.ALL | wx.EXPAND, 5)

        bsMain.Add(bsBottom, 1, wx.EXPAND, 5)

        self.SetSizer(bsMain)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.btnOK.Bind(wx.EVT_BUTTON, self.OnBtnOKButton)
        self.btnCancel.Bind(wx.EVT_BUTTON, self.OnBtnCancelButton)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def OnBtnOKButton(self, event):
        event.Skip()

    def OnBtnCancelButton(self, event):
        event.Skip()

