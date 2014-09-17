# -*- coding: utf-8 -*- 

# ##########################################################################
# # Python code generated with wxFormBuilder (version Jun  5 2014)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################
from collections import OrderedDict

import wx
from wx.lib import masked
import wx.xrc
import wx.combo
import wx.lib.masked
import wx.lib.agw.buttonpanel as BP

from datetime import datetime
from odmtools.lib.ObjectListView import FastObjectListView as OLV, ColumnDefn
from odmtools.lib.ObjectListView import EVT_CELL_EDIT_STARTING, EVT_CELL_EDIT_FINISHING
#from odmtools.common.icons.icons import add, stop_edit, deletered
from odmtools.common.icons.icons4addpoint import *


## Specific Settings
NO_DATA_VALUE = u'-9999'

###########################################################################
## Class AddPoints
###########################################################################

class AddPoints(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title="- ODMTools -",
                              pos=wx.DefaultPosition, size=(1125, 300),
                              style= wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL )

        mainPanel = wx.Panel(self, -1)
        vSizer = wx.BoxSizer(wx.VERTICAL)
        mainPanel.SetSizer(vSizer)

        self.olv = None
        self.titleBar = None
        self.selectedObject = None

        ## Cell Verification and Editors Init
        self.vfyDataValue = None
        self.vfyValueAcc = None
        self.localtime2Str = None
        self.timeEditor = None


        self.buildButtonPanel(mainPanel)
        self.initiateCellValidators()
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
        #TestBtn = BP.ButtonInfo(self.titleBar, wx.NewId(), appbar_exit.GetBitmap(), text="Test")


        self.titleBar.AddButton(addRowBtn)
        self.titleBar.AddButton(deleteRowBtn)
        self.titleBar.AddButton(csvUploadBtn)
        self.titleBar.AddButton(finishedBtn)
        self.titleBar.AddButton(clearRowsBtn)

        self.Bind(wx.EVT_BUTTON, self.onAddBtn, addRowBtn)
        self.Bind(wx.EVT_BUTTON, self.onDeleteBtn, deleteRowBtn)
        self.Bind(wx.EVT_BUTTON, self.onUploadBtn, csvUploadBtn)
        self.Bind(wx.EVT_BUTTON, self.onFinishedBtn, finishedBtn)
        self.Bind(wx.EVT_BUTTON, self.onClearAllBtn, clearRowsBtn)


    def initiateCellValidators(self):
        self.vfyDataValue = CellEdit().verifyDataValue
        self.vfyValueAcc = CellEdit().verifyValueAccuracy
        self.localtime2Str = CellEdit().localTimeToString
        self.vfyCensorCode = CellEdit().verifyCensorCode

        self.timeEditor = CellEdit().localTimeEditor
        self.censorEditor = CellEdit().censorCodeEditor

    def initiateObjectListView(self, mainPanel):
        """

        :param mainPanel:
        :return:
        """
        self.olv = OLV(mainPanel, wx.ID_ANY, style=wx.LC_REPORT)
        self.olv.SetEmptyListMsg("Add points either by csv or by adding a new row")
        self.olv.AddNamedImages("error", x_mark_16.GetBitmap(), x_mark_32.GetBitmap())
        self.olv.AddNamedImages("star", star_16.GetBitmap(), star_32.GetBitmap())
        self.buildOlv()
        self.olv.useAlternateBackColors = True
        #self.olv.oddRowsBackColor = wx.Colour(255, 239, 255)
        self.olv.oddRowsBackColor = wx.Colour(191, 239, 255)
        self.olv.cellEditMode = OLV.CELLEDIT_DOUBLECLICK
        self.olv.Bind(EVT_CELL_EDIT_STARTING, self.onEdit)
        self.olv.Bind(EVT_CELL_EDIT_FINISHING, self.onEditDone)
        self.olv.Bind(wx.EVT_LIST_COL_CLICK, self.onColClick)

    def buildOlv(self):
        columns = [
            ColumnDefn("", "left", -1, valueGetter=""),
            ColumnDefn("DataValue", "left", -1, valueGetter="dataValue", minimumWidth=100,
                          imageGetter=self.vfyDataValue, headerImage="star"),
            ColumnDefn("Time", "left", -1, valueGetter="time", minimumWidth=75,
                      cellEditorCreator=self.timeEditor, stringConverter=self.localtime2Str, headerImage="star"),
            ColumnDefn("Date", "left", -1, valueGetter="date", minimumWidth=85, headerImage="star"),
            ColumnDefn("UTCOffset", "left", -1, valueGetter="utcOffSet", minimumWidth=100, headerImage="star"),
            ColumnDefn("CensorCode", "left", -1, valueGetter="censorCode", minimumWidth=110,
                       cellEditorCreator=self.censorEditor, imageGetter=self.vfyCensorCode, headerImage="star"),
            ColumnDefn("ValueAccuracy", "left", -1, valueGetter="valueAccuracy", minimumWidth=100),
            ColumnDefn("DateTimeUTC", "left", -1, valueGetter="dateTimeUTC", minimumWidth=100),
            ColumnDefn("OffsetValue", "left", -1, valueGetter="offSetValue", minimumWidth=100),
            ColumnDefn("OffsetType", "left", -1, valueGetter="offSetType", minimumWidth=100),
            ColumnDefn("QualifierCode", "left", -1, valueGetter="qualifierCode", minimumWidth=100),
            ColumnDefn("LabSampleCode", "left", -1, valueGetter="labSampleCode", minimumWidth=100)
        ]

        self.olv.SetColumns(columns)
        self.olv.SetObjects(None)




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
    def onEditDone(self, event):
        print "Finished Editing", event.cellValue
    def onColClick(self, event):
        print "Col ClickED!"
        pass
    def __del__(self):
        pass

    class Points(object):
        """

        """

        def __init__(self, dataValue=NO_DATA_VALUE, valueAccuracy="None", time="00:00:00", date="", utcOffSet="None", dateTimeUTC="None",
                     offSetValue="None", offSetType="None", censorCode="None", qualifierCode="None", labSampleCode="None"):

            self.dataValue = dataValue
            self.valueAccuracy = valueAccuracy
            self.time = str(time)
            print "time: ", self.time, type(self.time)
            self.date = datetime.now().date()
            print "date: ", self.date, type(self.date)
            self.utcOffSet = utcOffSet
            self.dateTimeUTC = dateTimeUTC
            self.offSetValue = offSetValue
            self.offSetType = offSetType
            self.censorCode = censorCode
            self.qualifierCode = qualifierCode
            self.labSampleCode = labSampleCode






