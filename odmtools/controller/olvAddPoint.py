"""
    Object List View Control used in Add Point Form
"""
import wx

from datetime import datetime
from odmtools.common import x_mark_16, star_16, star_32, x_mark_32
from odmtools.controller.logicCellEdit import CellEdit

__author__ = 'Jacob'

from odmtools.lib.ObjectListView import FastObjectListView, ColumnDefn

# # Specific Settings
NO_DATA_VALUE = u'-9999'


class Points(object):
    """

    """

    def __init__(self, dataValue=NO_DATA_VALUE, valueAccuracy="NULL", time="00:00:00",
                 date="", utcOffSet="NULL", dateTimeUTC="NULL", offSetValue="NULL",
                 offSetType="NULL", censorCode="NULL", qualifierCode="NULL", qualifierDesc="NULL",
                 labSampleCode="NULL"):
        self.dataValue = dataValue
        self.valueAccuracy = valueAccuracy
        self.time = str(time)
        #print "time: ", self.time, type(self.time)
        self.date = datetime.now().date()
        #print "date: ", self.date, type(self.date)
        self.utcOffSet = utcOffSet
        self.dateTimeUTC = dateTimeUTC
        self.offSetValue = offSetValue
        self.offSetType = offSetType
        self.censorCode = censorCode
        self.qualifierCode = qualifierCode
        self.qualifierDesc = qualifierDesc
        self.labSampleCode = labSampleCode


class OLVAddPoint(FastObjectListView):
    """

    """
    def __init__(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        FastObjectListView.__init__(self, *args, **kwargs)
        ## Cell Verification and Editors Init
        self.vfyDataValue = None
        self.vfyValueAcc = None
        self.localtime2Str = None
        self.timeEditor = None

        self.SetEmptyListMsg("Add points either by csv or by adding a new row")
        self.AddNamedImages("error", x_mark_16.GetBitmap(), x_mark_32.GetBitmap())
        self.AddNamedImages("star", star_16.GetBitmap(), star_32.GetBitmap())

        self.initiateCellValidators()
        self.buildOlv()

        self.useAlternateBackColors = True
        self.oddRowsBackColor = wx.Colour(191, 239, 255)
        self.cellEditMode = self.CELLEDIT_DOUBLECLICK

    def buildOlv(self):
        columns = [
            ColumnDefn("", "left", -1, valueSetter=self.emptyCol),
            ColumnDefn("DataValue", "left", -1, valueGetter="dataValue", minimumWidth=100,
                      imageGetter=self.vfyDataValue, headerImage="star"),
            ColumnDefn("Date", "left", -1, valueGetter="date", minimumWidth=85, headerImage="star"),
            ColumnDefn("Time", "left", -1, valueGetter="time", minimumWidth=75,
                      cellEditorCreator=self.timeEditor, stringConverter=self.localtime2Str,
                      headerImage="star"),
            ColumnDefn("UTCOffset", "left", -1, valueGetter="utcOffSet", minimumWidth=100,
                      headerImage="star"),
            ColumnDefn("CensorCode", "left", -1, valueGetter="censorCode", minimumWidth=110,
                      cellEditorCreator=self.censorEditor, imageGetter=self.vfyCensorCode,
                      headerImage="star"),
            ColumnDefn("ValueAccuracy", "left", -1, valueGetter="valueAccuracy", minimumWidth=100),
            ColumnDefn("OffsetValue", "left", -1, valueGetter="offSetValue", minimumWidth=100),
            ColumnDefn("OffsetType", "left", -1, valueGetter="offSetType", minimumWidth=100),
            ColumnDefn("QualifierCode", "left", -1, valueGetter="qualifierCode", minimumWidth=100),
            ColumnDefn("QualifierDesc", "left", -1, valueGetter="qualifierDesc", minimumWidth=150),
            ColumnDefn("LabSampleCode", "left", -1, valueGetter="labSampleCode", minimumWidth=100)
        ]

        self.SetColumns(columns)
        self.SetObjects(None)

    def initiateCellValidators(self):
        self.vfyDataValue = CellEdit().verifyDataValue
        self.vfyValueAcc = CellEdit().verifyValueAccuracy
        self.localtime2Str = CellEdit().localTimeToString
        self.vfyCensorCode = CellEdit().verifyCensorCode

        self.timeEditor = CellEdit().localTimeEditor
        self.censorEditor = CellEdit().censorCodeEditor

    def sampleRow(self):
        return Points()

    def emptyCol(self):
        return " "