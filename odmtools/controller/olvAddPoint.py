import wx
import wx.lib.newevent
from datetime import datetime
from odmtools.common.icons import x_mark_16, star_16, star_32, x_mark_32, check_mark_3_16, check_mark_3_32
from odmtools.controller.logicCellEdit import CellEdit, NULL
from odmtools.lib.ObjectListView import FastObjectListView, ColumnDefn
OvlCheckEvent, EVT_OVL_CHECK_EVENT = wx.lib.newevent.NewEvent()


class Points(object):
    def __init__(self, dataValue="-9999", date=datetime.now().date(), time="00:00:00", utcOffSet=-7,
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

        self.date = str(date)
        self.valueDateTime = self.date

        self.utcOffSet = str(utcOffSet)
        self.valueDateTimeUTFOffset = -1
        self.offSetValue = offSetValue
        self.offSetType = offSetType
        self.censorCode = censorCode
        self.qualifierCode = qualifierCode
        self.labSampleCode = labSampleCode

        ## determines whether a row is in correct format or now
        self.validDataValue = False
        self.validTime = False
        self.validDate = False
        self.validUTCOffSet = False
        self.validCensorCode = False
        self.validValueAcc = False
        self.validOffSetValue = False
        self.validOffSetType = False
        self.validQualifierCode = False
        self.validLabSampleCode = False


class OLVAddPoint(FastObjectListView):
    def __init__(self, *args, **kwargs):
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

        self.checkedObjects = []

        # # Custom Image Getters
        self.imgGetterDataValue = cellEdit.imgGetterDataValue
        self.imgGetterDate = cellEdit.imgGetterDate
        self.imgGetterTime = cellEdit.imgGetterTime
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
        self.dateEditor = cellEdit.dateEditor
        self.timeEditor = cellEdit.localTimeEditor
        self.censorEditor = cellEdit.censorCodeEditor
        self.offSetTypeEditor = cellEdit.offSetTypeEditor
        self.qualifierCodeEditor = cellEdit.qualifierCodeEditor
        self.labSampleEditor = cellEdit.labSampleCodeEditor
        self.valueDateTimeEditorCreator = cellEdit.valueDateTimeEditor
        # self.valueDateTimeUTFOffset = cellEdit.valueDateTimeUTFOffsetCreator

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
            ColumnDefn("DataValue", "left", -1, minimumWidth=100,
                       valueGetter='dataValue',
                       valueSetter=self.valueSetterDataValue,
                       imageGetter=self.imgGetterDataValue,
                       stringConverter=self.str2DataValue,
                       headerImage="star"),
            ColumnDefn("Date", "left", -1, minimumWidth=120,
                       valueGetter="date",
                       imageGetter=self.imgGetterDate,
                       cellEditorCreator=self.dateEditor,
                       headerImage="star"),
            ColumnDefn("Time", "left", -1, minimumWidth=100,
                       valueGetter="time",
                       imageGetter=self.imgGetterTime,
                       cellEditorCreator=self.timeEditor,
                       stringConverter=self.localtime2Str,
                       headerImage="star"),
            ColumnDefn("UTCOffset", "left", -1, minimumWidth=100, valueGetter="utcOffSet",
                       imageGetter=self.imgGetterUTCOffset, headerImage="star"),

            ColumnDefn("CensorCode", "left", -1, valueGetter="censorCode", minimumWidth=110,
                       cellEditorCreator=self.censorEditor, imageGetter=self.imgGetterCensorCode, headerImage="star"),

            # valueGetter needs to be created in the Points class
            ColumnDefn(title="ValueDateTime", align="left", valueGetter="valueDateTime",
                       minimumWidth=123, cellEditorCreator=self.valueDateTimeEditorCreator, headerImage="star"),

            ColumnDefn(title="ValueDateTimeUTFOffset", align="left", valueGetter="valueDateTimeUTFOffset",
                       minimumWidth=130, headerImage="star"),

            ColumnDefn("OffsetValue", "left", -1, valueGetter="offSetValue", minimumWidth=100,
                       stringConverter=self.offSetValue2Str,
                       imageGetter=self.imgGetterOffSetValue),
            ColumnDefn("OffsetType", "left", -1, valueGetter="offSetType", minimumWidth=100,
                       imageGetter=self.imgGetterOffSetType,
                       cellEditorCreator=self.offSetTypeEditor),
            ColumnDefn("QualifierCode", "left", -1, valueGetter="qualifierCode", minimumWidth=130,
                       imageGetter=self.imgGetterQualifier,
                       cellEditorCreator=self.qualifierCodeEditor),
            ColumnDefn("LabSampleCode", "left", -1, valueGetter="labSampleCode", minimumWidth=130,
                       imageGetter=self.imgGetterlabSample,
                       cellEditorCreator=self.labSampleEditor
                       ),
        ]

        self.SetColumns(columns)

        # self.CreateCheckStateColumn()
        self.SetObjects(None)

        def rowFormatter(listItem, point):
            """Formats each row to have a larger font than the default font.

            :param listItem:
            :param point:
            :return:
            """
            listItem.SetFont(wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False))

        self.rowFormatter = rowFormatter
        self.AutoSizeColumns()

    def isCorrect(self, point):
        validators = [
            self.imgGetterDataValue, self.imgGetterDate, self.imgGetterTime, self.imgGetterCensorCode,
            self.imgGetterUTCOffset, self.imgGetterValueAcc, self.imgGetterlabSample,
            self.imgGetterQualifier, self.imgGetterOffSetType, self.imgGetterOffSetValue
        ]

        isCorrect = True
        for v in validators:
            returnValue = v(point)
            if returnValue == "error":
                isCorrect = False

        return isCorrect

    def sampleRow(self):
        return Points()

    def emptyCol(self):
        return " "

