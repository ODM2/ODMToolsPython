#Boa:FramePanel:pnlMethods

import wx
import wx.grid
import wx.richtext
# from odmtools.odmdata import ODM
from odm2api.ODM2.models import Methods


[wxID_PNLMETHOD, wxID_PNLMETHODSLISTCTRL1, wxID_PNLMETHODSRBCREATENEW,
 wxID_PNLMETHODSRBGENERATE, wxID_PNLMETHODSRBSELECT,
 wxID_PNLMETHODSRICHTEXTCTRL1,
] = [wx.NewId() for _init_ctrls in range(6)]

# from odmtools.common.logger import LoggerTool
import logging
# tool = LoggerTool()
# logger = tool.setupLogger(__name__, __name__ + '.log', 'w', logging.DEBUG)
logger =logging.getLogger('main')

<<<<<<< HEAD

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
              size=wx.Size(392, 152), style=wx.LC_REPORT|wx.LC_SINGLE_SEL)
        self.lstMethods.Bind(wx.EVT_SET_FOCUS, self.OnLstMethodSetFocus)


        self.lstMethods.InsertColumn(0, 'Description')
        self.lstMethods.InsertColumn(1, 'Link')
        self.lstMethods.InsertColumn(2, 'id')
        self.lstMethods.SetColumnWidth(0, 200)
        self.lstMethods.SetColumnWidth(1, 153)
        self.lstMethods.SetColumnWidth(2,0)
        # self.lstMethods.Enable(False)




    def __init__(self, parent, id, pos, size, style, name, ss, method):
        self.series_service = ss
        self.prev_val = method
        self._init_ctrls(parent)

    def OnLstMethodSetFocus(self, event):
        self.rbSelect.SetValue(True)

    def OnRbGenerateRadiobutton(self, event):
        # self.lstMethods.Enable(False)
        self.txtMethodDescrip.Enable(False)

        event.Skip()

    def OnRbSelectRadiobutton(self, event):
        self.lstMethods.Enable(True)
        self.txtMethodDescrip.Enable(False)

        event.Skip()

    def OnRbCreateNewRadiobutton(self, event):
        # self.lstMethods.Enable(False)
        self.txtMethodDescrip.Enable(True)

        event.Skip()

    def OnTxtMethodDescripSetFocus(self, event):
        if self.txtMethodDescrip.GetValue() =="Method Description":
            self.txtMethodDescrip.SetValue("")

        event.Skip()

    def OnTxtMethodDescripKillFocus(self, event):
        if self.txtMethodDescrip.GetValue() =="":
            self.txtMethodDescrip.SetValue("Method Description")

        event.Skip()


    def getMethod(self):

        m = None
        if self.rbGenerate.Value:
            genmethod = "Values derived from ODM Tools Python"

            m= self.series_service.get_method_by_description(genmethod)
            if m is None:
                logger.debug("assigning new method description")
                m = Methods()
                m.MethodDescription = genmethod


        elif self.rbSelect.Value:
            index = self.lstMethods.GetFirstSelected()
            desc= self.lstMethods.GetItem(index, 0).GetText()

            logger.debug(desc)
            m= self.series_service.get_method_by_description(desc)



        elif self.rbCreateNew.Value:

            logger.debug("assigning new method description")
            m.description = self.txtMethodDescrip.GetValue()

        return m
