"""
    ADD Point Cell Editor Logic
"""
from collections import OrderedDict
import datetime

import wx
import wx.combo
from wx.lib import masked
from odmtools.gui.frmFlagValues import frmFlagValues
from odmtools.lib.ObjectListView import CellEditor

__author__ = 'Jacob'

#### Options ####
utcOffSetBounds = (-12, 12)
NULL = "NULL"
NEW = "[New Qualifier]"

class CellEdit():
    def __init__(self, parent, serviceManager, recordService):
        self.parent = parent
        self.recordService = recordService
        if serviceManager:
            self.serviceManager = serviceManager
            self.cv_service = serviceManager.get_cv_service()
            self.series_service = serviceManager.get_series_service()
            offsetChoices = OrderedDict((x.description, x.id) for x in
                                        self.cv_service.get_offset_type_cvs())
            self.offSetTypeChoices = [NULL] + offsetChoices.keys()

            labChoices = OrderedDict((x.lab_sample_code, x.id) for x in self.cv_service.get_samples())

            self.censorCodeChoices = [NULL] + [x.term for x in self.cv_service.get_censor_code_cvs()]
            self.labSampleChoices = [NULL] + labChoices.keys()

            self.qualifierChoices = OrderedDict((x.code + ':' + x.description, x.id)
                                           for x in self.series_service.get_all_qualifiers() if x.code and x.description)
            self.qualifierCodeChoices = [NULL] + self.qualifierChoices.keys() + [NEW]

        else:
            self.censorCodeChoices = [NULL] + ['SampleCensorCode1'] + ['SampleCensorCode2'] + ['SampleCensorCode3']
            self.labSampleChoices = [NULL] + ['SampleLabSample1'] + ['SampleLabSample2'] + ['SampleLabSample3']
            self.offSetTypeChoices = [NULL] + ['SampleOffsetType1'] + ['SampleOffsetType2'] + ['SampleOffsetType3']
            self.qualifierCodeChoices = [NULL] + ['SampleQualifierCode1'] + ['SampleQualifierCode2'] + ['SampleQualifierCode3']

    """
        --------------------
        Custom Image Getters
        --------------------
    """
    def imgGetterDataValue(self, point):
        """Required Element

        :param point:
        :return:
        """
        point.validDataValue = False
        if not point.dataValue:
            return "error"
        if isinstance(point.dataValue, basestring):
            for type in [int, float]:
                try:
                    value = type(point.dataValue)
                    if isinstance(value, type):
                        point.validDataValue = True
                        return "check"
                except ValueError:
                    continue
        elif isinstance(point.dataValue, int):
            point.validDataValue = True
            return "check"
        elif isinstance(point.dataValue, float):
            point.validDataValue = True
            return "check"
        return "error"

    def imgGetterDate(self, point):
        """ Required Element

        :param point:
        :return:
        """

        date = point.date
        point.validDate = False
        try:
            datetime.datetime.strptime(str(date), '%Y-%m-%d').date()
            point.validDate = True
            return "check"
        except Exception as e:
            pass

        return "error"

    def imgGetterTime(self, point):
        """

        :param point:
        :return:
        """

        time = point.time
        point.validTime = False
        try:
            datetime.datetime.strptime(str(time), '%H:%M:%S')
            point.validTime = True
            return "check"
        except:
            pass

        return "error"


    def imgGetterCensorCode(self, point):
        """Required Element

        :param point:
        :return:
        """
        point.validCensorCode = False
        if not point.censorCode:
            return "error"
        if point.censorCode == NULL:
            return "error"
        if not point.censorCode in self.censorCodeChoices:
            return "error"

        point.validCensorCode = True
        return "check"

    def imgGetterUTCOFFset(self, point):
        """Required Element

        :param point:
        :return:
        """

        value = point.utcOffSet
        point.validUTCOffSet = False
        if not value:
            return "error"

        if isinstance(value, int):
            if utcOffSetBounds[0] <= value <= utcOffSetBounds[1]:
                point.validUTCOffSet = True
                return "check"

        if isinstance(value, basestring):
            try:
                newValue = int(value)
                if isinstance(newValue, int):
                    if utcOffSetBounds[0] <= newValue <= utcOffSetBounds[1]:
                        point.validUTCOffSet = True
                        return "check"
            except ValueError as e:
                pass

        return "error"

    def imgGetterValueAcc(self, point):
        """
        """
        value = point.valueAccuracy
        point.validValueAcc = False
        if not value:
            return "error"

        if value == NULL:
            point.validValueAcc = True
            return "check"

        if isinstance(value, basestring):
            for type in [int, float]:
                try:
                    value = type(value)
                    if isinstance(value, type):
                        point.validValueAcc = True
                        return "check"
                except ValueError:
                    continue
        return "error"

    def imgGetterOffSetType(self, point):
        """
        """
        point.validOffSetType = False
        if not point.offSetType in self.offSetTypeChoices:
            return "error"
        point.validOffSetType = True
        return "check"

    def imgGetterOffSetValue(self, point):
        """
        """

        point.validOffSetValue = False
        if point.offSetValue == NULL:
            point.validOffSetValue = True
            return "check"

        if isinstance(point.offSetValue, basestring):
            for type in [int, float]:
                try:
                    value = type(point.offSetValue)
                    if isinstance(value, type):
                        point.validOffSetValue = True
                        return "check"
                except ValueError:
                    continue
        elif isinstance(point.offSetValue, int):
            point.validOffSetValue = True
            return "check"
        elif isinstance(point.offSetValue, float):
            point.validOffSetValue = True
            return "check"
        return "error"


    def imgGetterQualifierCode(self, point):
        """
        """

        point.validQualifierCode = False
        if not point.qualifierCode in self.qualifierCodeChoices:
            return "error"
        point.validQualifierCode = True
        return "check"

    def imgGetterLabSampleCode(self, point):
        """
        """

        point.validLabSampleCode = False
        if not point.labSampleCode in self.labSampleChoices:
            return "error"
        point.validLabSampleCode = True
        return "check"

    """
        --------------------
        Custom Value Setters
        --------------------
    """
    def valueSetterDataValue(self, point, newValue):
        """

        :param point:
        :return:
        """
        point.dataValue = newValue

    def valueSetterUTCOffset(self, point, newValue):

        if newValue == NULL:
            point.utcOffSet = newValue
            return

        if isinstance(newValue, basestring):
            point.utcOffSet = int(float(newValue))
            return

        point.utcOffSet = newValue


    """
        ------------------------
        Custom String Converters
        ------------------------
    """
    def strConverterDataValue(self, value):
        """
        """

        try:
            return str(value)
        except Exception as e:
            return str(NULL)

    def strConverterLocalTime(self, time):
        """Required Element

        :param time:
        :return:
        """

        return unicode(time)

    def strConverterUTCOffset(self, value):
        """
        """

        return str(value)

    def strConverterOffSetValue(self, value):
        """
        """
        try:
            return str(value)
        except UnicodeEncodeError:
            return str(NULL)

    """
        ------------------
        Custom CellEditors
        ------------------
    """

    def localTimeEditor(self, olv, rowIndex, subItemIndex):
        """

        :param olv:
        :param rowIndex:
        :param subItemIndex:
        :return:
        """

        # odcb = masked.TimeCtrl(olv, fmt24hr=True)
        odcb = TimePicker(olv)

        odcb.Bind(wx.EVT_KEY_DOWN, olv._HandleChar)
        return odcb

    def dateEditor(self, olv, rowIndex, subItemIndex):
        """

        :param olv:
        :param rowIndex:
        :param subItemIndex:
        :return:
        """
        odcb = DatePicker(olv)
        odcb.Bind(wx.EVT_KEY_DOWN, olv._HandleChar)
        return odcb

    def offSetTypeEditor(self, olv, rowIndex, subItemIndex):
        """

        :param olv:
        :param rowIndex:
        :param subItemIndex:
        :return:
        """

        odcb = CustomComboBox(olv, choices=self.offSetTypeChoices, style=wx.CB_READONLY)
        # OwnerDrawnComboxBoxes don't generate EVT_CHAR so look for keydown instead
        odcb.Bind(wx.EVT_KEY_DOWN, olv._HandleChar)
        return odcb

    def qualifierCodeEditor(self, olv, rowIndex, subItemIndex):
        """

        :param olv:
        :param rowIndex:
        :param subItemIndex:
        :return:
        """
        def cbHandler(event):
            """
            :param event:
                :type wx.EVT_COMBOBOX:
            """

            if event.GetEventObject().Value == NEW:
                dlg = frmFlagValues(self.parent, self.cv_service, self.qualifierChoices, isNew=True)

                value = dlg.ShowModal()
                if value == wx.ID_OK and dlg.selectedValue:
                    self.qualifierCodeChoices.insert(0, dlg.selectedValue)
                    event.GetEventObject().SetItems(self.qualifierCodeChoices)
                    print event.GetEventObject().GetValue()
                    print type(event.GetEventObject())
                    event.GetEventObject().SetValue(dlg.selectedValue)
                    print event.GetEventObject().GetValue()
                #dlg.Destroy()

        try:
            self.qualifierChoices = OrderedDict((x.code + ':' + x.description, x.id)
                                               for x in self.cv_service.get_all_qualifiers() if x.code and x.description)
            self.qualifierCodeChoices = [NULL] + self.qualifierChoices.keys() + [NEW]
        except:
            pass
        odcb = CustomComboBox(olv, choices=self.qualifierCodeChoices, style=wx.CB_READONLY)
        # OwnerDrawnComboxBoxes don't generate EVT_CHAR so look for keydown instead
        odcb.Bind(wx.EVT_KEY_DOWN, olv._HandleChar)
        odcb.Bind(wx.EVT_COMBOBOX, cbHandler)
        return odcb

    def censorCodeEditor(self, olv, rowIndex, subItemIndex):
        """

        :param olv:
        :param rowIndex:
        :param subItemIndex:
        :return:
        """
        odcb = CustomComboBox(olv, choices=self.censorCodeChoices, style=wx.CB_READONLY)
        # OwnerDrawnComboxBoxes don't generate EVT_CHAR so look for keydown instead
        odcb.Bind(wx.EVT_KEY_DOWN, olv._HandleChar)
        return odcb

    def labSampleCodeEditor(self, olv, rowIndex, subItemIndex):
        """

        :param olv:
        :param rowIndex:
        :param subItemIndex:
        :return:
        """

        odcb = CustomComboBox(olv, choices=self.labSampleChoices, style=wx.CB_READONLY)
        odcb.Bind(wx.EVT_KEY_DOWN, olv._HandleChar)
        return odcb

