#Boa:Dialog:frmLinearDrift

import wx
from wx.lib.pubsub import pub as Publisher

def create(parent):
    return frmLinearDrift(parent)

[wxID_FRMLINEARDRIFT, wxID_FRMLINEARDRIFTBTNCANCEL, wxID_FRMLINEARDRIFTBTNOK,
 wxID_FRMLINEARDRIFTLBLFNLGAP, wxID_FRMLINEARDRIFTLBLMESSAGE,
 wxID_FRMLINEARDRIFTTXTFINALGAPVALUE,
] = [wx.NewId() for _init_ctrls in range(6)]

class frmLinearDrift(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_FRMLINEARDRIFT, name=u'frmLinearDrift',
              parent=prnt, pos=wx.Point(610, 334), size=wx.Size(286, 130),
              style=wx.DEFAULT_DIALOG_STYLE, title=u'Linear Drift Correction ')
        self.SetClientSize(wx.Size(270, 92))

        self.lblFnlGap = wx.StaticText(id=wxID_FRMLINEARDRIFTLBLFNLGAP,
              label=u'Final Gap Value:', name=u'lblFnlGap', parent=self,
              pos=wx.Point(16, 48), size=wx.Size(78, 13), style=0)

        self.lblMessage = wx.StaticText(id=wxID_FRMLINEARDRIFTLBLMESSAGE,
              label=u'Enter a negative value to move points down. \nEnter a positive value to move points up.',
              name=u'lblMessage', parent=self, pos=wx.Point(16, 8),
              #size=wx.Size(248, 26), style=0
              size=wx.Size(248, 30), style=0
        )

        self.txtFinalGapValue = wx.TextCtrl(id=wxID_FRMLINEARDRIFTTXTFINALGAPVALUE,
              name=u'txtFinalGapValue', parent=self, pos=wx.Point(100, 40),
              size=wx.Size(164, 21), style=0, value=u'')

        self.btnOK = wx.Button(id=wxID_FRMLINEARDRIFTBTNOK, label=u'OK',
              name=u'btnOK', parent=self, pos=wx.Point(104, 64),
              size=wx.Size(75, 23), style=0)
        self.btnOK.Bind(wx.EVT_BUTTON, self.OnBtnOKButton,
              id=wxID_FRMLINEARDRIFTBTNOK)

        self.btnCancel = wx.Button(id=wxID_FRMLINEARDRIFTBTNCANCEL,
              label=u'Cancel', name=u'btnCancel', parent=self, pos=wx.Point(184,
              64), size=wx.Size(75, 23), style=0)
        self.btnCancel.Bind(wx.EVT_BUTTON, self.OnBtnCancelButton,
              id=wxID_FRMLINEARDRIFTBTNCANCEL)

    def __init__(self, parent, record_service):
        self._record_service = record_service
        self._init_ctrls(parent)

    def OnBtnOKButton(self, event):
        self._record_service.drift_correction(float(self.txtFinalGapValue.GetValue()))

        #Publisher.sendMessage(("updateValues"), event=event)
        self.Close()

    def OnBtnCancelButton(self, event):
        event.Skip()
        self.Close()
