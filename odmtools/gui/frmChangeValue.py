#Boa:Frame:frmChangeValue

import wx
from wx.lib.pubsub import pub as Publisher

def create(parent):
    return frmChangeValue(parent)

[wxID_FRMCHANGEVALUE, wxID_FRMCHANGEVALUEBTNAPPLY, 
 wxID_FRMCHANGEVALUEBTNCANCEL, wxID_FRMCHANGEVALUECBVALUE, 
 wxID_FRMCHANGEVALUEPANEL1, wxID_FRMCHANGEVALUETXTVALUE, 
] = [wx.NewId() for _init_ctrls in range(6)]

class frmChangeValue(wx.Dialog):
    def _init_coll_gridSizer1_Items(self, parent):
        # generated method, don't edit

        parent.Add(self.cbValue, 50, border=5, flag=wx.ALL)
        parent.Add(self.txtValue, 50, border=5, flag=wx.ALL)
        parent.Add(self.btnOk, 50, border=5, flag=wx.ALL)
        parent.Add(self.btnCancel, 50, border=5, flag=wx.ALL)

    def _init_sizers(self):
        # generated method, don't edit
        self.gridSizer1 = wx.GridSizer(cols=2, hgap=0, rows=2, vgap=0)

        self._init_coll_gridSizer1_Items(self.gridSizer1)

        self.panel1.SetSizer(self.gridSizer1)

    def _init_ctrls(self, prnt):
        # generated method, don't edit

        wx.Dialog.__init__(self, id=wxID_FRMCHANGEVALUE, name=u'frmChangeValue',
              parent=prnt, pos=wx.Point(732, 489), size=wx.Size(248, 109),
              style=wx.STAY_ON_TOP | wx.DEFAULT_FRAME_STYLE, title=u'Change Value')
        # wx.Frame.__init__(self, id=wxID_FRMCHANGEVALUE, name=u'frmChangeValue',
        #       parent=prnt, pos=wx.Point(732, 489), size=wx.Size(248, 109),
        #       style=wx.STAY_ON_TOP | wx.DEFAULT_FRAME_STYLE,
        #       title=u'Change Value')
        self.SetClientSize(wx.Size(232, 71))
        self.SetMinSize(wx.Size(248, 109))
        self.SetMaxSize(wx.Size(248, 109))

        self.panel1 = wx.Panel(id=wxID_FRMCHANGEVALUEPANEL1, name='panel1',
              parent=self, pos=wx.Point(0, 0), size=wx.Size(232, 71),
              style=wx.TAB_TRAVERSAL)
        self.panel1.SetLabel(u'panel1')

        self.cbValue = wx.ComboBox(choices=['Add', 'Subtract', 'Multiply', 'Set to'], id=wxID_FRMCHANGEVALUECBVALUE,
              name=u'cbValue', parent=self.panel1, pos=wx.Point(5, 5),
              size=wx.Size(104, 21), style=0, value=u'Add')

        self.txtValue = wx.TextCtrl(id=wxID_FRMCHANGEVALUETXTVALUE,
              name=u'txtValue', parent=self.panel1, pos=wx.Point(121, 5),
              size=wx.Size(100, 21), style=0, value=u'')

        self.btnOk = wx.Button(id=wxID_FRMCHANGEVALUEBTNAPPLY,
              label=u'Ok', name=u'btnOk', parent=self.panel1,
              pos=wx.Point(5, 40), size=wx.Size(104, 23), style=0)        
        self.btnOk.Bind(wx.EVT_BUTTON, self.OnBtnOkButton,
              id=wxID_FRMCHANGEVALUEBTNAPPLY)

        self.btnCancel = wx.Button(id=wxID_FRMCHANGEVALUEBTNCANCEL,
              label=u'Cancel', name=u'btnCancel', parent=self.panel1,
              pos=wx.Point(121, 40), size=wx.Size(99, 23), style=0)        
        self.btnCancel.Bind(wx.EVT_BUTTON, self.OnBtnCancelButton,
              id=wxID_FRMCHANGEVALUEBTNCANCEL)

        self._init_sizers()

    def __init__(self, parent, record_service):
      self.record_service = record_service
      self._init_ctrls(parent)

    def OnBtnCancelButton(self, event):
      self.Close()
      event.Skip()

    def OnBtnOkButton(self, event):
      operator = self.cbValue.GetValue()
      value = self.txtValue.GetValue()

      if operator == 'Add':
        operator = '+'
      if operator == 'Subtract':
        operator = '-'
      if operator == 'Multiply':
        operator = '*'
      if operator == 'Set to':
        operator = '='

      self.record_service.change_value(value, operator)
      #Publisher.sendMessage(("updateValues"), event=event)
      self.Close()
