# -*- coding: utf-8 -*- 

# ##########################################################################
## Python code generated with wxFormBuilder (version Feb 26 2014)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MyFrame1
###########################################################################

class MyFrame1(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(500, 300), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        self.m_panel1 = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer1.Add(self.m_panel1, 1, wx.EXPAND | wx.ALL, 5)

        self.addbutton = wx.Button(self, wx.ID_ANY, u"Add ", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.addbutton, 0, wx.ALL, 5)

        self.removebutton = wx.Button(self, wx.ID_ANY, u"Remove ", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.removebutton, 0, wx.ALL, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

        self.Bind(wx.EVT_BUTTON, self.onAdd, id = self.addbutton.Id)
        self.Bind(wx.EVT_BUTTON, self.onRemove, id = self.removebutton.Id)


    def onAdd(self, event):
        pass


    def onRemove(self, event):
        pass

    def __del__(self):
        pass
	

