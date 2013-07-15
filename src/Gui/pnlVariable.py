#Boa:FramePanel:pnlVariable

import wx
import frmCreateVariable
from odmdata import Variable

[wxID_PNLVARIABLE, wxID_PNLVARIABLELSTVARIABLE, wxID_PNLVARIABLERBCREATE,
 wxID_PNLVARIABLERBCURRENT, wxID_PNLVARIABLERBSELECT,wxID_PNLVARIABLETXTNEWVAR,
] = [wx.NewId() for _init_ctrls in range(6)]

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
              size=wx.Size(392, 160), style=wx.LC_REPORT|wx.LC_SINGLE_SEL)
        self.lstVariable.InsertColumn(0, 'Code')
        self.lstVariable.InsertColumn(1, 'Name')
        self.lstVariable.InsertColumn(2, 'Speciation')
        self.lstVariable.InsertColumn(3, 'Units')
        self.lstVariable.InsertColumn(4, 'Sample Medium')
        self.lstVariable.InsertColumn(5, 'Value Type')
        self.lstVariable.InsertColumn(6, 'IsRegular')
        self.lstVariable.InsertColumn(7, 'Time Support')
        self.lstVariable.InsertColumn(8, 'Time Units')
        self.lstVariable.InsertColumn(9, 'DataType')
        self.lstVariable.InsertColumn(10, 'General Category')
        self.lstVariable.InsertColumn(11, 'NoDataValue')
        self.lstVariable.InsertColumn(12, 'id')
        self.lstVariable.SetColumnWidth(0, 50)
        self.lstVariable.SetColumnWidth(1, 100)
        self.lstVariable.SetColumnWidth(12,0)

        self.lstVariable.Bind(wx.EVT_LIST_ITEM_SELECTED,
              self.OnListCtrl1ListItemSelected, id=wxID_PNLVARIABLELSTVARIABLE)

        self.lstVariable.Enable(False)

        self.txtNewVar =  wx.TextCtrl(id=wxID_PNLVARIABLETXTNEWVAR,
                  name=u'txtNewVar', parent=self, pos=wx.Point(16,
                 276), size=wx.Size(392, 21), style=0, value=u'')
        self.txtNewVar.Enable(False)

    def __init__(self, parent, id, pos, size, style, name, sm, var):
        self.prev_var= var
        self.service_man = sm
        self.series_service = sm.get_series_service()
        self._init_ctrls(parent)

    def OnRbCurrentRadiobutton(self, event):
        self.lstVariable.Enable(False)

        event.Skip()

    def OnRbSelectRadiobutton(self, event):
        self.lstVariable.Enable(True)

        event.Skip()

    def OnRbCreateRadiobutton(self, event):
        self.lstVariable.Enable(False)

        create_Var = frmCreateVariable.frmCreateVariable(self, self.service_man, self.prev_var)
        create_Var.ShowModal()
        # if cancelled return to previous radio button
        # else enable text box and enter the text info.
        # get Variable object
        event.Skip()

    def OnListCtrl1ListItemSelected(self, event):
        event.Skip()

    def getVariable(self):

        v =  Variable()
        if self.rbCurrent.Value:
            v= self.prev_var
        elif self.rbSelect.Value:
            index = self.lstVariable.GetFirstSelected()
            print self.lstVariable.GetItem(index,-1).GetText()
            v= self.series_service.get_variable_by_id(self.lstVariable.GetItem(index,-1).GetText())
##            index = self.lstVariable.GetFocusedItem()
##            v.id = self.lstVariable.GetItem(index,-1)
##            v.code = self.lstVariables.GetItem(index, 0)
##            v.definition= self.lstVariables.GetItem(index, 1)
##            v.explanation=self.lstVariable.GetItem(index, 2)

        elif self.rbCreate.Value:
            print "Created"
        return v
