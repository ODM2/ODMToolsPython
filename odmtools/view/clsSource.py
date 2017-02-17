
import wx

class pnlSource(wx.Panel):
    def __init__(self):
        wx.Panel.__init__(self, id=wx.ID_ANY, name=u'pnlSource',
                          parent=prnt, pos=wx.Point(1034, 305), size=wx.Size(439, 357),
                          style=wx.TAB_TRAVERSAL)
        self.SetClientSize(wx.Size(423, 319))

        self.rbCurrent = wx.RadioButton(id=wx.ID_ANY,
                                        label=u'Use Current Source', name=u'rbCurrent', parent=self,
                                        pos=wx.Point(16, 16), size=wx.Size(384, 13), style=0)
        self.rbCurrent.SetValue(True)
        self.rbCurrent.Bind(wx.EVT_RADIOBUTTON, self.OnRbCurrentRadiobutton,
                            id=wxID_PNLVARIABLERBCURRENT)

        self.rbSelect = wx.RadioButton(id=wx.ID_ANY,
                                       label=u'Select an existing Source', name=u'rbSelect',
                                       parent=self, pos=wx.Point(16, 56), size=wx.Size(384, 16),
                                       style=0)
        self.rbSelect.SetValue(False)
        self.rbSelect.Bind(wx.EVT_RADIOBUTTON, self.OnRbSelectRadiobutton,
                           id=wxID_PNLVARIABLERBSELECT)

        self.rbCreate = wx.RadioButton(id=wx.ID_ANY,
                                       label=u'Create New Source', name=u'rbCreate', parent=self,
                                       pos=wx.Point(16, 256), size=wx.Size(368, 13), style=0)
        self.rbCreate.SetValue(False)
        self.rbCreate.Bind(wx.EVT_RADIOBUTTON, self.OnRbCreateRadiobutton,
                           id=wxID_PNLVARIABLERBCREATE)

        self.lstVariable = wx.ListCtrl(id=wx.ID_ANY,
                                       name=u'lstSource', parent=self, pos=wx.Point(16, 80),
                                       size=wx.Size(392, 160), style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.lstVariable.InsertColumn(0, 'Organization')
        self.lstVariable.InsertColumn(1, 'Description')
        self.lstVariable.InsertColumn(2, 'Contact Name')
        self.lstVariable.InsertColumn(3, 'Phone')
        self.lstVariable.InsertColumn(4, 'Email')
        self.lstVariable.InsertColumn(5, 'Address')
        self.lstVariable.InsertColumn(6, 'City')
        self.lstVariable.InsertColumn(7, 'State')
        self.lstVariable.InsertColumn(8, 'ZipCode')
        self.lstVariable.InsertColumn(9, 'Citation')
        self.lstVariable.InsertColumn(10, 'MetaDataID')
        self.lstVariable.SetColumnWidth(0, 50)
        self.lstVariable.SetColumnWidth(1, 100)
        self.lstVariable.SetColumnWidth(10, 0)

        self.lstVariable.Bind(wx.EVT_LIST_ITEM_SELECTED,
                              self.OnListCtrl1ListItemSelected, id=wxID_PNLVARIABLELSTVARIABLE)

        self.lstVariable.Enable(False)

        