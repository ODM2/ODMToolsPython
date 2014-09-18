"""
    ADD Point Cell Editor Logic
"""

import wx
import wx.combo
from wx.lib import masked

__author__ = 'Jacob'


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

        odcb.Bind(wx.EVT_KEY_DOWN, olv._HandleChar)
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
        #kwargs['style'] = wx.TE_PROCESS_ENTER
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
