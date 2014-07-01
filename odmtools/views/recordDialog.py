# -*- coding: utf-8 -*- 

# ##########################################################################
## Python code generated with wxFormBuilder (version Jun  5 2014)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
from odmtools.common import file_new, edit, script

###########################################################################
## Class recordDialog
###########################################################################

class recordDialog(wx.Dialog):
    def __init__(self, script, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"Recoding options", pos=wx.DefaultPosition,
                           size=wx.Size(258, 125), style=wx.DEFAULT_DIALOG_STYLE)
        self.initDialog()
        self.script = script

    def initDialog(self):
        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        bSizer5 = wx.BoxSizer(wx.VERTICAL)

        bSizer6 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText1 = wx.StaticText(self, wx.ID_ANY, u"Record Service", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText1.Wrap(-1)
        bSizer6.Add(self.m_staticText1, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        bSizer5.Add(bSizer6, 1, wx.ALIGN_CENTER, 5)

        self.m_toolBar2 = wx.ToolBar(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_FLAT | wx.TB_TEXT)
        self.m_newTool = self.m_toolBar2.AddLabelTool(wx.ID_ANY, u"New", file_new.GetBitmap(), wx.NullBitmap, wx.ITEM_NORMAL,
                                                      wx.EmptyString, wx.EmptyString, None)

        self.m_openTool = self.m_toolBar2.AddLabelTool(wx.ID_ANY, u"Open", edit.GetBitmap(), wx.NullBitmap, wx.ITEM_NORMAL,
                                                       wx.EmptyString, wx.EmptyString, None)

        self.m_appendTool = self.m_toolBar2.AddLabelTool(wx.ID_ANY, u"Continue editing", script.GetBitmap(), wx.NullBitmap,
                                                         wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None)

        self.m_toolBar2.Realize()

        bSizer5.Add(self.m_toolBar2, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.SetSizer(bSizer5)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.Bind(wx.EVT_TOOL, self.onNewToolClicked, id=self.m_newTool.GetId())
        self.Bind(wx.EVT_TOOL, self.onOpenToolClicked, id=self.m_openTool.GetId())
        self.Bind(wx.EVT_TOOL, self.onAppendToolClicked, id=self.m_appendTool.GetId())

    # Virtual event handlers, overide them in your derived class

    def onNewToolClicked(self, event):


        event.Skip()
    def onOpenToolClicked(self, event):

        event.Skip()
    def onAppendToolClicked(self, event):

        event.Skip()
