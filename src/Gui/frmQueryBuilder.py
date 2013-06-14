#Boa:Frame:frmQueryBuilder

import wx
import wx.richtext

def create(parent):
    return frmQueryBuilder(parent)

[wxID_FRMQUERYBUILDER, wxID_FRMQUERYBUILDERBTNALL, wxID_FRMQUERYBUILDERBTNAND, 
 wxID_FRMQUERYBUILDERBTNAPPLY, wxID_FRMQUERYBUILDERBTNCANCEL, 
 wxID_FRMQUERYBUILDERBTNCLEAR, wxID_FRMQUERYBUILDERBTNEQUAL, 
 wxID_FRMQUERYBUILDERBTNGETUNIQUE, wxID_FRMQUERYBUILDERBTNGREATTHAN, 
 wxID_FRMQUERYBUILDERBTNGTEQUAL, wxID_FRMQUERYBUILDERBTNISNOTNULL, 
 wxID_FRMQUERYBUILDERBTNISNULL, wxID_FRMQUERYBUILDERBTNLESSTHAN, 
 wxID_FRMQUERYBUILDERBTNLIKE, wxID_FRMQUERYBUILDERBTNLTEQUAL, 
 wxID_FRMQUERYBUILDERBTNNOT, wxID_FRMQUERYBUILDERBTNNOTEQUAL, 
 wxID_FRMQUERYBUILDERBTNOR, wxID_FRMQUERYBUILDERBTNPAREN, 
 wxID_FRMQUERYBUILDERLBLCOLUMNS, wxID_FRMQUERYBUILDERLBLMAXIMUM, 
 wxID_FRMQUERYBUILDERLBLMINIMUM, wxID_FRMQUERYBUILDERLBLQUERY, 
 wxID_FRMQUERYBUILDERLBLVALUES, wxID_FRMQUERYBUILDERLISTCOLUMNS, 
 wxID_FRMQUERYBUILDERLISTUNIQEVALUES, wxID_FRMQUERYBUILDERPANEL1, 
 wxID_FRMQUERYBUILDERTBQUERY, wxID_FRMQUERYBUILDERTXTMAX, 
 wxID_FRMQUERYBUILDERTXTMIN, 
] = [wx.NewId() for _init_ctrls in range(30)]

