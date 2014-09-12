# -*- coding: utf-8 -*- 

# ##########################################################################
# # Python code generated with wxFormBuilder (version Jun  5 2014)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################
from collections import OrderedDict

import wx
import wx.xrc
import wx.combo
import wx.lib.agw.buttonpanel as BP

from ObjectListView import FastObjectListView as OLV, ColumnDefn
from odmtools.common.icons.icons import add, stop_edit, deletered
from odmtools.common.icons.newIcons import appbar_exit, appbar_folder_open, appbar_table_add, appbar_table_delete


###########################################################################
## Class AddPoints
###########################################################################

class AddPoints(wx.MiniFrame):
    def __init__(self, parent):
        wx.MiniFrame.__init__(self, parent, id=wx.ID_ANY, title="- ODMTools -",
                              pos=wx.DefaultPosition, size=(1280, 300),
                              style= wx.DEFAULT_FRAME_STYLE)

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
        self.titleBar = BP.ButtonPanel(mainPanel, -1, "Add points to ODMTools", alignment=BP.BP_ALIGN_LEFT)

        addRowBtn = BP.ButtonInfo(self.titleBar, wx.NewId(), appbar_table_add.GetBitmap(), text="Add Row")
        deleteRowBtn = BP.ButtonInfo(self.titleBar, wx.NewId(), appbar_table_delete.GetBitmap(), text="Delete Row")
        csvUploadBtn = BP.ButtonInfo(self.titleBar, wx.NewId(), appbar_folder_open.GetBitmap(), text="Upload CSV")
        finishedBtn = BP.ButtonInfo(self.titleBar, wx.NewId(), appbar_exit.GetBitmap(), text="Finished")

        self.titleBar.AddButton(addRowBtn)
        self.titleBar.AddButton(deleteRowBtn)
        self.titleBar.AddButton(csvUploadBtn)
        self.titleBar.AddButton(finishedBtn)

        self.Bind(wx.EVT_BUTTON, self.onAddBtn, addRowBtn)
        self.Bind(wx.EVT_BUTTON, self.onDeleteBtn, deleteRowBtn)
        self.Bind(wx.EVT_BUTTON, self.onUploadBtn, csvUploadBtn)
        self.Bind(wx.EVT_BUTTON, self.onFinishedBtn, finishedBtn)

    def initiateObjectListView(self, mainPanel):
        """

        :param mainPanel:
        :return:
        """
        self.olv = OLV(mainPanel, wx.ID_ANY, style=wx.LC_REPORT)
        self.olv.useAlternateBackColors = True
        self.olv.oddRowsBackColor = wx.Colour(191, 239, 255)
        self.olv.cellEditMode = OLV.CELLEDIT_DOUBLECLICK
        self.olv.SetEmptyListMsg("Add points either by csv or by adding a new row")
        self.buildOlv()
        #self.olv.CreateCheckStateColumn()
        #self.olv.SetObjects([self.Points('1'), self.Points('2'), self.Points('3'), self.Points('4')])
        self.olv.SetObjects(None)

    def buildOlv(self):
        """

        :return:
        """
        columns = [ColumnDefn("DataValue", "left", -1, valueGetter="dataValue", minimumWidth=125),
                   ColumnDefn("ValueAccuracy", "left", -1, valueGetter="valueAccuracy", minimumWidth=125),
                   ColumnDefn("LocalDateTime", "left", -1, valueGetter="localDateTime", minimumWidth=125),
                   ColumnDefn("UTCOffset", "left", -1, valueGetter="utcOffSet", minimumWidth=125),
                   ColumnDefn("DateTimeUTC", "left", -1, valueGetter="dateTimeUTC", minimumWidth=125),
                   ColumnDefn("OffsetValue", "left", -1, valueGetter="offSetValue", minimumWidth=125),
                   ColumnDefn("OffsetType", "left", -1, valueGetter="offSetType", minimumWidth=125),
                   ColumnDefn("CensorCode", "left", -1, valueGetter="censorCode", minimumWidth=125, cellEditorCreator=self.censorCodeEditor),
                   ColumnDefn("QualifierCode", "left", -1, valueGetter="qualifierCode", minimumWidth=125),
                   ColumnDefn("LabSampleCode", "left", -1, valueGetter="labSampleCode", minimumWidth=125)]
        self.olv.SetColumns(columns)

    def censorCodeEditor(self, olv, rowIndex, subItemIndex):
        """

        :param olv:
        :param rowIndex:
        :param subItemIndex:
        :return:
        """
        odcb = SensorCodeComboBox(olv)
        # OwnerDrawnComboxBoxes don't generate EVT_CHAR so look for keydown instead
        odcb.Bind(wx.EVT_KEY_DOWN, olv._HandleChar)
        return odcb

    # Virtual event handlers, override them in your derived class
    def onAddBtn(self, event):
        event.Skip()
    def onDeleteBtn(self, event):
        event.Skip()
    def onUploadBtn(self, event):
        event.Skip()
    def onFinishedBtn(self, event):
        event.Skip()
    def onSelected(self, event):
        event.Skip()

    def __del__(self):
        pass

    class Points(object):
        """

        """

        def __init__(self, dataValue=" ", valueAccuracy=" ", localDateTime=" ", utcOffSet=" ", dateTimeUTC=" ",
                     offSetValue=" ", offSetType=" ", censorCode=" ", qualifierCode=" ", labSampleCode=" "):
            self.dataValue = dataValue
            self.valueAccuracy = valueAccuracy
            self.localDateTime = localDateTime
            self.utcOffSet = utcOffSet
            self.dateTimeUTC = dateTimeUTC
            self.offSetValue = offSetValue
            self.offSetType = offSetType
            self.censorCode = censorCode
            self.qualifierCode = qualifierCode
            self.labSampleCode = labSampleCode


class SensorCodeComboBox(wx.combo.OwnerDrawnComboBox):
    """

    """
    def __init__(self, *args, **kwargs):
        self.popupRowHeight = kwargs.pop("popupRowHeight", 24)
        kwargs['style'] = kwargs.get('style', 0) | wx.CB_READONLY
        kwargs['choices'] = ['gt', 'lt', 'nc', 'nd', 'pnq']
        self.evenRowBackground = kwargs.pop("evenRowBackground", wx.WHITE)
        self.oddRowBackground = kwargs.pop("oddRowBackground", wx.Colour(191, 239, 255))
        wx.combo.OwnerDrawnComboBox.__init__(self, *args, **kwargs)

    def OnDrawBackground(self, dc, rect, item, flags):
        # If the item is selected, or we are painting the combo control itself, then use
        # the default rendering.
        if flags & (wx.combo.ODCB_PAINTING_CONTROL | wx.combo.ODCB_PAINTING_SELECTED):
            wx.combo.OwnerDrawnComboBox.OnDrawBackground(self, dc, rect, item, flags)
            return

        # Otherwise, draw every other background with different colour.
        if item & 1:
            backColour = self.oddRowBackground
        else:
            backColour = self.evenRowBackground
        dc.SetBrush(wx.Brush(backColour))
        dc.SetPen(wx.Pen(backColour))
        dc.DrawRectangleRect(rect)
