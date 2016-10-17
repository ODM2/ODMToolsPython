import logging

import wx
import wx.lib.newevent
# from ObjectListView.ObjectListView import FastObjectListView, ColumnDefn
from odmtools.lib.ObjectListView import FastObjectListView, ColumnDefn


# from odmtools.common.logger import LoggerTool


# tool = LoggerTool()
# logger = tool.setupLogger(__name__, __name__ + '.log', 'w', logging.DEBUG)
logger =logging.getLogger('main')

OvlCheckEvent, EVT_OVL_CHECK_EVENT = wx.lib.newevent.NewEvent()
from collections import OrderedDict
# def returnDict():
#     keys = ['SeriesID', 'SiteID', 'SiteCode', 'SiteName', 'VariableID', 'VariableCode', 'VariableName', 'Speciation',
#             'VariableUnitsID', 'VariableUnitsName', 'SampleMedium', 'ValueType', 'TimeSupport', 'TimeUnitsID',
#             'TimeUnitsName', 'DataType', 'GeneralCategory', 'MethodID', 'MethodDescription', 'SourceID',
#             'SourceDescription', 'Organization', 'Citation', 'QualityControlLevelID', 'QualityControlLevelCode',
#             'BeginDateTime', 'EndDateTime', 'BeginDateTimeUTC', 'EndDateTimeUTC', 'ValueCount'
#             ]
#     values = ['id', 'site_id', 'site_code', 'site_name', 'variable_id', 'variable_code', 'variable_name', 'speciation',
#               'variable_units_id', 'variable_units_name', 'sample_medium', 'value_type', 'time_support',
#               'time_units_id', 'time_units_name', 'data_type', 'general_category', 'method_id', 'method_description',
#               'source_id', 'source_description', 'organization', 'citation', 'quality_control_level_id',
#               'quality_control_level_code', 'begin_date_time', 'end_date_time', 'begin_date_time_utc',
#               'end_date_time_utc', 'value_count'
#               ]
#     return OrderedDict(zip(keys, values))



# def returnDict():

class clsSeriesTable(FastObjectListView):
    def __init__(self, *args, **kwargs):
        FastObjectListView.__init__(self, *args, **kwargs)
        """Max Number of Allowed Plots"""
        self.allowedLimit = 6

        """List of modelObjects"""
        self._modelObjects = []

        """Focused Object"""
        self.currentlySelectedObject = None

        """Object being edited"""
        self.editingObject = None

        #self._buildColumns()


        def rowFormatter(listItem, point):
            listItem.SetFont(wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False))

        self.rowFormatter = rowFormatter
        self.Bind(wx.EVT_LIST_KEY_DOWN, self.onKeyPress)

    def onKeyPress(self, evt):
        """Ignores Keypresses"""
        pass

    def _buildColumns(self, columns):
        seriesColumns = [
            ColumnDefn(key, align="left", minimumWidth=100, valueGetter=key,
                       # stringConverter = '%s')
                       stringConverter='%Y-%m-%d %H:%M:%S' if "date" in key.lower() else '%s')
            for key in columns]


        self.SetColumns(seriesColumns)
        self.CreateCheckStateColumn()

    """User can select series using the mouse to click on check boxes """

    def _HandleLeftDownOnImage(self, rowIndex, subItemIndex):
        """
        This is the same code, just added the original _HandleLeftDownOnImage in ObjectListView but
        has been enhanced to check against an allowed limit
        """
        #print "_HandleLeftDownOnImage called!", rowIndex, " ", subItemIndex

        column = self.columns[subItemIndex]
        if not column.HasCheckState():
            return

        self._PossibleFinishCellEdit()
        modelObject = self.GetObjectAt(rowIndex)
        if modelObject is not None:
            checkedlen = len(self.GetCheckedObjects())
            if column.GetCheckState(modelObject) is False:
                if checkedlen < self.allowedLimit:
                    column.SetCheckState(modelObject, not column.GetCheckState(modelObject))

                    # Just added the event here ===================================
                    e = OvlCheckEvent(object=modelObject, value=column.GetCheckState(modelObject))
                    wx.PostEvent(self, e)
                    # =============================================================

                    self.RefreshIndex(rowIndex, modelObject)
                else:
                    wx.MessageBox("Visualization is limited to {0} series.".format(self.allowedLimit), "Can't add plot",
                                  wx.OK | wx.ICON_INFORMATION)
            else:
                if checkedlen > 0:
                    column.SetCheckState(modelObject, not column.GetCheckState(modelObject))

                    # Just added the event here ===================================
                    e = OvlCheckEvent(object=modelObject, value=column.GetCheckState(modelObject))
                    wx.PostEvent(self, e)
                    # =============================================================

    def SaveObject(self, object):
        """Original List of objects is stored while filtering"""
        self._modelObjects = object

    def GetModelObjects(self):
        """Returns the original modelobjects
        To be used for after filtering in order to return to the original list of objects

        :rtype: list of modelObjects
        """
        return self._modelObjects if self._modelObjects else []