class CellEdit():
    def __init__(self):
        pass

    def verifyDataValue(self, point):
        """Required Element

        :param point:
        :return:
        """
        if not point.dataValue:
            return "error"

    def verifyValueAccuracy(self, point):
        """Not Required

        :param point:
        :return:
        """
        if not point.valueAccuracy:
            return "error"

    def localTimeToString(self, time):
        """Required Element

        :param time:
        :return:
        """
        try:
            return str(time)
        except UnicodeEncodeError as e:
            #print "Error! in the unicode encoding..."
            return str("00:00:00")

    def verifyCensorCode(self, point):
        """Required Element

        :param point:
        :return:
        """
        if not point.censorCode:
            return "error"

    def censorCodeEditor(self, olv, rowIndex, subItemIndex):
        """

        :param olv:
        :param rowIndex:
        :param subItemIndex:
        :return:
        """
        odcb = CensorCodeComboBox(olv)
        # OwnerDrawnComboxBoxes don't generate EVT_CHAR so look for keydown instead
        odcb.Bind(wx.EVT_KEY_DOWN, olv._HandleChar)
        return odcb

    def localTimeEditor(self, olv, rowIndex, subItemIndex):
        """
        """

        # odcb = masked.TimeCtrl(olv, fmt24hr=True)
        odcb = TimePicker(olv, fmt24hr=True)

        odcb.Bind(wx.EVT_CHAR, olv._HandleChar)
        return odcb


class TimePicker(masked.TimeCtrl):
    """

    """
    def __init__(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        kwargs['fmt24hr'] = True
        kwargs['value'] = "00:00:00"
        kwargs['style'] = wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB
        masked.TimeCtrl.__init__(self, *args, **kwargs)

    def SetValue(self, value):
        """Put a new value into the editor"""
        print "In SetValue ", value, type(value)
        newValue = value or ""
        try:
            super(self.__class__, self).SetValue(newValue)
        except UnicodeEncodeError as e:
            newValue = unicode('00:00:00')
            super(self.__class__, self).SetValue(newValue)

class CensorCodeComboBox(wx.combo.OwnerDrawnComboBox):
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
