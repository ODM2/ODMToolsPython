#Boa:FramePanel:pnlIntro

import wx

[wxID_PNLINTRO, wxID_PNLINTROLBLHOW, wxID_PNLINTRORBSAVE, 
 wxID_PNLINTRORBSAVEAS, 
] = [wx.NewId() for _init_ctrls in range(4)]

class pnlIntro(wx.Panel):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PNLINTRO, name=u'pnlIntro', parent=prnt,
              pos=wx.Point(571, 262), size=wx.Size(439, 357),
              style=wx.TAB_TRAVERSAL)
        self.SetClientSize(wx.Size(423, 319))

        self.rbSave = wx.RadioButton(id=wxID_PNLINTRORBSAVE,
              label=u'Save  (Save the data using the same series Catalog Entry',
              name=u'rbSave', parent=self, pos=wx.Point(64, 64),
              size=wx.Size(352, 16), style=0)
        self.rbSave.SetValue(True)
        self.rbSave.Bind(wx.EVT_RADIOBUTTON, self.OnBtnSaveRadiobutton,
              id=wxID_PNLINTRORBSAVE)

        self.rbSaveAs = wx.RadioButton(id=wxID_PNLINTRORBSAVEAS,
              label=u'Save As...(Create a new Series Catalog Entry)',
              name=u'rbSaveAs', parent=self, pos=wx.Point(64, 96),
              size=wx.Size(352, 16), style=0)
        self.rbSaveAs.SetValue(True)
        self.rbSaveAs.Bind(wx.EVT_RADIOBUTTON, self.OnBtnSaveAsRadiobutton,
              id=wxID_PNLINTRORBSAVEAS)

        self.lblHow = wx.StaticText(id=wxID_PNLINTROLBLHOW,
              label=u'How would you like to save the series?', name=u'lblHow',
              parent=self, pos=wx.Point(32, 32), size=wx.Size(376, 13),
              style=0)

    def __init__(self, parent, id, pos, size, style, name):
        self._init_ctrls(parent)

    def OnBtnSaveRadiobutton(self, event):
        event.Skip()

    def OnBtnSaveAsRadiobutton(self, event):
        event.Skip()