=======
class pnlMethod(wx.Panel):  # Rename this to page method view
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # Create components
        header_text = wx.StaticText(self, label="Method")
        static_line = wx.StaticLine(self, size=(-1, 12))

        required_static_box_sizer = wx.StaticBoxSizer(box=wx.StaticBox(self, label="Required Fields"), orient=wx.VERTICAL)
        method_code_text = wx.StaticText(self, label="Method Code")
        self.method_code_text_ctrl = wx.TextCtrl(self)
        method_name_text = wx.StaticText(self, label="Method Name")
        self.method_name_text_ctrl = wx.TextCtrl(self)
        method_type_text = wx.StaticText(self, label="Method Type")
        self.method_type_combo = wx.ComboBox(self)

        optional_static_box_sizer = wx.StaticBoxSizer(box=wx.StaticBox(self, label="Optional Fields"), orient=wx.VERTICAL)
        organization_text = wx.StaticText(self, label="Organization")
        self.organization_text_ctrl = wx.TextCtrl(self)
        method_link_text = wx.StaticText(self, label="Method Link")
        self.method_link_text_ctrl = wx.TextCtrl(self)
        description_text = wx.StaticText(self, label="Description")
        self.description_text_ctrl = wx.TextCtrl(self, size=(-1, 75))

        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        row_sizer.Add(method_code_text, 0, wx.EXPAND)
        row_sizer.Add(self.method_code_text_ctrl, 1, wx.EXPAND | wx.LEFT, 24)
        required_static_box_sizer.Add(row_sizer, 0, wx.EXPAND | wx.ALL, 5)

        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        row_sizer.Add(method_name_text, 0, wx.EXPAND)
        row_sizer.Add(self.method_name_text_ctrl, 1, wx.EXPAND | wx.LEFT, 20)
        required_static_box_sizer.Add(row_sizer, 0, wx.EXPAND | wx.ALL, 5)

        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        row_sizer.Add(method_type_text, 0, wx.EXPAND)
        row_sizer.Add(self.method_type_combo, 1, wx.EXPAND | wx.LEFT, 26)
        required_static_box_sizer.Add(row_sizer, 0, wx.EXPAND | wx.ALL, 5)

        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        row_sizer.Add(organization_text, 0, wx.EXPAND)
        row_sizer.Add(self.organization_text_ctrl, 1, wx.EXPAND | wx.LEFT, 27)
        optional_static_box_sizer.Add(row_sizer, 0, wx.EXPAND | wx.ALL, 5)

        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        row_sizer.Add(method_link_text, 0, wx.EXPAND)
        row_sizer.Add(self.method_link_text_ctrl, 1, wx.EXPAND | wx.LEFT, 27)
        optional_static_box_sizer.Add(row_sizer, 0, wx.EXPAND | wx.ALL, 5)

        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        row_sizer.Add(description_text, 0, wx.EXPAND)
        row_sizer.Add(self.description_text_ctrl, 1, wx.EXPAND | wx.LEFT, 34)
        optional_static_box_sizer.Add(row_sizer, 0, wx.EXPAND | wx.ALL, 5)

        # Style Components
        font = wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD)
        header_text.SetFont(font)

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Add components to sizer
        main_sizer.Add(header_text, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        main_sizer.Add(static_line, 0, wx.EXPAND | wx.TOP, 5)
        main_sizer.Add(required_static_box_sizer, 0, wx.EXPAND | wx.TOP, 10)
        main_sizer.Add(optional_static_box_sizer, 0, wx.EXPAND | wx.TOP, 10)
        self.SetSizer(main_sizer)

# class pnlMethod(wx.Panel):
#     def _init_ctrls(self, prnt):
#         # generated method, don't edit
#         wx.Panel.__init__(self, id=wxID_PNLMETHOD, name=u'pnlMethod',
#               parent=prnt, pos=wx.Point(135, 307), size=wx.Size(439, 357),
#               style=wx.TAB_TRAVERSAL)
#         self.SetClientSize(wx.Size(423, 319))
#
#         self.rbGenerate = wx.RadioButton(id=wxID_PNLMETHODSRBGENERATE,
#               label=u'Automatically generate a Method ', name=u'rbGenerate',
#               parent=self, pos=wx.Point(16, 8), size=wx.Size(392, 16), style=0)
#         self.rbGenerate.SetValue(True)
#         self.rbGenerate.Bind(wx.EVT_RADIOBUTTON, self.OnRbGenerateRadiobutton,
#               id=wxID_PNLMETHODSRBGENERATE)
#
#         self.rbSelect = wx.RadioButton(id=wxID_PNLMETHODSRBSELECT,
#               label=u'Select an existing Method', name=u'rbSelect', parent=self,
#               pos=wx.Point(16, 32), size=wx.Size(392, 13), style=0)
#         self.rbSelect.SetValue(False)
#         self.rbSelect.Bind(wx.EVT_RADIOBUTTON, self.OnRbSelectRadiobutton,
#               id=wxID_PNLMETHODSRBSELECT)
#
#         self.rbCreateNew = wx.RadioButton(id=wxID_PNLMETHODSRBCREATENEW,
#               label=u'Create a new Method ', name=u'rbCreateNew', parent=self,
#               pos=wx.Point(16, 208), size=wx.Size(392, 13), style=0)
#         self.rbCreateNew.SetValue(False)
#         self.rbCreateNew.Bind(wx.EVT_RADIOBUTTON, self.OnRbCreateNewRadiobutton,
#               id=wxID_PNLMETHODSRBCREATENEW)
#
#         self.txtMethodDescrip = wx.richtext.RichTextCtrl(id=wxID_PNLMETHODSRICHTEXTCTRL1,
#               parent=self, pos=wx.Point(16, 224), size=wx.Size(392, 84),
#               style=wx.richtext.RE_MULTILINE, value=u'Method Description')
#         self.txtMethodDescrip.Enable(False)
#         self.txtMethodDescrip.Bind(wx.EVT_SET_FOCUS, self.OnTxtMethodDescripSetFocus)
#         self.txtMethodDescrip.Bind(wx.EVT_KILL_FOCUS, self.OnTxtMethodDescripKillFocus)
#
#         self.lstMethods = wx.ListCtrl(id=wxID_PNLMETHODSLISTCTRL1,
#               name='lstMethods', parent=self, pos=wx.Point(16, 48),
#               size=wx.Size(392, 152), style=wx.LC_REPORT|wx.LC_SINGLE_SEL)
#         self.lstMethods.Bind(wx.EVT_SET_FOCUS, self.OnLstMethodSetFocus)
#
#
#         self.lstMethods.InsertColumn(0, 'Description')
#         self.lstMethods.InsertColumn(1, 'Link')
#         self.lstMethods.InsertColumn(2, 'id')
#         self.lstMethods.SetColumnWidth(0, 200)
#         self.lstMethods.SetColumnWidth(1, 153)
#         self.lstMethods.SetColumnWidth(2,0)
#         # self.lstMethods.Enable(False)
#
#
#
#
#     def __init__(self, parent, id, pos, size, style, name, ss, method):
#         self.series_service = ss
#         self.prev_val = method
#         self._init_ctrls(parent)
#
#     def OnLstMethodSetFocus(self, event):
#         self.rbSelect.SetValue(True)
#
#     def OnRbGenerateRadiobutton(self, event):
#         # self.lstMethods.Enable(False)
#         self.txtMethodDescrip.Enable(False)
#
#         event.Skip()
#
#     def OnRbSelectRadiobutton(self, event):
#         self.lstMethods.Enable(True)
#         self.txtMethodDescrip.Enable(False)
#
#         event.Skip()
#
#     def OnRbCreateNewRadiobutton(self, event):
#         # self.lstMethods.Enable(False)
#         self.txtMethodDescrip.Enable(True)
#
#         event.Skip()
#
#     def OnTxtMethodDescripSetFocus(self, event):
#         if self.txtMethodDescrip.GetValue() =="Method Description":
#             self.txtMethodDescrip.SetValue("")
#
#         event.Skip()
#
#     def OnTxtMethodDescripKillFocus(self, event):
#         if self.txtMethodDescrip.GetValue() =="":
#             self.txtMethodDescrip.SetValue("Method Description")
#
#         event.Skip()
#
#
#     def getMethod(self):
#
#         m =  Method()
#         if self.rbGenerate.Value:
#             genmethod = "Values derived from ODM Tools Python"
#             m= self.series_service.get_method_by_description(genmethod)
#             if m is None:
#                 logger.debug("assigning new method description")
#                 m =  Method()
#                 m.description = genmethod
#
#         elif self.rbSelect.Value:
#             index = self.lstMethods.GetFirstSelected()
#             desc= self.lstMethods.GetItem(index, 0).GetText()
#
#             logger.debug(desc)
#             m= self.series_service.get_method_by_description(desc)
#
#
#
#         elif self.rbCreateNew.Value:
#             logger.debug("assigning new method description")
#             m.description = self.txtMethodDescrip.GetValue()
#         return m
>>>>>>> origin/update_cvs
