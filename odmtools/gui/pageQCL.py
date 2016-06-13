#Boa:FramePanel:pnlQCL

import wx
from odmtools.odmdata import QualityControlLevel

[wxID_PNLQCL, wxID_PNLQCLLBLCODE, wxID_PNLQCLLBLDEFINITION,
 wxID_PNLQCLLBLEXPLANATION, wxID_PNLQCLLSTQCL, wxID_PNLQCLRBCREATE,
 wxID_PNLQCLRBSELECT, wxID_PNLQCLTXTCODE, wxID_PNLQCLTXTDEFINITION,
 wxID_PNLQCLTXTEXPLANATION,
] = [wx.NewId() for _init_ctrls in range(10)]

# from odmtools.common.logger import LoggerTool
import logging
# tool = LoggerTool()
# logger = tool.setupLogger(__name__, __name__ + '.log', 'w', logging.DEBUG)
logger =logging.getLogger('main')

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
        self.txtCode.Enable(False)

        self.lblDefinition = wx.StaticText(id=wxID_PNLQCLLBLDEFINITION,
              label=u'Definition:', name=u'lblDefinition', parent=self,
              pos=wx.Point(24, 216), size=wx.Size(50, 13), style=0)

        self.txtDefinition = wx.TextCtrl(id=wxID_PNLQCLTXTDEFINITION,
              name=u'txtDefinition', parent=self, pos=wx.Point(88, 216),
              size=wx.Size(320, 21), style=0, value=u'')
        self.txtDefinition.Enable(False)

        self.lstQCL = wx.ListCtrl(id=wxID_PNLQCLLSTQCL, name=u'lstQCL',
              parent=self, pos=wx.Point(16, 24), size=wx.Size(392, 136),
              style=wx.LC_REPORT|wx.LC_SINGLE_SEL)
        self.lstQCL.InsertColumn(0, 'Code')
        self.lstQCL.InsertColumn(1, 'Definition')
        self.lstQCL.InsertColumn(2, 'Explanation')
        self.lstQCL.InsertColumn(3, 'id')
        self.lstQCL.SetColumnWidth(0, 50)
        self.lstQCL.SetColumnWidth(1, 50)
        self.lstQCL.SetColumnWidth(2, 200)
        self.lstQCL.SetColumnWidth(3, 0)



        self.lstQCL.Bind(wx.EVT_LIST_ITEM_SELECTED,
              self.OnListCtrl1ListItemSelected, id=wxID_PNLQCLLSTQCL)
        self.lstQCL.Enable(True)

        self.txtExplanation = wx.TextCtrl(id=wxID_PNLQCLTXTEXPLANATION,
              name=u'txtExplanation', parent=self, pos=wx.Point(88, 248),
              size=wx.Size(320, 64), style=wx.TE_MULTILINE | wx.TE_WORDWRAP,
              value=u'')
        self.txtExplanation.Enable(False)

        self.lblExplanation = wx.StaticText(id=wxID_PNLQCLLBLEXPLANATION,
              label=u'Explanation:', name=u'lblExplanation', parent=self,
              pos=wx.Point(16, 248), size=wx.Size(61, 13), style=0)

    def __init__(self, parent, id, pos, size, style, name, ss, qcl):
        self.series_service = ss
        self.prev_val = qcl
        self._init_ctrls(parent)

    def OnRbSelectRadiobutton(self, event):
        self.txtExplanation.Enable(False)
        self.txtDefinition.Enable(False)
        self.txtCode.Enable(False)
        self.lstQCL.Enable(True)
        event.Skip()

    def OnRbCreateRadiobutton(self, event):
        self.txtExplanation.Enable(True)
        self.txtDefinition.Enable(True)
        self.txtCode.Enable(True)
        self.lstQCL.Enable(False)
        event.Skip()

    def OnListCtrl1ListItemSelected(self, event):
        event.Skip()

    def GetLstSelection(self):
        return self.lstQCL.GetFirstSelected()

    def getQCL(self):
        q = QualityControlLevel()
        if self.rbCreate.Value:
            q.code = self.txtCode.Value
            q.definition= self.txtDefinition.Value
            q.explanation = self.txtExplanation.Value

        elif self.rbSelect.Value:
            index = self.GetLstSelection()
            logger.debug("lstQCL: %s" %(self.lstQCL))
            code= self.lstQCL.GetItem(index, 0).GetText()
            logger.debug(code)
            q= self.series_service.get_qcl_by_code(code)

##            q.id = self.lstQCL.GetItem(index,3).GetText()
##            q.code = self.lstQCL.GetItem(index, 0).GetText()
##            q.definition= self.lstQCL.GetItem(index, 1).GetText()
##            q.explanation=self.lstQCL.GetItem(index, 2).GetText()

        return q

