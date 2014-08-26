# -*- coding: utf-8 -*- 

# ##########################################################################
## Python code generated with wxFormBuilder (version Jun  5 2014)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
from ObjectListView import FastObjectListView as objectListView, ColumnDefn
from odmtools.common.icons.icons import add

###########################################################################
## Class AddPoints
###########################################################################

class AddPoints(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                           size=wx.Size(510, 259), style=wx.DEFAULT_DIALOG_STYLE | wx.CLOSE_BOX)

        self.m_toolBar1 = wx.ToolBar(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL)
        self.m_tool1 = self.m_toolBar1.AddLabelTool(wx.ID_ANY, u"tool", add.GetBitmap())
        #
        # self.m_tool2 = self.m_toolBar1.AddLabelTool(wx.ID_ANY, u"tool", wx.NullBitmap, wx.NullBitmap, wx.ITEM_NORMAL,
        #                                             wx.EmptyString, wx.EmptyString, None)
        #
        # self.m_tool3 = self.m_toolBar1.AddLabelTool(wx.ID_ANY, u"tool", wx.NullBitmap, wx.NullBitmap, wx.ITEM_NORMAL,
        #                                             wx.EmptyString, wx.EmptyString, None)
        #
        # self.m_tool4 = self.m_toolBar1.AddLabelTool(wx.ID_ANY, u"tool", wx.NullBitmap, wx.NullBitmap, wx.ITEM_NORMAL,
        #                                             wx.EmptyString, wx.EmptyString, None)

        self.m_toolBar1.Realize()

        self.olv = objectListView(self, wx.ID_ANY, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.olv.SetEmptyListMsg("Nothing to see here... yet!")
        #elements = {
            
        #}
        #self.olv.SetColumns([ColumnDefn(key, valueGetter=value for key, value in elements])])
        self.olv.SetObjects(None)

        #self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        olvSizer = wx.BoxSizer(wx.HORIZONTAL)
        olvSizer.Add(self.olv, 1, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 5)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(olvSizer, 1, wx.EXPAND, 5)
        mainSizer.Add(self.m_toolBar1, 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(mainSizer)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        # self.Bind(wx.EVT_TOOL, self.onClick, id=self.m_tool1.GetId())
        # self.Bind(wx.EVT_TOOL, self.onClose, id=self.m_tool2.GetId())

    def __del__(self):
        pass


    # Virtual event handlers, overide them in your derived class
    def onClick(self, event):
        event.Skip()

    def onClose(self, event):
        event.Skip()

class Example(wx.Frame):
    def __init__(self, parent, *args, **kwargs):
        wx.Frame.__init__(self, parent, *args, **kwargs)
        m = AddPoints(parent)
        m.ShowModal()

if __name__ == '__main__':
    app = wx.App(useBestVisual=True)
    ex = Example(None)
    app.MainLoop()
