"""
    Object List View Control used in Add Point Form
"""
import wx

from datetime import datetime
from odmtools.common import x_mark_16, star_16, star_32, x_mark_32, check_mark_3_16, check_mark_3_32
from odmtools.controller.logicCellEdit import CellEdit, NULL

__author__ = 'Jacob'

from odmtools.lib.ObjectListView import FastObjectListView, ColumnDefn


class Points(object):
    """

    """

    def __init__(self, dataValue="-9999", date=datetime.now().date(), time="00:00:00", utcOffSet="-7",
                 censorCode="NULL", valueAccuracy="NULL", offSetValue="NULL", offSetType="NULL", qualifierCode="NULL",
                 labSampleCode="NULL"):
        try:
            self.dataValue = str(dataValue)
        except:
            self.dataValue = dataValue

        self.valueAccuracy = valueAccuracy

        try:
            self.time = str(time)
        except:
            self.time = time

        try:
            self.date = datetime.strptime(str(date), '%Y-%m-%d').date()
        except Exception as e:
            self.date = datetime.now().date()

        self.utcOffSet = utcOffSet
        #self.dateTimeUTC = dateTimeUTC
        self.offSetValue = offSetValue
        self.offSetType = offSetType
        self.censorCode = censorCode
        self.qualifierCode = qualifierCode
        self.labSampleCode = labSampleCode

        ## determines whether a row is in correct format or now
        self.validDataValue = False
        self.validUTCOffSet = False
        self.validCensorCode = False
        self.validValueAcc = False
        self.validOffSetValue = False
        self.validOffSetType = False
        self.validQualifierCode = False
        self.validLabSampleCode = False

    def isCorrect(self):
        valid = [
            self.validDataValue, self.validUTCOffSet, self.validCensorCode, self.validValueAcc,
            self.validOffSetValue, self.validOffSetType, self.validQualifierCode, self.validLabSampleCode
        ]

        if all(valid):
            return True
        return False


class OLVAddPoint(FastObjectListView):
    """

    """
    def __init__(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """


        try:
            self.serviceManager = kwargs.pop("serviceManager")
        except:
            self.serviceManager = None
        try:
            self.recordService = kwargs.pop("recordService")
        except:
            self.recordService = None


        FastObjectListView.__init__(self, *args, **kwargs)

        cellEdit = CellEdit(self, self.serviceManager, self.recordService)

        # # Custom Image Getters
        self.imgGetterDataValue = cellEdit.imgGetterDataValue
        self.imgGetterCensorCode = cellEdit.imgGetterCensorCode
        self.imgGetterUTCOffset = cellEdit.imgGetterUTCOFFset
        self.imgGetterValueAcc = cellEdit.imgGetterValueAcc
        self.imgGetterlabSample = cellEdit.imgGetterLabSampleCode
        self.imgGetterQualifier = cellEdit.imgGetterQualifierCode
        self.imgGetterOffSetType = cellEdit.imgGetterOffSetType
        self.imgGetterOffSetValue = cellEdit.imgGetterOffSetValue

        ## Custom Value Setters
        ## Sets the value, can modify rules for setting value
        self.valueSetterDataValue = cellEdit.valueSetterDataValue
        self.valueSetterUTCOffset = cellEdit.valueSetterUTCOffset

        ## Custom String Converters
        ## Changes how the string will appear in the cell after editing
        self.localtime2Str = cellEdit.strConverterLocalTime
        self.str2DataValue = cellEdit.strConverterDataValue
        self.utcOffSet2Str = cellEdit.strConverterUTCOffset
        self.offSetValue2Str = cellEdit.strConverterOffSetValue

        ## Custom CellEditors
        ## Custom cell editors for each cell
        self.timeEditor = cellEdit.localTimeEditor
        self.censorEditor = cellEdit.censorCodeEditor
        self.offSetTypeEditor = cellEdit.offSetTypeEditor
        self.qualifierCodeEditor = cellEdit.qualifierCodeEditor
        self.labSampleEditor = cellEdit.labSampleCodeEditor

        self.SetEmptyListMsg("Add points either by csv or by adding a new row")
        self.AddNamedImages("error", x_mark_16.GetBitmap(), x_mark_32.GetBitmap())
        self.AddNamedImages("star", star_16.GetBitmap(), star_32.GetBitmap())
        self.AddNamedImages("check", check_mark_3_16.GetBitmap(), check_mark_3_32.GetBitmap())

        self.buildOlv()

        self.useAlternateBackColors = True
        self.oddRowsBackColor = wx.Colour(191, 239, 255)
        self.cellEditMode = self.CELLEDIT_DOUBLECLICK

    def buildOlv(self):
        columns = [
            ## TODO This is needed for the windows version
            #ColumnDefn("", "left", -1, valueSetter=self.emptyCol),
            ColumnDefn("DataValue", "left", -1, minimumWidth=100,
                       valueGetter='dataValue',
                       valueSetter=self.valueSetterDataValue,
                       imageGetter=self.imgGetterDataValue,
                       stringConverter=self.str2DataValue,
                       headerImage="star"),
            ColumnDefn("Date", "left", -1,  minimumWidth=85,
                       valueGetter="date",
                       headerImage="star"),
            ColumnDefn("Time", "left", -1, valueGetter="time", minimumWidth=75,
                       cellEditorCreator=self.timeEditor,
                       stringConverter=self.localtime2Str,
                       headerImage="star"),
            ColumnDefn("UTCOffset", "left", -1, minimumWidth=100,
                       valueGetter="utcOffSet",
                       valueSetter=self.valueSetterUTCOffset,
                       imageGetter=self.imgGetterUTCOffset,
                       headerImage="star"),
            ColumnDefn("CensorCode", "left", -1, valueGetter="censorCode", minimumWidth=110,
                       cellEditorCreator=self.censorEditor,
                       imageGetter=self.imgGetterCensorCode,
                       headerImage="star"),
            ColumnDefn("ValueAccuracy", "left", -1, valueGetter="valueAccuracy", minimumWidth=100,
                       imageGetter=self.imgGetterValueAcc),
            ColumnDefn("OffsetValue", "left", -1, valueGetter="offSetValue", minimumWidth=100,
                       stringConverter=self.offSetValue2Str,
                       imageGetter=self.imgGetterOffSetValue),
            ColumnDefn("OffsetType", "left", -1, valueGetter="offSetType", minimumWidth=100,
                       imageGetter=self.imgGetterOffSetType,
                       cellEditorCreator=self.offSetTypeEditor),
            ColumnDefn("QualifierCode", "left", -1, valueGetter="qualifierCode", minimumWidth=100,
                       imageGetter=self.imgGetterQualifier,
                       cellEditorCreator=self.qualifierCodeEditor),
            ColumnDefn("LabSampleCode", "left", -1, valueGetter="labSampleCode", minimumWidth=130,
                       imageGetter=self.imgGetterlabSample,
                       cellEditorCreator=self.labSampleEditor
                       ),
        ]

        self.SetColumns(columns)
        self.SetObjects(None)

    def sampleRow(self):
        return Points()

    def emptyCol(self):
        return " "