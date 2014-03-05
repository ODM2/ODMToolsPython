#Boa:Frame:frmDataFilter

from datetime import datetime
import logging

import wx
from wx.lib.pubsub import pub as Publisher


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
console.setFormatter(
    logging.Formatter('%(asctime)s - %(levelname)s - %(name)s.%(funcName)s() (%(lineno)d): %(message)s')
)
logger.addHandler(console)

def create(parent):
    return frmDataFilter(parent)

[wxID_FRMDATAFILTER, wxID_FRMDATAFILTERBTNAPPLY, wxID_FRMDATAFILTERBTNCANCEL,
 wxID_FRMDATAFILTERBTNCLEAR, wxID_FRMDATAFILTERBTNOK,
 wxID_FRMDATAFILTERCBGAPTIME, wxID_FRMDATAFILTERDBAFTER,
 wxID_FRMDATAFILTERDPBEFORE, wxID_FRMDATAFILTERLBLDATEAFTER,
 wxID_FRMDATAFILTERLBLDATEBEFORE, wxID_FRMDATAFILTERLBLGAPSTIME,
 wxID_FRMDATAFILTERLBLGAPVALUE, wxID_FRMDATAFILTERLBLTHRESHVALGT,
 wxID_FRMDATAFILTERLBLTHRESHVALLT, wxID_FRMDATAFILTERPANEL1,
 wxID_FRMDATAFILTERRBDATAGAPS, wxID_FRMDATAFILTERRBDATE,
 wxID_FRMDATAFILTERRBTHRESHOLD, wxID_FRMDATAFILTERRBVCHANGETHRESH,
 wxID_FRMDATAFILTERSBDATE, wxID_FRMDATAFILTERSBGAPS,
 wxID_FRMDATAFILTERSBTHRESHOLD, wxID_FRMDATAFILTERTXTGAPSVAL,
 wxID_FRMDATAFILTERTXTTHRESHVALGT, wxID_FRMDATAFILTERTXTTHRESVALLT,
 wxID_FRMDATAFILTERTXTVCHANGETHRESH, wxID_FRMDATAFILTERCHKFILTER,
] = [wx.NewId() for _init_ctrls in range(27)]

