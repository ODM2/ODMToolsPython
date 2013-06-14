#Boa:FramePanel:pnlMethods

import wx
import wx.grid
import wx.richtext

[wxID_PNLMETHOD, wxID_PNLMETHODSLISTCTRL1, wxID_PNLMETHODSRBCREATENEW, 
 wxID_PNLMETHODSRBGENERATE, wxID_PNLMETHODSRBSELECT, 
 wxID_PNLMETHODSRICHTEXTCTRL1, 
] = [wx.NewId() for _init_ctrls in range(6)]

class pnlMethod(wx.Panel):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PNLMETHOD, name=u'pnlMethod',
              parent=prnt, pos=wx.Point(135, 307), size=wx.Size(439, 357),
              style=wx.TAB_TRAVERSAL)
        self.SetClientSize(wx.Size(423, 319))

        self.rbGenerate = wx.RadioButton(id=wxID_PNLMETHODSRBGENERATE,
              label=u'Automatically generate a Method ', name=u'rbGenerate',
              parent=self, pos=wx.Point(16, 8), size=wx.Size(392, 16), style=0)
        self.rbGenerate.SetValue(True)
        self.rbGenerate.Bind(wx.EVT_RADIOBUTTON, self.OnRbGenerateRadiobutton,
              id=wxID_PNLMETHODSRBGENERATE)

        self.rbSelect = wx.RadioButton(id=wxID_PNLMETHODSRBSELECT,
              label=u'Select an existing Method', name=u'rbSelect', parent=self,
              pos=wx.Point(16, 32), size=wx.Size(392, 13), style=0)
        self.rbSelect.SetValue(False)
        self.rbSelect.Bind(wx.EVT_RADIOBUTTON, self.OnRbSelectRadiobutton,
              id=wxID_PNLMETHODSRBSELECT)

        self.rbCreateNew = wx.RadioButton(id=wxID_PNLMETHODSRBCREATENEW,
              label=u'Create a new Method ', name=u'rbCreateNew', parent=self,
              pos=wx.Point(16, 208), size=wx.Size(392, 13), style=0)
        self.rbCreateNew.SetValue(False)
        self.rbCreateNew.Bind(wx.EVT_RADIOBUTTON, self.OnRbCreateNewRadiobutton,
              id=wxID_PNLMETHODSRBCREATENEW)

        self.txtMethodDescrip = wx.richtext.RichTextCtrl(id=wxID_PNLMETHODSRICHTEXTCTRL1,
              parent=self, pos=wx.Point(16, 224), size=wx.Size(392, 84),
              style=wx.richtext.RE_MULTILINE, value=u'Method Description')
        self.txtMethodDescrip.Enable(False)
        self.txtMethodDescrip.Bind(wx.EVT_SET_FOCUS, self.OnTxtMethodDescripSetFocus)
        self.txtMethodDescrip.Bind(wx.EVT_KILL_FOCUS, self.OnTxtMethodDescripKillFocus)  

        self.lstMethods = wx.ListCtrl(id=wxID_PNLMETHODSLISTCTRL1,
              name='lstMethods', parent=self, pos=wx.Point(16, 48),
              size=wx.Size(392, 152), style=wx.LC_REPORT)
        self.lstMethods.Disable()


    def __init__(self, parent, id, pos, size, style, name):
        self._init_ctrls(parent)

    def OnRbGenerateRadiobutton(self, event):
        self.txtMethodDescrip.Enable(False)
        self.lstMethods.Enable(False)
        event.Skip()

    def OnRbSelectRadiobutton(self, event):
        self.txtMethodDescrip.Enable(False)
        self.lstMethods.Enable()
        
        event.Skip()

    def OnRbCreateNewRadiobutton(self, event):
        self.txtMethodDescrip.Enable()   
        self.lstMethods.Enable(False)     
        event.Skip()
    
    def OnTxtMethodDescripSetFocus(self, event):               
        if self.txtMethodDescrip.GetValue() =="Method Description":
            self.txtMethodDescrip.SetValue("")
        event.Skip()
    def OnTxtMethodDescripKillFocus(self, event):
        if self.txtMethodDescrip.GetValue() =="":
            self.txtMethodDescrip.SetValue("Method Description")
