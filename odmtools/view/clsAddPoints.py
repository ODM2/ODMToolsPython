# -*- coding: utf-8 -*- 

# ##########################################################################
# # Python code generated with wxFormBuilder (version Jun  5 2014)
# # http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.combo
import wx.lib.masked
import wx.lib.agw.buttonpanel as BP

from odmtools.controller.olvAddPoint import OLVAddPoint
from odmtools.lib.ObjectListView import EVT_CELL_EDIT_STARTING, EVT_CELL_EDIT_FINISHING

#from odmtools.common.icons.icons import add, stop_edit, deletered
from odmtools.common.icons.icons4addpoint import *




###########################################################################
## Class AddPoints
###########################################################################

class AddPoints(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title="- ODMTools -", pos=wx.DefaultPosition, size=(1175, 425),
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        mainPanel = wx.Panel(self, -1)
        vSizer = wx.BoxSizer(wx.VERTICAL)
        mainPanel.SetSizer(vSizer)

        self.olv = None
        self.titleBar = None
        self.selectedObject = None

        self.buildButtonPanel(mainPanel)
        self.initiateObjectListView(mainPanel)
        self.sb = self.CreateStatusBar()

        vSizer.Add(self.titleBar, 0, wx.EXPAND | wx.ALL)
        vSizer.Add(self.olv, 1, wx.EXPAND | wx.ALL, 5)

        self.titleBar.DoLayout()
        vSizer.Layout()

        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onSelected, id=self.olv.GetId())


    def buildButtonPanel(self, mainPanel):
        """

        :param mainPanel:
        :return:
        """
        self.titleBar = BP.ButtonPanel(mainPanel, -1, "Add points to ODMTools\n"
                                                      "Pressing 'c' when editing time "
                                                      "will set the value to the localtime", alignment=BP.BP_ALIGN_LEFT)

        addRowBtn = BP.ButtonInfo(self.titleBar, wx.NewId(), plus_6_64.GetBitmap(), text="Add Row")
        deleteRowBtn = BP.ButtonInfo(self.titleBar, wx.NewId(), minus_6_64.GetBitmap(), text="Delete Row")
        clearRowsBtn = BP.ButtonInfo(self.titleBar, wx.NewId(), delete_64.GetBitmap(), text="Clear All")
        csvUploadBtn = BP.ButtonInfo(self.titleBar, wx.NewId(), csv_64.GetBitmap(), text="Upload CSV")
        finishedBtn = BP.ButtonInfo(self.titleBar, wx.NewId(), exit_64.GetBitmap(), text="Finished")


        self.titleBar.AddButton(addRowBtn)
        self.titleBar.AddButton(deleteRowBtn)
        self.titleBar.AddButton(clearRowsBtn)
        self.titleBar.AddButton(csvUploadBtn)
        self.titleBar.AddButton(finishedBtn)

        self.Bind(wx.EVT_BUTTON, self.onAddBtn, addRowBtn)
        self.Bind(wx.EVT_BUTTON, self.onDeleteBtn, deleteRowBtn)
        self.Bind(wx.EVT_BUTTON, self.onClearAllBtn, clearRowsBtn)
        self.Bind(wx.EVT_BUTTON, self.onUploadBtn, csvUploadBtn)
        self.Bind(wx.EVT_BUTTON, self.onFinishedBtn, finishedBtn)

    def initiateObjectListView(self, mainPanel):
        """

        :param mainPanel:
        :return:
        """
        self.olv = OLVAddPoint(parent=mainPanel, id=wx.ID_ANY, style=wx.LC_REPORT)
        self.olv.Bind(EVT_CELL_EDIT_STARTING, self.onEdit)
        self.olv.Bind(EVT_CELL_EDIT_FINISHING, self.onEditDone)
        self.olv.Bind(wx.EVT_LIST_COL_CLICK, self.onColClick)


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

    def onTestBtn(self, event):
        event.Skip()

    def onSelected(self, event):
        event.Skip()

    def onEdit(self, event):
        print "Began editting!", event.cellValue
        if event.subItemIndex == 0:
            event.Veto()

    def onEditDone(self, event):
        print "Finished Editing", event.cellValue

    def onColClick(self, event):
        pass

    def __del__(self):
        pass




