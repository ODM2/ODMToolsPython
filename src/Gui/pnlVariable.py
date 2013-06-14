#Boa:FramePanel:pnlVariable

import wx
import frmCreateVariable

[wxID_PNLVARIABLE, wxID_PNLVARIABLELSTVARIABLE, wxID_PNLVARIABLERBCREATE, 
 wxID_PNLVARIABLERBCURRENT, wxID_PNLVARIABLERBSELECT, 
] = [wx.NewId() for _init_ctrls in range(5)]

class pnlVariable(wx.Panel):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PNLVARIABLE, name=u'pnlVariable',
              parent=prnt, pos=wx.Point(1034, 305), size=wx.Size(439, 357),
              style=wx.TAB_TRAVERSAL)
        self.SetClientSize(wx.Size(423, 319))

        self.rbCurrent = wx.RadioButton(id=wxID_PNLVARIABLERBCURRENT,
              label=u'Use Current Variable', name=u'rbCurrent', parent=self,
              pos=wx.Point(16, 16), size=wx.Size(384, 13), style=0)
        self.rbCurrent.SetValue(True)
        self.rbCurrent.Bind(wx.EVT_RADIOBUTTON, self.OnRbCurrentRadiobutton,
              id=wxID_PNLVARIABLERBCURRENT)

        self.rbSelect = wx.RadioButton(id=wxID_PNLVARIABLERBSELECT,
              label=u'Select an existing Variable', name=u'rbSelect',
              parent=self, pos=wx.Point(16, 56), size=wx.Size(384, 16),
              style=0)
        self.rbSelect.SetValue(False)
        self.rbSelect.Bind(wx.EVT_RADIOBUTTON, self.OnRbSelectRadiobutton,
              id=wxID_PNLVARIABLERBSELECT)

        self.rbCreate = wx.RadioButton(id=wxID_PNLVARIABLERBCREATE,
              label=u'Create New Variable', name=u'rbCreate', parent=self,
              pos=wx.Point(16, 256), size=wx.Size(368, 13), style=0)
        self.rbCreate.SetValue(False)
        self.rbCreate.Bind(wx.EVT_RADIOBUTTON, self.OnRbCreateRadiobutton,
              id=wxID_PNLVARIABLERBCREATE)
        

        self.lstVariable = wx.ListCtrl(id=wxID_PNLVARIABLELSTVARIABLE,
              name=u'lstVariable', parent=self, pos=wx.Point(16, 80),
              size=wx.Size(392, 160), style=wx.LC_REPORT)
        self.lstVariable.Bind(wx.EVT_LIST_ITEM_SELECTED,
              self.OnListCtrl1ListItemSelected, id=wxID_PNLVARIABLELSTVARIABLE)
        self.lstVariable.Enable(False)

    def __init__(self, parent, id, pos, size, style, name):
        self._init_ctrls(parent)

    def OnRbCurrentRadiobutton(self, event):
        self.lstVariable.Enable(False)

        event.Skip()

    def OnRbSelectRadiobutton(self, event):
        self.lstVariable.Enable(True)

        event.Skip()

    def OnRbCreateRadiobutton(self, event):
        self.lstVariable.Enable(False)

        create_Var = frmCreateVariable.frmCreateVariable(self)
        create_Var.ShowModal()
        event.Skip()

    def OnListCtrl1ListItemSelected(self, event):
        event.Skip()