class frmQueryBuilder(wx.Dialog):
    def _init_ctrls(self, prnt, filter= None):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_FRMQUERYBUILDER,
              name=u'frmQueryBuilder', parent=prnt, pos=wx.Point(547, 281),
              size=wx.Size(379, 469), style=wx.DEFAULT_DIALOG_STYLE,
              title=u'Advanced Query')
        self.SetClientSize(wx.Size(363, 431))
        self.SetMaxSize(wx.Size(379, 469))
        self.SetMinSize(wx.Size(379, 469))

        self.panel1 = wx.Panel(id=wxID_FRMQUERYBUILDERPANEL1, name='panel1',
              parent=self, pos=wx.Point(0, 0), size=wx.Size(363, 431),
              style=wx.TAB_TRAVERSAL)

        self.listColumns = wx.ListBox(choices=["SeriesID", "SiteID",
              "VariableID", "MethodID", "SourceID", "QualityControlLevelID",
              "SiteName", "SiteCode", "Latitude", "Longitude", "VariableName",
              "VariableCode", "DataType", "Value Type", "Speciation",
              "SampleMedium", "TimeSupport", "GeneralCategory", "NoDataValue",
              "VarialbeUnitsName", "TimeUnitsName", "MethodDescription",
              "SourceDescription", "Organization", "Citation",
              "QualityControlLevelCode", "QualityControlLevelDefinition",
              "BeginDateTime", "EndDateTime", "BeginDateTimeUTC",
              "EndDateTimeUTC", "ValueCount", "Checked"],
              id=wxID_FRMQUERYBUILDERLISTCOLUMNS, name=u'listColumns',
              parent=self.panel1, pos=wx.Point(16, 24), size=wx.Size(152, 152),
              style=0)
        self.listColumns.Bind(wx.EVT_LISTBOX_DCLICK,
              self.OnListColumnsListboxDclick,
              id=wxID_FRMQUERYBUILDERLISTCOLUMNS)
        self.listColumns.Bind(wx.EVT_LISTBOX, self.OnListColumnsListbox,
              id=wxID_FRMQUERYBUILDERLISTCOLUMNS)

        self.tbQuery = wx.richtext.RichTextCtrl(id=wxID_FRMQUERYBUILDERTBQUERY,
              parent=self.panel1, pos=wx.Point(16, 264), size=wx.Size(328, 128),
              style=wx.richtext.RE_MULTILINE, value=u'')
        self.tbQuery.SetLabel(u'')
        self.tbQuery.SetName(u'tbQuery')
        self.tbQuery.SetValue(str(filter))

        self.listUniqeValues = wx.ListBox(choices=[],
              id=wxID_FRMQUERYBUILDERLISTUNIQEVALUES, name=u'listUniqeValues',
              parent=self.panel1, pos=wx.Point(216, 24), size=wx.Size(132, 152),
              style=0)

        self.txtMin = wx.TextCtrl(id=wxID_FRMQUERYBUILDERTXTMIN, name=u'txtMin',
              parent=self.panel1, pos=wx.Point(256, 216), size=wx.Size(80, 21),
              style=0, value='')

        self.txtMax = wx.TextCtrl(id=wxID_FRMQUERYBUILDERTXTMAX, name=u'txtMax',
              parent=self.panel1, pos=wx.Point(256, 240), size=wx.Size(84, 21),
              style=0, value='')

        self.lblColumns = wx.StaticText(id=wxID_FRMQUERYBUILDERLBLCOLUMNS,
              label=u'Column Names:', name=u'lblColumns', parent=self.panel1,
              pos=wx.Point(16, 8), size=wx.Size(75, 13), style=0)

        self.lblValues = wx.StaticText(id=wxID_FRMQUERYBUILDERLBLVALUES,
              label=u'Unique Values', name=u'lblValues', parent=self.panel1,
              pos=wx.Point(216, 8), size=wx.Size(68, 13), style=0)

        self.lblQuery = wx.StaticText(id=wxID_FRMQUERYBUILDERLBLQUERY,
              label=u'SELECT * FROM [Attributes] WHERE', name=u'lblQuery',
              parent=self.panel1, pos=wx.Point(16, 248), size=wx.Size(176, 13),
              style=0)

        self.lblMinimum = wx.StaticText(id=wxID_FRMQUERYBUILDERLBLMINIMUM,
              label=u'Minimum', name=u'lblMinimum', parent=self.panel1,
              pos=wx.Point(208, 213), size=wx.Size(41, 11), style=0)

        self.lblMaximum = wx.StaticText(id=wxID_FRMQUERYBUILDERLBLMAXIMUM,
              label=u'Maximum', name=u'lblMaximum', parent=self.panel1,
              pos=wx.Point(208, 240), size=wx.Size(45, 13), style=0)

        self.btnIsNull = wx.Button(id=wxID_FRMQUERYBUILDERBTNISNULL,
              label=u'Is Null', name=u'btnIsNull', parent=self.panel1,
              pos=wx.Point(16, 184), size=wx.Size(40, 23), style=0)
        self.btnIsNull.Bind(wx.EVT_BUTTON, self.OnBtnIsNullButton,
              id=wxID_FRMQUERYBUILDERBTNISNULL)

        self.btnApply = wx.Button(id=wxID_FRMQUERYBUILDERBTNAPPLY,
              label=u'Apply', name=u'btnApply', parent=self.panel1,
              pos=wx.Point(200, 400), size=wx.Size(75, 23), style=0)
        self.btnApply.Bind(wx.EVT_BUTTON, self.OnBtnApplyButton,
              id=wxID_FRMQUERYBUILDERBTNAPPLY)

        self.btnNot = wx.Button(id=wxID_FRMQUERYBUILDERBTNNOT, label=u'Not',
              name=u'btnNot', parent=self.panel1, pos=wx.Point(160, 216),
              size=wx.Size(40, 23), style=0)
        self.btnNot.Bind(wx.EVT_BUTTON, self.OnBtnNotButton,
              id=wxID_FRMQUERYBUILDERBTNNOT)

        self.btnOr = wx.Button(id=wxID_FRMQUERYBUILDERBTNOR, label=u'OR',
              name=u'btnOr', parent=self.panel1, pos=wx.Point(120, 216),
              size=wx.Size(32, 23), style=0)
        self.btnOr.Bind(wx.EVT_BUTTON, self.OnBtnOrButton,
              id=wxID_FRMQUERYBUILDERBTNOR)

        self.btnAnd = wx.Button(id=wxID_FRMQUERYBUILDERBTNAND, label=u'AND',
              name=u'btnAnd', parent=self.panel1, pos=wx.Point(72, 216),
              size=wx.Size(40, 23), style=0)
        self.btnAnd.Bind(wx.EVT_BUTTON, self.OnBtnAndButton,
              id=wxID_FRMQUERYBUILDERBTNAND)

        self.btnAll = wx.Button(id=wxID_FRMQUERYBUILDERBTNALL, label=u'*',
              name=u'btnAll', parent=self.panel1, pos=wx.Point(216, 184),
              size=wx.Size(32, 23), style=0)
        self.btnAll.Bind(wx.EVT_BUTTON, self.OnBtnAllButton,
              id=wxID_FRMQUERYBUILDERBTNALL)

        self.btnEqual = wx.Button(id=wxID_FRMQUERYBUILDERBTNEQUAL, label=u'=',
              name=u'btnEqual', parent=self.panel1, pos=wx.Point(176, 24),
              size=wx.Size(32, 23), style=0)
        self.btnEqual.Bind(wx.EVT_BUTTON, self.OnBtnEqualButton,
              id=wxID_FRMQUERYBUILDERBTNEQUAL)

        self.btnParen = wx.Button(id=wxID_FRMQUERYBUILDERBTNPAREN, label=u'( )',
              name=u'btnParen', parent=self.panel1, pos=wx.Point(136, 184),
              size=wx.Size(32, 24), style=0)
        self.btnParen.Bind(wx.EVT_BUTTON, self.OnBtnParenButton,
              id=wxID_FRMQUERYBUILDERBTNPAREN)

        self.btnLike = wx.Button(id=wxID_FRMQUERYBUILDERBTNLIKE, label=u'Like',
              name=u'btnLike', parent=self.panel1, pos=wx.Point(16, 216),
              size=wx.Size(48, 23), style=0)
        self.btnLike.Bind(wx.EVT_BUTTON, self.OnBtnLikeButton,
              id=wxID_FRMQUERYBUILDERBTNLIKE)

        self.btnGTEqual = wx.Button(id=wxID_FRMQUERYBUILDERBTNGTEQUAL,
              label=u'>=', name=u'btnGTEqual', parent=self.panel1,
              pos=wx.Point(176, 152), size=wx.Size(32, 23), style=0)
        self.btnGTEqual.Bind(wx.EVT_BUTTON, self.OnBtnGTEqualButton,
              id=wxID_FRMQUERYBUILDERBTNGTEQUAL)

        self.btnLTEqual = wx.Button(id=wxID_FRMQUERYBUILDERBTNLTEQUAL,
              label=u'<=', name=u'btnLTEqual', parent=self.panel1,
              pos=wx.Point(176, 184), size=wx.Size(32, 23), style=0)
        self.btnLTEqual.Bind(wx.EVT_BUTTON, self.OnBtnLTEqualButton,
              id=wxID_FRMQUERYBUILDERBTNLTEQUAL)

        self.btnNotEqual = wx.Button(id=wxID_FRMQUERYBUILDERBTNNOTEQUAL,
              label=u'<>', name=u'btnNotEqual', parent=self.panel1,
              pos=wx.Point(176, 56), size=wx.Size(32, 23), style=0)
        self.btnNotEqual.Bind(wx.EVT_BUTTON, self.OnBtnNotEqualButton,
              id=wxID_FRMQUERYBUILDERBTNNOTEQUAL)

        self.btnLessThan = wx.Button(id=wxID_FRMQUERYBUILDERBTNLESSTHAN,
              label=u'<', name=u'btnLessThan', parent=self.panel1,
              pos=wx.Point(176, 120), size=wx.Size(32, 23), style=0)
        self.btnLessThan.Bind(wx.EVT_BUTTON, self.OnBtnLessThanButton,
              id=wxID_FRMQUERYBUILDERBTNLESSTHAN)

        self.btnGetUnique = wx.Button(id=wxID_FRMQUERYBUILDERBTNGETUNIQUE,
              label=u'Get Unique Values', name=u'btnGetUnique',
              parent=self.panel1, pos=wx.Point(256, 184), size=wx.Size(99, 23),
              style=0)
        self.btnGetUnique.Bind(wx.EVT_BUTTON, self.OnBtnGetUniqueButton,
              id=wxID_FRMQUERYBUILDERBTNGETUNIQUE)

        self.btnGreatThan = wx.Button(id=wxID_FRMQUERYBUILDERBTNGREATTHAN,
              label=u'>', name=u'btnGreatThan', parent=self.panel1,
              pos=wx.Point(176, 88), size=wx.Size(32, 23), style=0)
        self.btnGreatThan.Bind(wx.EVT_BUTTON, self.OnBtnGreatThanButton,
              id=wxID_FRMQUERYBUILDERBTNGREATTHAN)

        self.btnIsNotNull = wx.Button(id=wxID_FRMQUERYBUILDERBTNISNOTNULL,
              label=u'Is Not Null', name=u'btnIsNotNull', parent=self.panel1,
              pos=wx.Point(64, 184), size=wx.Size(64, 24), style=0)
        self.btnIsNotNull.Bind(wx.EVT_BUTTON, self.OnBtnIsNotNullButton,
              id=wxID_FRMQUERYBUILDERBTNISNOTNULL)

        self.btnCancel = wx.Button(id=wxID_FRMQUERYBUILDERBTNCANCEL,
              label=u'Cancel', name=u'btnCancel', parent=self.panel1,
              pos=wx.Point(280, 400), size=wx.Size(75, 23), style=0)
        self.btnCancel.Bind(wx.EVT_BUTTON, self.OnBtnCancelButton,
              id=wxID_FRMQUERYBUILDERBTNCANCEL)

        self.btnClear = wx.Button(id=wxID_FRMQUERYBUILDERBTNCLEAR,
              label=u'Clear Query', name=u'btnClear', parent=self.panel1,
              pos=wx.Point(120, 400), size=wx.Size(75, 23), style=0)
        self.btnClear.Bind(wx.EVT_BUTTON, self.OnBtnClearButton,
              id=wxID_FRMQUERYBUILDERBTNCLEAR)

    def __init__(self, parent, filter = None):
        self._init_ctrls(parent, filter)
        
    

    def OnBtnCancelButton(self, event):
