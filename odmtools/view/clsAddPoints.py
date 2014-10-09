# -*- coding: utf-8 -*- 

# ##########################################################################
# # Python code generated with wxFormBuilder (version Jun  5 2014)
# # http://www.wxformbuilder.org/
# #
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.combo
import wx.lib.masked
import wx.lib.agw.buttonpanel as BP

from odmtools.controller.olvAddPoint import OLVAddPoint
from odmtools.lib.ObjectListView import EVT_CELL_EDIT_STARTING, EVT_CELL_EDIT_FINISHING
from odmtools.common.icons.icons4addpoint import *





###########################################################################
## Class AddPoints
###########################################################################

class AddPoints(wx.Frame):
    def __init__(self, parent, **kwargs):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title="- ODMTools -", pos=wx.DefaultPosition,
                          size=(1055, 425), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        mainPanel = wx.Panel(self, -1)
        vSizer = wx.BoxSizer(wx.VERTICAL)
        mainPanel.SetSizer(vSizer)

        self.olv = None
        self.titleBar = None
        self.selectedObject = None

        self.buildButtonPanel(mainPanel)
        self.initiateObjectListView(mainPanel, **kwargs)
        self.sb = self.CreateStatusBar()

        vSizer.Add(self.titleBar, 0, wx.EXPAND | wx.ALL)
        vSizer.Add(self.olv, 1, wx.EXPAND | wx.ALL, 5)

        self.titleBar.DoLayout()
        vSizer.Layout()


    def buildButtonPanel(self, mainPanel):
        """

        :param mainPanel:
        :return:
        """
        self.titleBar = BP.ButtonPanel(mainPanel, -1, "Add points to ODMTools\n"
                                                      "Pressing 'c' when editing time "
                                                      "will set the value to the localtime",
                                       alignment=BP.BP_ALIGN_LEFT)

        self.addRowBtn = BP.ButtonInfo(self.titleBar, wx.NewId(), plus_6_64.GetBitmap(), text="Add Row")
        self.deleteRowBtn = BP.ButtonInfo(self.titleBar, wx.NewId(), minus_6_64.GetBitmap(), text="Delete Row")
        self.clearRowsBtn = BP.ButtonInfo(self.titleBar, wx.NewId(), delete_64.GetBitmap(), text="Clear All")
        self.csvUploadBtn = BP.ButtonInfo(self.titleBar, wx.NewId(), csv_64.GetBitmap(), text="Upload CSV")
        self.infoBtn = BP.ButtonInfo(self.titleBar, wx.NewId(), info_5_32.GetBitmap(), text="Format Guide")
        self.finishedBtn = BP.ButtonInfo(self.titleBar, wx.NewId(), exit_64.GetBitmap(), text="Finished")

        self.titleBar.AddButton(self.addRowBtn)
        self.titleBar.AddButton(self.deleteRowBtn)
        self.titleBar.AddButton(self.clearRowsBtn)
        self.titleBar.AddButton(self.csvUploadBtn)
        self.titleBar.AddButton(self.infoBtn)
        self.titleBar.AddButton(self.finishedBtn)

        self.Bind(wx.EVT_BUTTON, self.onAddBtn, self.addRowBtn)
        self.Bind(wx.EVT_BUTTON, self.onDeleteBtn, self.deleteRowBtn)
        self.Bind(wx.EVT_BUTTON, self.onClearAllBtn, self.clearRowsBtn)
        self.Bind(wx.EVT_BUTTON, self.onUploadBtn, self.csvUploadBtn)
        self.Bind(wx.EVT_BUTTON, self.onInfoBtn, self.infoBtn)
        self.Bind(wx.EVT_BUTTON, self.onFinishedBtn, self.finishedBtn)

    def initiateObjectListView(self, mainPanel, **kwargs):
        """

        :param mainPanel:
        :return:
        """
        self.olv = OLVAddPoint(parent=mainPanel, id=wx.ID_ANY, style=wx.LC_REPORT, **kwargs)
        self.olv.Bind(EVT_CELL_EDIT_STARTING, self.onEdit)
        self.olv.Bind(EVT_CELL_EDIT_FINISHING, self.onEditFinish)
        #self.olv.Bind(wx.EVT_LIST_COL_CLICK, self.onColClick)
        self.olv.Bind(wx.EVT_LIST_ITEM_FOCUSED, self.onSelected)
        #self.olv.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onTooltip)
        self.olv.Bind(wx.EVT_CHAR, self.onChar)


    # Virtual event handlers, override them in your derived class
    def onAddBtn(self, event):
        event.Skip()

    def onClearAllBtn(self, event):
        event.Skip()

    def onDeleteBtn(self, event):
        event.Skip()

    def onUploadBtn(self, event):
        event.Skip()

    def onFinishedBtn(self, event):
        event.Skip()

    def onInfoBtn(self, event):
        event.Skip()

    def onSelected(self, event):
        event.Skip()

    def onTooltip(self, event):
        event.Skip()

    def onChar(self, event):
        pass

    def onEdit(self, event):
        ## Ignore editing on first cell
        if event.subItemIndex == 0:
            event.Veto()

    def onEditFinish(self, event):
        pass

    def onColClick(self, event):
        ## Ignore col clicking
        pass

    def __del__(self):
        pass


