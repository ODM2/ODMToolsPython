import logging

import wx
import wx.lib.newevent
from ObjectListView.ObjectListView import FastObjectListView

from common.logger import LoggerTool


tool = LoggerTool()
logger = tool.setupLogger(__name__, __name__ + '.log', 'w', logging.DEBUG)

OvlCheckEvent, EVT_OVL_CHECK_EVENT = wx.lib.newevent.NewEvent()


class clsSeriesTable(FastObjectListView):
    """Max Number of Allowed Plots"""
    allowedLimit = 6

    """List of modelObjects"""
    _modelObjects = []

    """Focused Object"""
    currentlySelectedObject = None

    """Object being edited"""
    editingObject = None

    """User can select using the space bar """
    def SetCheckState(self, modelObject, state):
        """
        This is the same code as the original SetCheckState in ObjectListView but
        has been enhanced to check against an allowed limit
        """
        #print "SetCheckState called!"

        if self.checkStateColumn is None:
            return None
        else:
            checkedlen = len(self.GetCheckedObjects())
            if self.GetCheckState(modelObject) is False:
                if checkedlen < self.allowedLimit:
                    r = self.checkStateColumn.SetCheckState(modelObject, state)

                    # Just added the event here ===================================
                    e = OvlCheckEvent(object=modelObject, value=state)
                    wx.PostEvent(self, e)
                    # =============================================================

                    return r
                else:
                    wx.MessageBox("Visualization is limited to {0} series.".format(self.allowedLimit), "Can't add plot",
                                  wx.OK | wx.ICON_INFORMATION)
            else:
                if checkedlen > 0:
                    r = self.checkStateColumn.SetCheckState(modelObject, state)

                    # Just added the event here ===================================
                    e = OvlCheckEvent(object=modelObject, value=state)
                    wx.PostEvent(self, e)
                    # =============================================================

                    return r

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







