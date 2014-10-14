__author__ = 'Jacob'

import wx
from odmtools.controller.olvSeriesSelector import EVT_OVL_CHECK_EVENT
from odmtools.controller import olvSeriesSelector
from odmtools.odmservices import ServiceManager

[wxID_PNLSERIESSELECTOR, wxID_PNLSERIESSELECTORCBSITES, wxID_PNLSERIESSELECTORCBVARIABLES,
 wxID_PNLSERIESSELECTORCHECKSITE, wxID_PNLSERIESSELECTORCHECKVARIABLE, wxID_PNLSERIESSELECTORLBLSITE,
 wxID_PNLSERIESSELECTORLBLVARIABLE, wxID_PNLSERIESSELECTORtableSeries, wxID_PNLSERIESSELECTORPANEL1,
 wxID_PNLSERIESSELECTORPANEL2, wxID_PNLSIMPLE, wxID_PNLRADIO, wxID_FRAME1RBADVANCED, wxID_FRAME1RBALL,
 wxID_FRAME1RBSIMPLE, wxID_FRAME1SPLITTER, wxID_PNLSPLITTER, wxID_PNLSERIESSELECTORtableSeriesTest, ] = [
    wx.NewId() for _init_ctrls in range(18)]

class ClsSeriesSelector(wx.Panel):
    def __init__(self, parent, id, size, style, name, dbservice, pos=None ):
        self.parent = parent
        wx.Panel.__init__(self, id=wxID_PNLSERIESSELECTOR, name=u'pnlSeriesSelector', parent=parent,
                          size=wx.Size(935, 270), style=wx.TAB_TRAVERSAL)
        self._init_ctrls()
        self.dbservice = dbservice
        self.initTableSeries()
        self.initSVBoxes()
        # Subscribe functions
        self.initPubSub()
        sm = ServiceManager()
        self.export_service = sm.get_export_service()
        self.selectedIndex = 0
        self.isEditing = False
    ## Radio Sizer
    ##    def _init_coll_boxSizer5_Items(self, parent):
    ##        # generated method, don't edit
    ##
    ##        parent.AddWindow(self.rbAll, 0, border=1, flag=wx.ALL)
    ##        parent.AddWindow(self.rbSimple, 0, border=1, flag=wx.ALL)
    ##        parent.AddWindow(self.rbAdvanced, 0, border=1, flag=wx.ALL)


    ## Splitter Sizer
    def _init_coll_boxSizer3_Items(self, parent):
        # generated method, don't edit
        parent.AddWindow(self.cpnlSimple, 0, flag=wx.RIGHT | wx.LEFT | wx.EXPAND)
        parent.AddWindow(self.tblSeries, 100, flag=wx.EXPAND)

    ## Panel Sizer
    def _init_coll_boxSizer1_Items(self, parent):
        # generated method, don't edit
        parent.AddSizer(self.pnlRadio, 0, border=7, flag=wx.LEFT | wx.RIGHT | wx.TOP)
        parent.AddWindow(self.pnlData, 100, border=3, flag=wx.LEFT | wx.RIGHT | wx.EXPAND)

    ## Site Sizer
    def _init_coll_boxSizer4_Items(self, parent):
        # generated method, don't edit
        parent.AddWindow(self.checkSite, 0, border=3, flag=wx.LEFT | wx.RIGHT)
        parent.AddWindow(self.lblSite, 0, border=3, flag=wx.LEFT | wx.RIGHT)
        parent.AddWindow(self.cbSites, 90, border=3, flag=wx.LEFT | wx.RIGHT | wx.EXPAND)

    ## Variable Sizer
    def _init_coll_boxSizer2_Items(self, parent):
        # generated method, don't edit
        parent.AddWindow(self.checkVariable, 0, border=3, flag=wx.LEFT | wx.RIGHT)
        parent.AddWindow(self.lblVariable, 0, border=3, flag=wx.LEFT | wx.RIGHT)
        parent.AddWindow(self.cbVariables, 90, border=3, flag=wx.LEFT | wx.RIGHT | wx.EXPAND)

    ##  Simple Filter Sizer
    def _init_coll_boxSizer6_Items(self, parent):
        parent.AddWindow(self.pnlSite, 50, flag=wx.EXPAND)
        parent.AddWindow(self.pnlVar, 50, flag=wx.EXPAND)
        # parent.AddSizer(self.boxSizer4, 0, border=5, flag=wx.EXPAND)
        # parent.AddSizer(self.boxSizer2, 0, border=5, flag=wx.EXPAND)


    def _init_sizers(self):
        # generated method, don't edit
        self.boxSizer1 = wx.BoxSizer(orient=wx.VERTICAL)
        self.boxSizer2 = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.boxSizer3 = wx.BoxSizer(orient=wx.VERTICAL)
        self.boxSizer4 = wx.BoxSizer(orient=wx.HORIZONTAL)
        ##        self.boxSizer5 = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.boxSizer6 = wx.BoxSizer(orient=wx.VERTICAL)

        self._init_coll_boxSizer1_Items(self.boxSizer1)
        self._init_coll_boxSizer2_Items(self.boxSizer2)
        self._init_coll_boxSizer3_Items(self.boxSizer3)
        self._init_coll_boxSizer4_Items(self.boxSizer4)
        ##        self._init_coll_boxSizer5_Items(self.boxSizer5)
        self._init_coll_boxSizer6_Items(self.boxSizer6)

        self.SetSizer(self.boxSizer1)
        ##        self.pnlRadio.SetSizer(self.boxSizer5)
        ##        self.pnlSite.SetSizer(self.boxSizer4)
        ##        self.pnlVar.SetSizer(self.boxSizer2)
        self.cpnlSimple.SetSizer(self.boxSizer6)
        self.pnlData.SetSizer(self.boxSizer3)
        # self.pnlRadio.SetSizer(self.boxSizer5)

    def _init_ctrls(self):
        # generated method, don't edit


        self.SetClientSize(wx.Size(919, 232))
        self.Enable(True)

        ## Radio panel
        self.pnlRadio = wx.Panel(id=wxID_PNLRADIO, name='pnlRadio', parent=self, pos=wx.Point(3, 3),
                                 size=wx.Size(919, 20), style=wx.TAB_TRAVERSAL)

        self.rbAll = wx.RadioButton(id=wxID_FRAME1RBALL, label=u'All', name=u'rbAll', parent=self.pnlRadio,
                                    pos=wx.Point(0, 0), size=wx.Size(81, 20), style=0)

        self.rbSimple = wx.RadioButton(id=wxID_FRAME1RBSIMPLE, label=u'Simple Filter', name=u'rbSimple',
                                       parent=self.pnlRadio, pos=wx.Point(81, 0), size=wx.Size(112, 20), style=0)

        self.rbAdvanced = wx.RadioButton(id=wxID_FRAME1RBADVANCED, label=u'Advanced Filter', name=u'rbAdvanced',
                                         parent=self.pnlRadio, pos=wx.Point(193, 0), size=wx.Size(104, 20), style=0)

        self.rbAll.SetValue(True)

        self.rbAdvanced.Enable(False)

        ## Splitter panel
        self.pnlData = wx.Panel(id=wxID_PNLSPLITTER, name='pnlData', parent=self, pos=wx.Point(0, -10),
                                size=wx.Size(900, 349), style=wx.TAB_TRAVERSAL)

        self.cpnlSimple = wx.CollapsiblePane(self.pnlData, label="", style=wx.CP_DEFAULT_STYLE | wx.CP_NO_TLW_RESIZE)

        ## Site Panel
        self.pnlSite = wx.Panel(id=wxID_PNLSERIESSELECTORPANEL1, name='pnlSite', parent=self.cpnlSimple.GetPane(),
                                pos=wx.Point(3, 0), size=wx.Size(800, 25), style=wx.TAB_TRAVERSAL)

        self.cbSites = wx.ComboBox(choices=[], id=wxID_PNLSERIESSELECTORCBSITES, name=u'cbSites', parent=self.pnlSite,
                                   pos=wx.Point(100, 0), size=wx.Size(700, 23), style=wx.CB_READONLY, value=u'')

        self.checkSite = wx.CheckBox(id=wxID_PNLSERIESSELECTORCHECKSITE, label=u'', name=u'checkSite',
                                     parent=self.pnlSite, pos=wx.Point(3, 0), size=wx.Size(21, 21), style=0)

        self.lblSite = wx.StaticText(id=wxID_PNLSERIESSELECTORLBLSITE, label=u'Site', name=u'lblSite',
                                     parent=self.pnlSite, pos=wx.Point(30, 0), size=wx.Size(60, 21), style=0)
        self.lblSite.SetToolTipString(u'staticText1')

        self.cbSites.SetLabel(u'')
        #self.checkSite.SetValue(False)

        ### Variable Panel
        self.pnlVar = wx.Panel(id=wxID_PNLSERIESSELECTORPANEL2, name='pnlVar', parent=self.cpnlSimple.GetPane(),
                               pos=wx.Point(3, 26), size=wx.Size(800, 25), style=wx.TAB_TRAVERSAL)

        self.lblVariable = wx.StaticText(id=wxID_PNLSERIESSELECTORLBLVARIABLE, label=u'Variable', name=u'lblVariable',
                                         parent=self.pnlVar, pos=wx.Point(30, 0), size=wx.Size(60, 21), style=0)

        self.checkVariable = wx.CheckBox(id=wxID_PNLSERIESSELECTORCHECKVARIABLE, label=u'', name=u'checkVariable',
                                         parent=self.pnlVar, pos=wx.Point(3, 0), size=wx.Size(21, 21), style=0)

        self.cbVariables = wx.ComboBox(choices=[], id=wxID_PNLSERIESSELECTORCBVARIABLES, name=u'cbVariables',
                                       parent=self.pnlVar, pos=wx.Point(100, 0), size=wx.Size(700, 25), style=wx.CB_READONLY,
                                       value='comboBox4')
        self.cbVariables.SetLabel(u'')
        self.cbVariables.Enable(False)

        #wx.EVT_RADIOBUTTON(self, self.rbAll.Id, self.onRbAllRadiobutton)
        self.rbAll.Bind(wx.EVT_RADIOBUTTON, self.onRbAllRadiobutton, id=wxID_FRAME1RBALL)
        self.rbSimple.Bind(wx.EVT_RADIOBUTTON, self.onRbSimpleRadiobutton, id=wxID_FRAME1RBSIMPLE)
        self.rbAdvanced.Bind(wx.EVT_RADIOBUTTON, self.onRbAdvancedRadiobutton, id=wxID_FRAME1RBADVANCED)

        self.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.onPaneChanged, self.cpnlSimple)
        self.checkSite.Bind(wx.EVT_CHECKBOX, self.onCheck, id=wxID_PNLSERIESSELECTORCHECKSITE)
        self.checkVariable.Bind(wx.EVT_CHECKBOX, self.onCheck, id=wxID_PNLSERIESSELECTORCHECKVARIABLE)
        self.cbSites.Bind(wx.EVT_COMBOBOX, self.onCbSitesCombobox, id=wxID_PNLSERIESSELECTORCBSITES)
        self.cbVariables.Bind(wx.EVT_COMBOBOX, self.onCbVariablesCombobox, id=wxID_PNLSERIESSELECTORCBVARIABLES)


        ### New Stuff ##################################################################################################

        self.tblSeries = olvSeriesSelector.clsSeriesTable(id=wxID_PNLSERIESSELECTORtableSeries, parent=self.pnlData,
                                               name=u'tblSeries', size=wx.Size(950, 108), pos=wx.Point(5, 5),
                                               style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_VIRTUAL)

        self.tblSeries.SetEmptyListMsg("No Database Loaded")

        #self.tblSeries.rowFormatter = self._rowFormatter
        self.tblSeries.Bind(EVT_OVL_CHECK_EVENT, self.onReadyToPlot)
        self.tblSeries.Bind(wx.EVT_LIST_ITEM_FOCUSED, self.getSelectedObject)
        self.tblSeries.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnTableRightDown,
                                   id=wxID_PNLSERIESSELECTORtableSeries)
        self.tblSeries.handleStandardKeys = True
        self.tblSeries.useAlternateBackColors = True
        #self.tblSeries.oddRowsBackColor = wx.Colour(143, 188, 188)
        self.tblSeries.oddRowsBackColor = wx.Colour(191, 217, 217)
        self.cpnlSimple.Collapse(True)
        self._init_sizers()

    ## Virtual Event Handlers
    def onReadyToPlot(self, event):
        event.Skip()

    def onReadyToEdit(self, event):
        event.Skip()

    def stopEdit(self):
        pass

    def getSelectedObject(self, event):
        event.Skip()

    def resetDB(self, dbservice):
        pass

    def initTableSeries(self):
        pass

    def refreshTableSeries(self, db):
        pass

    def refreshSeries(self):
        pass

    def initSVBoxes(self):
        pass

    def initPubSub(self):
        pass

    def OnTableRightDown(self, event):
        event.Skip()

    def onPaneChanged(self, event=None):
        pass

    def onRbAdvancedRadiobutton(self, event):
        event.Skip()

    def onRbAllRadiobutton(self, event):
        event.Skip()

    def onRbSimpleRadiobutton(self, event):
        event.Skip()

    def onRightPlot(self, event):
        event.Skip()

    def onRightEdit(self, event):
        event.Skip()

    def onRightRefresh(self, event):
        event.Skip()

    def onRightClearSelected(self, event):
        event.Skip()

    def onRightExData(self, event):
        event.Skip()

    def onRightExMeta(self, event):
        event.Skip()

    def onCbSitesCombobox(self, event):
        event.Skip()

    def onCbVariablesCombobox(self, event):
        event.Skip()

    def siteAndVariables(self):
        pass

    def siteOnly(self):
        pass

    def variableOnly(self):
        pass

    def onCheck(self, event):
        event.Skip()

    def setFilter(self, site_code='', var_code='', advfilter=''):
        pass

    def isEditing(self):
        return self.isEditing


    def _rowFormatter(self, listItem, object):
        pass