import wx
import wx.lib.newevent
from datetime import datetime
from odmtools.common.icons import x_mark_16, star_16, star_32, x_mark_32, check_mark_3_16, check_mark_3_32
from odmtools.controller.logicCellEdit import CellEdit, NULL
from odmtools.lib.ObjectListView import FastObjectListView, ColumnDefn
from odmtools.odmservices.service_manager import ServiceManager
OvlCheckEvent, EVT_OVL_CHECK_EVENT = wx.lib.newevent.NewEvent()


class Points(object):
    def __init__(self, data_value="-9999", date=datetime.now().date(), time="00:00:00", utcOffSet=-7,
                 censor_code="NULL", quality_code="NULL", time_agg_interval="NULL", time_agg_unit="NULL", annotation="NULL"):
        try:
            self.dataValue = str(data_value)
        except:
            self.dataValue = data_value
        try:
            self.time = str(time)
        except:
            self.time = time

        self.date = str(date)
        self.valueDateTime = self.date

        self.utcOffSet = str(utcOffSet)
        self.censorCode = censor_code
        self.qualityCodeCV = quality_code
        self.timeAggInterval = time_agg_interval
        self.timeAggregationUnitID = time_agg_unit
        self.annotation = annotation

        ## determines whether a row is in correct format or now
        self.validDataValue = False
        self.validTime = False
        self.validDate = False
        self.validUTCOffSet = False
        self.validCensorCode = False
        self.validValueAcc = False
        self.validOffSetType = False
        self.validQualityCode = False
        self.validTimeAggInterval = False
        self.validTimeAggUnit = False


class OLVAddPoint(FastObjectListView):
    def __init__(self, *args, **kwargs):
        if "serviceManager" in kwargs:
            self.serviceManager = kwargs.pop("serviceManager")
        else:
            try:
                self.serviceManager = ServiceManager()
            except:
                self.serviceManager = None

        try:
            self.recordService = kwargs.pop("recordService")
        except:
            self.recordService = None

        FastObjectListView.__init__(self, *args, **kwargs)

        self.cellEdit = CellEdit(self, self.serviceManager, self.recordService)

        self.checkedObjects = []

        # # Custom Image Getters
        self.imgGetterDataValue = self.cellEdit.imgGetterDataValue
        self.imgGetterDate = self.cellEdit.imgGetterDate
        self.imgGetterTime = self.cellEdit.imgGetterTime
        self.imgGetterCensorCode = self.cellEdit.imgGetterCensorCode
        self.imgGetterUTCOffset = self.cellEdit.imgGetterUTCOFFset
        self.imgGetterQualityCode = self.cellEdit.imgGetterQualityCode
        self.imgGetterTimeAggInterval = self.cellEdit.imgGetterTimeAggregationInterval
        self.imgGetterTimeAggUnit = self.cellEdit.imgGetterTimeAggregationUnit

        ## Custom Value Setters
        ## Sets the value, can modify rules for setting value
        self.valueSetterDataValue = self.cellEdit.valueSetterDataValue
        self.valueSetterUTCOffset = self.cellEdit.valueSetterUTCOffset

        ## Custom String Converters
        ## Changes how the string will appear in the cell after editing
        self.localtime2Str = self.cellEdit.strConverterLocalTime
        self.str2DataValue = self.cellEdit.strConverterDataValue
        self.utcOffSet2Str = self.cellEdit.strConverterUTCOffset
        # self.offSetValue2Str = cellEdit.strConverterOffSetValue

        ## Custom CellEditors
        ## Custom cell editors for each cell
        self.dateEditor = self.cellEdit.dateEditor
        self.timeEditor = self.cellEdit.localTimeEditor
        self.censorEditor = self.cellEdit.censorCodeEditor
        self.valueDateTimeEditorCreator = self.cellEdit.valueDateTimeEditor
        self.qualityCodeCreator = self.cellEdit.setComboForQualityCodeColumn
        self.timeAggregationUnitIDCreator = self.cellEdit.setComboForTimeAggregationUnitIDCreator
        self.annotationCreator = self.cellEdit.setComboForAnnotation

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
            ColumnDefn(title="DataValue",
                       minimumWidth=100,
                       valueGetter='dataValue',
                       valueSetter=self.valueSetterDataValue,
                       imageGetter=self.imgGetterDataValue,
                       stringConverter=self.str2DataValue,
                       headerImage="star"),

            ColumnDefn(title="Date", minimumWidth=120,
                       valueGetter="date",
                       imageGetter=self.imgGetterDate,
                       cellEditorCreator=self.dateEditor,
                       headerImage="star"),

            ColumnDefn(title="Time", minimumWidth=100,
                       valueGetter="time",
                       imageGetter=self.imgGetterTime,
                       cellEditorCreator=self.timeEditor,
                       stringConverter=self.localtime2Str,
                       headerImage="star"),

            ColumnDefn(title="UTCOffset",
                       minimumWidth=100,
                       valueGetter="utcOffSet",
                       imageGetter=self.imgGetterUTCOffset,
                       headerImage="star"),

            ColumnDefn(title="CensorCode",
                       valueGetter="censorCode",
                       minimumWidth=110,
                       cellEditorCreator=self.censorEditor,
                       imageGetter=self.imgGetterCensorCode,
                       headerImage="star"),

            ColumnDefn(title="Quality CodeCV",
                       valueGetter="qualityCodeCV",
                       minimumWidth=130,
                       cellEditorCreator=self.qualityCodeCreator,
                       imageGetter=self.imgGetterQualityCode,
                       headerImage="star"),

            ColumnDefn(title="TimeAggregationInterval",
                       minimumWidth=130,
                       valueGetter="timeAggInterval",
                       imageGetter=self.imgGetterTimeAggInterval,
                       headerImage="star"),

            ColumnDefn(title="TimeAggregationUnitID",
                       minimumWidth=130,
                       valueGetter="timeAggregationUnitID",
                       cellEditorCreator=self.timeAggregationUnitIDCreator,
                       imageGetter=self.imgGetterTimeAggUnit, headerImage="star"),

            ColumnDefn(title="Annotation",
                       minimumWidth=130,
                       valueGetter="annotation",
                       cellEditorCreator=self.annotationCreator)
        ]

        self.SetColumns(columns)
        self.SetObjects(None)

        def rowFormatter(listItem, point):
            """Formats each row to have a larger font than the default font.

            :param listItem:
            :param point:
            :return:
            """
            listItem.SetFont(wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False))

        self.rowFormatter = rowFormatter

    def isCorrect(self, point):
        validators = [
            self.imgGetterDataValue, self.imgGetterDate, self.imgGetterTime, self.imgGetterCensorCode,
            self.imgGetterUTCOffset, self.imgGetterQualityCode, self.imgGetterTimeAggInterval, self.imgGetterTimeAggUnit
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