##        return ""
        self.Close()
        self.Destroy()

    def OnBtnApplyButton(self, event):
##        return self.tbQuery.GetValue()
        self.Close()
        self.Destroy()

    def OnBtnClearButton(self, event):
        self.tbQuery.SetValue("")
        event.Skip()

    def OnBtnEqualButton(self, event):
        event.Skip()

    def OnBtnNotEqualButton(self, event):
        event.Skip()

    def OnListColumnsListboxDclick(self, event):
        event.Skip()

    def OnBtnIsNullButton(self, event):
        event.Skip()

    def OnBtnNotButton(self, event):
        event.Skip()

    def OnBtnOrButton(self, event):
        event.Skip()

    def OnBtnAndButton(self, event):
        event.Skip()

    def OnBtnAllButton(self, event):
        event.Skip()

    def OnBtnParenButton(self, event):
        event.Skip()

    def OnBtnLikeButton(self, event):
        event.Skip()

    def OnBtnGTEqualButton(self, event):
        event.Skip()

    def OnBtnLTEqualButton(self, event):
        event.Skip()

    def OnBtnLessThanButton(self, event):
        event.Skip()

    def OnBtnGetUniqueButton(self, event):
        event.Skip()

    def OnBtnGreatThanButton(self, event):
        event.Skip()

    def OnBtnIsNotNullButton(self, event):
        event.Skip()

    def OnListColumnsListbox(self, event):
        event.Skip()


