
import wx

class clsSource(wx.Panel):
    def __init__(self,prnt,id,pos,size,style,name):
        wx.Panel.__init__(self, id=id, name=name,
                          parent=prnt, pos=pos, size=size,
                          style=style)


        self.SetClientSize(wx.Size(423, 319))

        self.rbCurrent = wx.RadioButton(id=wx.ID_ANY,
                                        label=u'Use Current Source', name=u'rbCurrent', parent=self,
                                        pos=wx.Point(16, 16), size=wx.Size(384, 13), style=0)
        self.rbCurrent.SetValue(True)
        self.rbCurrent.Bind(wx.EVT_RADIOBUTTON, self.OnRbCurrentRadiobutton)

        self.rbSelect = wx.RadioButton(id=wx.ID_ANY,
                                       label=u'Select an existing Source', name=u'rbSelect',
                                       parent=self, pos=wx.Point(16, 56), size=wx.Size(384, 16),
                                       style=0)
        self.rbSelect.SetValue(False)
        self.rbSelect.Bind(wx.EVT_RADIOBUTTON, self.OnRbSelectRadiobutton)

        self.rbCreate = wx.RadioButton(id=wx.ID_ANY,
                                       label=u'Create New Source', name=u'rbCreate', parent=self,
                                       pos=wx.Point(16, 256), size=wx.Size(368, 13), style=0)
        self.rbCreate.SetValue(False)
        self.rbCreate.Bind(wx.EVT_RADIOBUTTON, self.OnRbCreateRadiobutton)

        self.lstSource = wx.ListCtrl(id=wx.ID_ANY,
                                     name=u'lstSource', parent=self, pos=wx.Point(16, 80),
                                     size=wx.Size(392, 160), style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.lstSource.InsertColumn(0, 'Organization')
        self.lstSource.InsertColumn(1, 'Description')
        self.lstSource.InsertColumn(2, 'Link')
        self.lstSource.InsertColumn(3, 'Contact Name')
        self.lstSource.InsertColumn(4, 'Phone')
        self.lstSource.InsertColumn(5, 'Email')
        self.lstSource.InsertColumn(6, 'Address')
        self.lstSource.InsertColumn(7, 'City')
        self.lstSource.InsertColumn(8, 'State')
        self.lstSource.InsertColumn(9, 'ZipCode')
        self.lstSource.InsertColumn(10, 'Citation')
        self.lstSource.SetColumnWidth(0, 100)
        self.lstSource.SetColumnWidth(1, 100)

        self.lstSource.Bind(wx.EVT_LIST_ITEM_SELECTED,
                            self.OnListCtrl1ListItemSelected)

        self.lstSource.Enable(False)

    def OnRbCurrentRadiobutton(self):
        pass

    def OnRbCreateRadiobutton(self, create):
        pass

    def OnRbSelectRadiobutton(self, e):
        pass

    def OnListCtrl1ListItemSelected(self, e):
        pass