class frmDataFilter(wx.Dialog):
    def _init_ctrls(self, prnt):
        self.is_applied = False
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_FRMDATAFILTER, name=u'frmDataFilter',
              parent=prnt, pos=wx.Point(599, 384), size=wx.Size(313, 400),
              style=wx.DEFAULT_DIALOG_STYLE, title=u'Data Filter')
        self.SetClientSize(wx.Size(297, 370))
        self.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL, False,
              u'MS Shell Dlg 2'))

        self.panel1 = wx.Panel(id=wxID_FRMDATAFILTERPANEL1, name='panel1',
              parent=self, pos=wx.Point(0, 0), size=wx.Size(297, 370),
              style=wx.TAB_TRAVERSAL)

        self.sbThreshold = wx.StaticBox(id=wxID_FRMDATAFILTERSBTHRESHOLD,
              label=u'Value Threshold', name=u'sbThreshold', parent=self.panel1,
              pos=wx.Point(16, 8), size=wx.Size(272, 72), style=0)
        self.sbThreshold.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              u'MS Shell Dlg 2'))

        self.sbGaps = wx.StaticBox(id=wxID_FRMDATAFILTERSBGAPS,
              label=u'Data Gaps', name=u'sbGaps', parent=self.panel1,
              pos=wx.Point(16, 88), size=wx.Size(272, 72), style=0)
        self.sbGaps.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              u'MS Shell Dlg 2'))

        self.sbDate = wx.StaticBox(id=wxID_FRMDATAFILTERSBDATE, label=u'Date',
              name=u'sbDate', parent=self.panel1, pos=wx.Point(16, 168),
              size=wx.Size(264, 112), style=0)
        self.sbDate.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              u'MS Shell Dlg 2'))

        self.rbThreshold = wx.RadioButton(id=wxID_FRMDATAFILTERRBTHRESHOLD,
              label=u'', name=u'rbThreshold', parent=self.panel1,
              pos=wx.Point(8, 8), size=wx.Size(16, 13), style=0)
        self.rbThreshold.SetValue(True)

        self.rbDataGaps = wx.RadioButton(id=wxID_FRMDATAFILTERRBDATAGAPS,
              label=u'', name=u'rbDataGaps', parent=self.panel1, pos=wx.Point(8,
              88), size=wx.Size(16, 13), style=0)

        self.rbDate = wx.RadioButton(id=wxID_FRMDATAFILTERRBDATE, label=u'',
              name=u'rbDate', parent=self.panel1, pos=wx.Point(8, 168),
              size=wx.Size(16, 13), style=0)

        self.rbVChangeThresh = wx.RadioButton(id=wxID_FRMDATAFILTERRBVCHANGETHRESH,
              label=u'Value Change Threshold >=', name=u'rbVChangeThresh',
              parent=self.panel1, pos=wx.Point(8, 288), size=wx.Size(152, 13),
              style=0)
        self.rbVChangeThresh.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, u'MS Shell Dlg 2'))

        self.lblThreshValGT = wx.StaticText(id=wxID_FRMDATAFILTERLBLTHRESHVALGT,
              label=u'Value >', name=u'lblThreshValGT', parent=self.panel1,
              pos=wx.Point(24, 32), size=wx.Size(38, 13), style=0)

        self.lblThreshValLT = wx.StaticText(id=wxID_FRMDATAFILTERLBLTHRESHVALLT,
              label=u'Value<', name=u'lblThreshValLT', parent=self.panel1,
              pos=wx.Point(24, 56), size=wx.Size(35, 13), style=0)

        self.txtThreshValGT = wx.TextCtrl(id=wxID_FRMDATAFILTERTXTTHRESHVALGT,
              name=u'txtThreshValGT', parent=self.panel1, pos=wx.Point(72, 24),
              size=wx.Size(200, 21), style=0, value='')

        self.txtThreshValLT = wx.TextCtrl(id=wxID_FRMDATAFILTERTXTTHRESVALLT,
              name=u'txtThresValLT', parent=self.panel1, pos=wx.Point(72, 48),
              size=wx.Size(200, 21), style=0, value='')

        self.lblGapValue = wx.StaticText(id=wxID_FRMDATAFILTERLBLGAPVALUE,
              label=u'Value:', name=u'lblGapValue', parent=self.panel1,
              pos=wx.Point(32, 112), size=wx.Size(31, 13), style=0)

        self.lblGapsTime = wx.StaticText(id=wxID_FRMDATAFILTERLBLGAPSTIME,
              label=u'Time Period:', name=u'lblGapsTime', parent=self.panel1,
              pos=wx.Point(32, 136), size=wx.Size(60, 13), style=0)

        self.txtGapsVal = wx.TextCtrl(id=wxID_FRMDATAFILTERTXTGAPSVAL,
              name=u'txtGapsVal', parent=self.panel1, pos=wx.Point(80, 104),
              size=wx.Size(192, 21), style=0, value='')

        self.cbGapTime = wx.ComboBox(choices=['second', 'minute', 'hour',
              'day'], id=wxID_FRMDATAFILTERCBGAPTIME, name=u'cbGapTime',
              parent=self.panel1, pos=wx.Point(96, 128), size=wx.Size(176, 21),
              style=0, value='second')

        self.lblDateAfter = wx.StaticText(id=wxID_FRMDATAFILTERLBLDATEAFTER,
              label=u'After:', name=u'lblDateAfter', parent=self.panel1,
              pos=wx.Point(24, 232), size=wx.Size(30, 13), style=0)

        self.lblDateBefore = wx.StaticText(id=wxID_FRMDATAFILTERLBLDATEBEFORE,
              label=u'Before:', name=u'lblDateBefore', parent=self.panel1,
              pos=wx.Point(24, 184), size=wx.Size(37, 13), style=0)

        self.dpAfter = wx.DatePickerCtrl(id=wxID_FRMDATAFILTERDBAFTER,
              name=u'dbAfter', parent=self.panel1, pos=wx.Point(24, 248),
              size=wx.Size(248, 21), style=wx.DP_DROPDOWN | wx.DP_SHOWCENTURY)

        self.dpBefore = wx.DatePickerCtrl(id=wxID_FRMDATAFILTERDPBEFORE,
              name=u'dpBefore', parent=self.panel1, pos=wx.Point(24, 200),
              size=wx.Size(248, 21), style=wx.DP_DROPDOWN | wx.DP_SHOWCENTURY)

        self.txtVChangeThresh = wx.TextCtrl(id=wxID_FRMDATAFILTERTXTVCHANGETHRESH,
              name=u'changeThresh', parent=self.panel1, pos=wx.Point(168, 280),
              size=wx.Size(100, 21), style=0, value='')

        self.chkToggleFilterSelection = wx.CheckBox(id=wxID_FRMDATAFILTERCHKFILTER,
              name=u'checkbox', label=u'Filter from previous filter',
              parent=self.panel1, pos=wx.Point(8, 306),
              size=wx.Size(232,25), style=0)
        self.chkToggleFilterSelection.Bind(wx.EVT_CHECKBOX, self.onCheckbox,
              id=wxID_FRMDATAFILTERCHKFILTER)

        self.btnClear = wx.Button(id=wxID_FRMDATAFILTERBTNCLEAR,
              label=u'Clear Filter', name=u'btnClear', parent=self.panel1,
              pos=wx.Point(8, 335), size=wx.Size(64, 23), style=0)
        self.btnClear.Bind(wx.EVT_BUTTON, self.onBtnClearButton,
              id=wxID_FRMDATAFILTERBTNCLEAR)

        self.btnOK = wx.Button(id=wxID_FRMDATAFILTERBTNOK, label=u'OK',
              name=u'btnOK', parent=self.panel1, pos=wx.Point(128, 335),
              size=wx.Size(48, 23), style=0)
        self.btnOK.Bind(wx.EVT_BUTTON, self.onBtnOKButton,
              id=wxID_FRMDATAFILTERBTNOK)

        self.btnCancel = wx.Button(id=wxID_FRMDATAFILTERBTNCANCEL,
              label=u'Cancel', name=u'btnCancel', parent=self.panel1,
              pos=wx.Point(184, 335), size=wx.Size(48, 23), style=0)
        self.btnCancel.Bind(wx.EVT_BUTTON, self.onBtnCancelButton,
              id=wxID_FRMDATAFILTERBTNCANCEL)

        self.btnApply = wx.Button(id=wxID_FRMDATAFILTERBTNAPPLY, label=u'Apply',
              name=u'btnApply', parent=self.panel1, pos=wx.Point(240, 335),
              size=wx.Size(48, 23), style=0)
        self.btnApply.Bind(wx.EVT_BUTTON, self.onBtnApplyButton,
              id=wxID_FRMDATAFILTERBTNAPPLY)


        self.setDates()

    def __init__(self, parent, series):
        self.recordService = series
        self._init_ctrls(parent)

    def onCheckbox(self, event):
      self.recordService.toggle_filter_previous()

    def onBtnClearButton(self, event):
        self.setDates()
        self.txtThreshValGT.Clear()
        self.txtThreshValLT.Clear()
        self.txtGapsVal.Clear()
        self.cbGapTime.SetStringSelection("second")
        self.txtVChangeThresh.Clear()
        self.recordService.reset_filter()

        Publisher.sendMessage(("changePlotSelection"), sellist=self.recordService.get_filter_list())

    def onBtnOKButton(self, event):
        if not self.is_applied:
            self.onBtnApplyButton(event)
        self.Close()

    def onBtnCancelButton(self, event):
        self.Close()

    def onBtnApplyButton(self, event):
        self.is_applied = True
        if self.rbThreshold.GetValue():
          if self.txtThreshValGT.GetValue():
            self.recordService.filter_value(float(self.txtThreshValGT.GetValue()), '>')
          if self.txtThreshValLT.GetValue():
            self.recordService.filter_value(float(self.txtThreshValLT.GetValue()), '<')

        if self.rbDataGaps.GetValue():
          if self.txtGapsVal.GetValue():
            self.recordService.data_gaps(float(self.txtGapsVal.GetValue()), self.cbGapTime.GetValue())

        if self.rbDate.GetValue():
          dateAfter = self.dpAfter.GetValue()
          dateBefore = self.dpBefore.GetValue()

          dtDateAfter = datetime(int(dateAfter.Year), int(dateAfter.Month) + 1, int(dateAfter.Day))
          dtDateBefore = datetime(int(dateBefore.Year), int(dateBefore.Month) + 1, int(dateBefore.Day))
          self.recordService.filter_date(dtDateBefore, dtDateAfter)

        if self.rbVChangeThresh.GetValue():
          if self.txtVChangeThresh.GetValue():
            self.recordService.value_change_threshold(float(self.txtVChangeThresh.GetValue()))

        Publisher.sendMessage("changePlotSelection", sellist=self.recordService.get_filter_list())


    def setDates(self):
      dateAfter = self.recordService.get_series_points()[0][2]
      dateBefore = self.recordService.get_series_points()[-1][2]

      logger.debug("dateAfter: ", dateAfter.day, " + ", dateAfter.month, " + ", dateAfter.year)
      logger.debug("dateBefore: ", dateBefore.day, " + ", dateBefore.month, " + ", dateBefore.year)

      formattedDateAfter = wx.DateTimeFromDMY(int(dateAfter.day), int(dateAfter.month), int(dateAfter.year), 0, 0, 0)

      formattedDateBefore = wx.DateTimeFromDMY(int(dateBefore.day) + 1, int(dateBefore.month), int(dateBefore.year), 0, 0, 0)
      self.dpAfter.SetRange(formattedDateAfter, formattedDateBefore)
      self.dpBefore.SetRange(formattedDateAfter, formattedDateBefore)
      self.dpAfter.SetValue(formattedDateAfter)
      self.dpBefore.SetValue(formattedDateBefore)