'''
    def _HandleLeftDownOnImage(self, rowIndex, subItemIndex):
        """
        This is the same code, just added the original _HandleLeftDownOnImage in ObjectListView

        User can use mouse clicks to check/uncheck rows
        """

        column = self.columns[subItemIndex]
        if not column.HasCheckState():
            return

        self._PossibleFinishCellEdit()
        modelObject = self.GetObjectAt(rowIndex)
        if modelObject is not None:
            if column.GetCheckState(modelObject) is False:
                """Visually 'check' row"""
                column.SetCheckState(modelObject, not column.GetCheckState(modelObject))

                ## Keep a record of which objects are checked
                self.checkedObjects.append(modelObject)

                # Just added the event here ===================================
                e = OvlCheckEvent(object=modelObject, value=column.GetCheckState(modelObject),
                                  checkedObjects=self.checkedObjects, row=rowIndex, column=column)
                wx.PostEvent(self, e)
                # =============================================================

                self.RefreshIndex(rowIndex, modelObject)
            else:
                """Visually 'uncheck' row"""
                column.SetCheckState(modelObject, not column.GetCheckState(modelObject))

                self.checkedObjects.remove(modelObject)

                # Just added the event here ===================================
                e = OvlCheckEvent(object=modelObject, value=column.GetCheckState(modelObject),
                                  checkedObjects=self.checkedObjects, row=rowIndex, column=column)
                wx.PostEvent(self, e)
                # =============================================================

    def SetCheckState(self, modelObject, state):
        """
        This is the same code as the original SetCheckState in ObjectListView

        User can select using the space bar to check/uncheck rows

        """

        if self.checkStateColumn is None:
            return None

        if self.GetCheckState(modelObject) is False:
            """Visually 'check' row"""
            r = self.checkStateColumn.SetCheckState(modelObject, state)


            ## Keep a record of which objects are checked
            self.checkedObjects.append(modelObject)

            # Just added the event here ===================================
            e = OvlCheckEvent(object=modelObject, value=state,
                              checkedObjects=self.checkedObjects)
            wx.PostEvent(self, e)
            # =============================================================

            return r
        else:
            r = self.checkStateColumn.SetCheckState(modelObject, state)

            self.checkedObjects.remove(modelObject)

            # Just added the event here ===================================
            e = OvlCheckEvent(object=modelObject, value=state,
                              checkedObjects=self.checkedObjects)
            wx.PostEvent(self, e)
            # =============================================================

            return r

'''

