#Boa:FramePanel:pnlQCL

import wx

[wxID_PNLQCL, wxID_PNLQCLLBLCODE, wxID_PNLQCLLBLDEFINITION, 
 wxID_PNLQCLLBLEXPLANATION, wxID_PNLQCLLSTQCL, wxID_PNLQCLRBCREATE, 
 wxID_PNLQCLRBSELECT, wxID_PNLQCLTXTCODE, wxID_PNLQCLTXTDEFINITION, 
 wxID_PNLQCLTXTEXPLANATION, 
] = [wx.NewId() for _init_ctrls in range(10)]

class pnlQCL(wx.Panel):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PNLQCL, name=u'pnlQCL', parent=prnt,
              pos=wx.Point(589, 303), size=wx.Size(439, 357),
              style=wx.TAB_TRAVERSAL)
        self.SetClientSize(wx.Size(423, 319))

        self.rbSelect = wx.RadioButton(id=wxID_PNLQCLRBSELECT,
              label=u'Select an existing Quality Control Level',
              name=u'rbSelect', parent=self, pos=wx.Point(16, 8),
              size=wx.Size(392, 13), style=0)
        self.rbSelect.SetValue(True)
        self.rbSelect.Bind(wx.EVT_RADIOBUTTON, self.OnRbSelectRadiobutton,
              id=wxID_PNLQCLRBSELECT)

        self.rbCreate = wx.RadioButton(id=wxID_PNLQCLRBCREATE,
              label=u'Create Quality Control Level', name=u'rbCreate',
              parent=self, pos=wx.Point(16, 168), size=wx.Size(392, 13),
              style=0)
        self.rbCreate.SetValue(False)
        self.rbCreate.Bind(wx.EVT_RADIOBUTTON, self.OnRbCreateRadiobutton,
              id=wxID_PNLQCLRBCREATE)

        self.lblCode = wx.StaticText(id=wxID_PNLQCLLBLCODE, label=u'Code:',
              name=u'lblCode', parent=self, pos=wx.Point(40, 184),
              size=wx.Size(30, 13), style=0)

        self.txtCode = wx.TextCtrl(id=wxID_PNLQCLTXTCODE, name=u'txtCode',
              parent=self, pos=wx.Point(88, 184), size=wx.Size(320, 21),
              style=0, value=u'')

        self.lblDefinition = wx.StaticText(id=wxID_PNLQCLLBLDEFINITION,
              label=u'Definition:', name=u'lblDefinition', parent=self,
              pos=wx.Point(24, 216), size=wx.Size(50, 13), style=0)

        self.txtDefinition = wx.TextCtrl(id=wxID_PNLQCLTXTDEFINITION,
              name=u'txtDefinition', parent=self, pos=wx.Point(88, 216),
              size=wx.Size(320, 21), style=0, value=u'')

        self.lstQCL = wx.ListCtrl(id=wxID_PNLQCLLSTQCL, name=u'lstQCL',
              parent=self, pos=wx.Point(16, 24), size=wx.Size(392, 136),
              style=wx.LC_REPORT)
        self.lstQCL.Bind(wx.EVT_LIST_ITEM_SELECTED,
              self.OnListCtrl1ListItemSelected, id=wxID_PNLQCLLSTQCL)

        self.txtExplanation = wx.TextCtrl(id=wxID_PNLQCLTXTEXPLANATION,
              name=u'txtExplanation', parent=self, pos=wx.Point(88, 248),
              size=wx.Size(320, 64), style=wx.TE_MULTILINE | wx.TE_WORDWRAP,
              value=u'')

        self.lblExplanation = wx.StaticText(id=wxID_PNLQCLLBLEXPLANATION,
              label=u'Explanation:', name=u'lblExplanation', parent=self,
              pos=wx.Point(16, 248), size=wx.Size(61, 13), style=0)

    def __init__(self, parent, id, pos, size, style, name):
        self._init_ctrls(parent)

    def OnRbSelectRadiobutton(self, event):
        event.Skip()

    def OnRbCreateRadiobutton(self, event):
        event.Skip()

    def OnListCtrl1ListItemSelected(self, event):
        event.Skip()
    

   
