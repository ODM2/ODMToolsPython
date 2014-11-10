# Boa:Dialog:frmFlagValues

import wx

from odmtools.odmdata import Qualifier


def create(parent):
    return frmFlagValues(parent)

NEW = "[New Qualifier]"


class frmFlagValues(wx.Dialog):
    def _init_coll_boxSizer1_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.splitter, 85, border=0, flag=wx.EXPAND)
        parent.AddWindow(self.panel1, 15, border=0, flag=wx.EXPAND)

    def _init_coll_boxSizer2_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.pnlFiller, 60, border=0, flag=0)
        parent.AddWindow(self.btnOK, 0, border=0, flag=0)
        parent.AddSpacer(wx.Size(8, 8), border=0, flag=0)
        parent.AddWindow(self.btnCancel, 0, border=0, flag=0)

    def _init_sizers(self):
        # generated method, don't edit
        self.boxSizer1 = wx.BoxSizer(orient=wx.VERTICAL)

        self.boxSizer2 = wx.BoxSizer(orient=wx.HORIZONTAL)

        self._init_coll_boxSizer1_Items(self.boxSizer1)
        self._init_coll_boxSizer2_Items(self.boxSizer2)

        self.SetSizer(self.boxSizer1)
        self.panel1.SetSizer(self.boxSizer2)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, name=u'frmFlagValues', parent=prnt, pos=wx.Point(554, 325),
                           size=wx.Size(507, 206), style=wx.DEFAULT_DIALOG_STYLE, title=u'Flag Values')
        self.SetClientSize(wx.Size(491, 168))

        self.splitter = wx.SplitterWindow(name='splitter', parent=self,
                                          pos=wx.Point(0, 0), size=wx.Size(491, 142), style=wx.BORDER_SUNKEN)
        self.splitter.SetLabel(u'')
        self.pnlSelect = wx.Panel( name='pnlSelect', parent=self.splitter,
                                  pos=wx.Point(0, 0), size=wx.Size(491, 10), style=wx.TAB_TRAVERSAL)

        self.pnlCreate = wx.Panel( name='pnlCreate', parent=self.splitter,
                                  pos=wx.Point(0, 14), size=wx.Size(491, 178), style=wx.TAB_TRAVERSAL)
        self.pnlCreate.Show(False)

        self.lblQualifier = wx.StaticText( label=u'Qualifier:', name=u'lblQualifier',
                                          parent=self.pnlSelect, pos=wx.Point(16, 8), size=wx.Size(45, 13), style=0)

        self.cbQualif = wx.ComboBox(choices=[x for x in self.qualchoices.keys()] + [NEW], name=u'cbQualif',
                                    parent=self.pnlSelect, pos=wx.Point(16, 25), size=wx.Size(376, 21),
                                    style=wx.CB_READONLY, value=self.selectedValue)
        self.cbQualif.Bind(wx.EVT_COMBOBOX, self.OnCbQualifCombobox)
        self.showNewFields()

        self.lblCode = wx.StaticText( label=u'Code:', name=u'lblCode',
                                     parent=self.pnlCreate, pos=wx.Point(16, 8), size=wx.Size(30, 13), style=0)

        self.lblDesc = wx.StaticText( label=u'Description:', name=u'lblDesc',
                                     parent=self.pnlCreate, pos=wx.Point(16, 35), size=wx.Size(58, 13), style=0)

        self.txtCode = wx.TextCtrl( name=u'txtCode', parent=self.pnlCreate,
                                   pos=wx.Point(75, 8), size=wx.Size(100, 21), style=0, value=u'')

        self.txtDesc = wx.TextCtrl( name=u'txtDesc', parent=self.pnlCreate,
                                   pos=wx.Point(75, 35), size=wx.Size(296, 24), style=0, value=u'')

        self.panel1 = wx.Panel(name='panel1', parent=self, pos=wx.Point(0, 142),
                               size=wx.Size(491, 26), style=wx.TAB_TRAVERSAL)

        self.pnlFiller = wx.Panel( name=u'pnlFiller', parent=self.panel1,
                                  pos=wx.Point(0, 0), size=wx.Size(333, 100), style=wx.TAB_TRAVERSAL)

        self.btnOK = wx.Button(label=u'OK', name=u'btnOK', parent=self.panel1,
                               pos=wx.Point(333, 0), size=wx.Size(75, 23), style=0)
        self.btnOK.Bind(wx.EVT_BUTTON, self.OnBtnOKButton)

        self.btnCancel = wx.Button( label=u'Cancel', name=u'btnCancel',
                                   parent=self.panel1, pos=wx.Point(416, 0), size=wx.Size(75, 23), style=0)
        self.btnCancel.Bind(wx.EVT_BUTTON, self.OnBtnCancelButton)

        self.splitter.Initialize(self.pnlSelect)

        self._init_sizers()

    def __init__(self, parent, cv_service, choices, isNew=False):
        self.cv_service = cv_service

        self.qualchoices = choices
        if isNew:
            self.selectedValue = NEW
            wx.CallAfter(self.showNewFields)
        else:
            self.selectedValue = ''

        self._init_ctrls(parent)

    def GetValue(self):
        if self.qid:
            return self.qid
        else:
            return None

    def OnCbQualifCombobox(self, event):
        self.showNewFields()
        event.Skip()

    def showNewFields(self):
        if self.cbQualif.GetValue() == NEW:
            self.splitter.SplitHorizontally(self.pnlSelect, self.pnlCreate, 50)
        else:
            if self.splitter.IsSplit():
                self.splitter.Unsplit(self.pnlCreate)
                self.splitter.Initialize(self.pnlSelect)


    def OnBtnOKButton(self, event):
        # new
        if self.splitter.IsSplit():
            code = self.txtCode.GetValue()
            desc = self.txtDesc.GetValue()
            if not code or not desc:
                msg = "Please double check that you have entered values into the code field and description field"
                dlg = wx.MessageDialog(None, msg, "Code or Description cannot be empty",
                                       wx.OK | wx.OK_DEFAULT | wx.ICON_WARNING)
                dlg.ShowModal()
                return

            q = Qualifier()
            q.code = code
            q.description = desc

            self.cv_service.create_qualifier(q)
            self.qid = q.id
            self.selectedValue = q.code + '-' + q.description
            self.EndModal(wx.ID_OK)

        else:
            self.qid = self.qualchoices[self.cbQualif.GetValue()]
            self.selectedValue = self.cbQualif.GetValue()
            self.EndModal(wx.ID_CANCEL)

        event.Skip()
        #self.Close()

    def OnBtnCancelButton(self, event):
        self.EndModal(wx.ID_CANCEL)
        event.Skip()
        #self.Close()


