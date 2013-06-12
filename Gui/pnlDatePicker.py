#Boa:FramePanel:Panel1

import wx

[wxID_PANEL1, wxID_PANEL1DPDATE, wxID_PANEL1TXTLABEL, 
] = [wx.NewId() for _init_ctrls in range(3)]

class pnlDatePicker(wx.Panel):


    def _init_ctrls(self, prnt, lblText, minval, maxval, value):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANEL1, name='', parent=prnt,
              pos=wx.Point(648, 277), size=wx.Size(189, 80),
              style=wx.TAB_TRAVERSAL)
        self.SetClientSize(wx.Size(173, 42))

        self.txtLabel = wx.StaticText(id=wxID_PANEL1TXTLABEL, label=lblText,
              name=u'dpDate', parent=self, pos=wx.Point(8, 16),
              size=wx.Size(19, 13), style=0)

        self.dpDate = wx.DatePickerCtrl(id=wxID_PANEL1DPDATE, name=u'dpDate',
              parent=self, pos=wx.Point(64, 8), size=wx.Size(96, 21),
              style=wx.DP_DROPDOWN)
        self.dpDate.SetValue(value)#wx.DateTimeFromDMY(30, 10, 2010, 0, 0, 0)        
        self.dpDate.SetLabel(repr(value))#.strftime("%m-%d-%Y"))#"%Y-%m-%d'"")#'11/30/2010'

    def __init__(self, parent, id, labelText, value, name="", pos="", size="", style="", minval="", maxval=""):
        self._init_ctrls(parent, labelText, minval, maxval, value)
      