class DatePicker(wx.DatePickerCtrl):
    """
    This control uses standard datetime.
    wx.DatePickerCtrl works only with wx.DateTime, but they are strange beasts.
    wx.DataTime use 0 indexed months, i.e. January==0 and December==11.
    """

    def __init__(self, *args, **kwargs):
        kwargs['style'] = kwargs.get('style', 0) | wx.DP_DEFAULT
        wx.DatePickerCtrl.__init__(self, *args, **kwargs)
        self.SetValue(None)

    def SetValue(self, value):
        if value:
            dt = wx.DateTime()
            try:
                date = datetime.datetime.strptime(str(value), '%Y-%m-%d').date()
            except ValueError:
                return
            dt.Set(date.day, date.month-1, date.year)
        else:
            dt = wx.DateTime.Today()
        wx.DatePickerCtrl.SetValue(self, dt)

    def GetValue(self):
        """Get the value from the editor"""
        dt = wx.DatePickerCtrl.GetValue(self)
        if dt.IsOk():
            return datetime.date(dt.Year, dt.Month+1, dt.Day)
        else:
            return None

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
        kwargs['style'] = wx.TE_PROCESS_ENTER
        masked.TimeCtrl.__init__(self, *args, **kwargs)

    def SetValue(self, value):
        """Put a new value into the editor"""
        newValue = value or ""
        try:
            masked.TimeCtrl.SetValue(self, newValue)
        except UnicodeEncodeError as e:
            pass

    def GetValue(self):
        value = masked.TimeCtrl.GetValue(self)
        return value



class CustomComboBox(wx.combo.OwnerDrawnComboBox):
    """

    """
    def __init__(self, *args, **kwargs):
        self.popupRowHeight = kwargs.pop("popupRowHeight", 24)
        #kwargs['style'] = kwargs.get('style', 0) | wx.CB_READONLY
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

    def SetValue(self, value):
        wx.combo.OwnerDrawnComboBox.SetValue(self, value or "")

    def OnMeasureItem(self, item):
        return self.popupRowHeight

    def GetValue(self):
        value = wx.combo.OwnerDrawnComboBox.GetValue(self)
        return value