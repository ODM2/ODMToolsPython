import logging

import wx
import wx.lib.newevent
# from ObjectListView.ObjectListView import FastObjectListView, ColumnDefn
from odmtools.lib.ObjectListView import FastObjectListView, ColumnDefn

from odmtools.common.logger import LoggerTool
from odmtools.odmdata import Series


tool = LoggerTool()
logger = tool.setupLogger(__name__, __name__ + '.log', 'w', logging.DEBUG)

OvlCheckEvent, EVT_OVL_CHECK_EVENT = wx.lib.newevent.NewEvent()


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

        self._buildColumns()
        self.CreateCheckStateColumn()

        def rowFormatter(listItem, point):
            listItem.SetFont(wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False))

        self.rowFormatter = rowFormatter
        self.Bind(wx.EVT_LIST_KEY_DOWN, self.onKeyPress)

    def onKeyPress(self, evt):
        """Ignores Keypresses"""
        pass

    def _buildColumns(self):
        seriesColumns = [
            ColumnDefn(key, align="left", minimumWidth=100, valueGetter=value,
                       # stringConverter = '%s')
                       stringConverter='%Y-%m-%d %H:%M:%S' if "date" in key.lower() else'%s')
            for key, value in Series.returnDict().iteritems()]
        self.SetColumns(seriesColumns)

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







