#Boa:FramePanel:pnlSeriesSelector
import logging
import os

import wx


# import wx.lib.agw.ultimatelistctrl as ULC
# from ObjectListView import ObjectListView, ColumnDefn, Filter

from wx.lib.pubsub import pub as Publisher

# from ObjectListView import Filter
import wx.lib.agw.ultimatelistctrl as ULC
from common.logger import LoggerTool

try:
    from agw import pycollapsiblepane as PCP
except ImportError:  # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.pycollapsiblepane as PCP
from clsULC import clsULC, TextSearch, Chain
import frmQueryBuilder

from odmdata import MemoryDatabase
from odmservices import ServiceManager

tool = LoggerTool()
logger = tool.setupLogger(__name__, __name__ + '.log', 'w', logging.DEBUG)


##########only use this section when testing series selector #############


def create(parent):
    return test_ss(parent)


class test_ss(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, id=2, name=u'test_ss', parent=parent,
                          size=wx.Size(900, 700),
                          style=wx.DEFAULT_FRAME_STYLE, title=u'test_ss')
        id = 1
        size = wx.Size(900, 700)
        pos = (0, 0)
        style = "wx.TAB_TRAVERSAL"
        name = u'pnlSelector'
        service_manager = ServiceManager()
        dbservice = service_manager.get_series_service()
        pnl = pnlSeriesSelector(parent=self, id=id, size=size, style=style, name=name, dbservice=dbservice, pos=pos)

##################################################################

[wxID_PNLSERIESSELECTOR, wxID_PNLSERIESSELECTORCBSITES, wxID_PNLSERIESSELECTORCBVARIABLES,
 wxID_PNLSERIESSELECTORCHECKSITE, wxID_PNLSERIESSELECTORCHECKVARIABLE,
 wxID_PNLSERIESSELECTORLBLSITE, wxID_PNLSERIESSELECTORLBLVARIABLE,
 wxID_PNLSERIESSELECTORtableSeries, wxID_PNLSERIESSELECTORPANEL1,
 wxID_PNLSERIESSELECTORPANEL2, wxID_PNLSIMPLE, wxID_PNLRADIO,
 wxID_FRAME1RBADVANCED, wxID_FRAME1RBALL,
 wxID_FRAME1RBSIMPLE, wxID_FRAME1SPLITTER, wxID_PNLSPLITTER,
] = [wx.NewId() for _init_ctrls in range(17)]


class pnlSeriesSelector(wx.Panel):
    def __init__(self, parent, id, size, style, name, dbservice, pos=None, ):
        self.parent = parent
        self._init_ctrls(parent)

        self.dbservice = dbservice
        self.initTableSeries()
        self.initSVBoxes()

        # Subscribe functions
        self.initPubSub()

        sm = ServiceManager()
        self.export_service = sm.get_export_service()
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
        parent.AddWindow(self.tableSeries, 100, flag=wx.EXPAND)

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

    def _init_ctrls(self, prnt):
        # generated method, don't edit

        wx.Panel.__init__(self, id=wxID_PNLSERIESSELECTOR,
                          name=u'pnlSeriesSelector', parent=prnt,
                          size=wx.Size(935, 270), style=wx.TAB_TRAVERSAL)
        self.SetClientSize(wx.Size(919, 232))
        self.Enable(True)

        ## Radio panel
        self.pnlRadio = wx.Panel(id=wxID_PNLRADIO, name='pnlRadio',
                                 parent=self, pos=wx.Point(3, 3), size=wx.Size(919, 20),
                                 style=wx.TAB_TRAVERSAL)

        self.rbAll = wx.RadioButton(id=wxID_FRAME1RBALL, label=u'All',
                                    name=u'rbAll', parent=self.pnlRadio, pos=wx.Point(0, 0),
                                    size=wx.Size(81, 20), style=0)
        self.rbAll.SetValue(True)
        self.rbAll.Bind(wx.EVT_RADIOBUTTON, self.onRbAllRadiobutton,
                        id=wxID_FRAME1RBALL)

        self.rbSimple = wx.RadioButton(id=wxID_FRAME1RBSIMPLE,
                                       label=u'Simple Filter', name=u'rbSimple', parent=self.pnlRadio,
                                       pos=wx.Point(81, 0), size=wx.Size(112, 20), style=0)
        self.rbSimple.Bind(wx.EVT_RADIOBUTTON, self.onRbSimpleRadiobutton,
                           id=wxID_FRAME1RBSIMPLE)

        self.rbAdvanced = wx.RadioButton(id=wxID_FRAME1RBADVANCED,
                                         label=u'Advanced Filter', name=u'rbAdvanced', parent=self.pnlRadio,
                                         pos=wx.Point(193, 0), size=wx.Size(104, 20), style=0)
        self.rbAdvanced.Bind(wx.EVT_RADIOBUTTON, self.onRbAdvancedRadiobutton,
                             id=wxID_FRAME1RBADVANCED)
        self.rbAdvanced.Enable(False)

        ## Splitter panel
        self.pnlData = wx.Panel(id=wxID_PNLSPLITTER, name='pnlData',
                                parent=self, pos=wx.Point(0, -10), size=wx.Size(900, 349),
                                style=wx.TAB_TRAVERSAL)

        ##        self.splitter = wx.SplitterWindow(id=wxID_FRAME1SPLITTER,
        ##              name=u'splitter', parent=self.pnlData, pos=wx.Point(0, 0),
        ##              size=wx.Size(604, 137), style=wx.NO_BORDER)
        ##        self.splitter.SetMinSize(wx.Size(-1, -1))

        self.cpnlSimple = PCP.PyCollapsiblePane(parent=self.pnlData, label="",
                                                agwStyle=wx.CP_NO_TLW_RESIZE | wx.CP_GTK_EXPANDER | wx.CP_USE_STATICBOX,
                                                size=wx.Size(300, 20), pos=wx.Point(0, -20))
        self.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.onPaneChanged, self.cpnlSimple)

        ## panel for simple filter(top of splitter)
        ##        self.pnlSimple = wx.Panel(id=wxID_PNLSIMPLE, name='panel3',
        ##              parent=self.splitter, pos=wx.Point(0, 0), size=wx.Size(919, 300),
        ##              style=wx.TAB_TRAVERSAL)

        ## Site Panel
        self.pnlSite = wx.Panel(id=wxID_PNLSERIESSELECTORPANEL1, name='pnlSite',
                                parent=self.cpnlSimple.GetPane(), pos=wx.Point(3, 0), size=wx.Size(800, 25),
                                style=wx.TAB_TRAVERSAL)

        self.cbSites = wx.ComboBox(choices=[], id=wxID_PNLSERIESSELECTORCBSITES,
                                   name=u'cbSites', parent=self.pnlSite, pos=wx.Point(100, 0),
                                   size=wx.Size(700, 23), style=0, value=u'')
        self.cbSites.SetLabel(u'')
        self.cbSites.Bind(wx.EVT_COMBOBOX, self.onCbSitesCombobox,
                          id=wxID_PNLSERIESSELECTORCBSITES)

        self.checkSite = wx.CheckBox(id=wxID_PNLSERIESSELECTORCHECKSITE,
                                     label=u'', name=u'checkSite', parent=self.pnlSite, pos=wx.Point(3,
                                                                                                     0),
                                     size=wx.Size(21, 21), style=0)
        self.checkSite.SetValue(True)
        self.checkSite.Bind(wx.EVT_CHECKBOX, self.onCheck,
                            id=wxID_PNLSERIESSELECTORCHECKSITE)

        self.lblSite = wx.StaticText(id=wxID_PNLSERIESSELECTORLBLSITE,
                                     label=u'Site', name=u'lblSite', parent=self.pnlSite,
                                     pos=wx.Point(30, 0), size=wx.Size(60, 21), style=0)
        self.lblSite.SetToolTipString(u'staticText1')

        ### Variable Panel
        self.pnlVar = wx.Panel(id=wxID_PNLSERIESSELECTORPANEL2, name='pnlVar',
                               parent=self.cpnlSimple.GetPane(), pos=wx.Point(3, 26), size=wx.Size(800, 25),
                               style=wx.TAB_TRAVERSAL)

        self.lblVariable = wx.StaticText(id=wxID_PNLSERIESSELECTORLBLVARIABLE,
                                         label=u'Variable', name=u'lblVariable', parent=self.pnlVar,
                                         pos=wx.Point(30, 0), size=wx.Size(60, 21), style=0)

        self.checkVariable = wx.CheckBox(id=wxID_PNLSERIESSELECTORCHECKVARIABLE,
                                         label=u'', name=u'checkVariable', parent=self.pnlVar,
                                         pos=wx.Point(3, 0), size=wx.Size(21, 21), style=0)
        self.checkVariable.Bind(wx.EVT_CHECKBOX, self.onCheck,
                                id=wxID_PNLSERIESSELECTORCHECKVARIABLE)

        self.cbVariables = wx.ComboBox(choices=[],
                                       id=wxID_PNLSERIESSELECTORCBVARIABLES, name=u'cbVariables',
                                       parent=self.pnlVar, pos=wx.Point(100, 0), size=wx.Size(700, 25),
                                       style=0, value='comboBox4')
        self.cbVariables.SetLabel(u'')
        self.cbVariables.Enable(False)
        self.cbVariables.Bind(wx.EVT_COMBOBOX, self.onCbVariablesCombobox,
                              id=wxID_PNLSERIESSELECTORCBVARIABLES)

        self.tableSeries = clsULC(id=wxID_PNLSERIESSELECTORtableSeries,
                                  name=u'tableSeries', parent=self.pnlData, pos=wx.Point(5, 5),
                                  size=wx.Size(903, 108),
                                  agwStyle=ULC.ULC_REPORT | ULC.ULC_HRULES | ULC.ULC_VRULES | ULC.ULC_HAS_VARIABLE_ROW_HEIGHT | ULC.ULC_SINGLE_SEL)
        ##        self.splitter.Initialize(self.tableSeries)
        self.cpnlSimple.Collapse(True)
        # self.splitter.SplitHorizontally(self.pnlSimple, self.tableSeries, 1)

        #   self.tableSeries.Bind(ULC.EVT_LIST_ITEM_SELECTED, self.testBinding)

        self.tableSeries.Bind(ULC.EVT_LIST_ITEM_CHECKED,
                              self.onTableSeriesListItemSelected,
                              id=wxID_PNLSERIESSELECTORtableSeries)

        self.tableSeries.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK,
                              self.OnTableRightDown,
                              id=wxID_PNLSERIESSELECTORtableSeries)

        Publisher.subscribe(self.onEditButton, ("selectEdit"))
        self._init_sizers()

    #def testBinding(self, event):
    #    print "event:", event.m_itemIndex

    def initPubSub(self):
        Publisher.subscribe(self.refreshSeries, "refreshSeries")

    def resetDB(self, dbservice):

        #####INIT DB Connection
        self.dbservice = dbservice
        #self.tableSeries.clear()
        self.cbVariables.Clear()
        self.cbSites.Clear()
        self.siteList = None
        self.varList = None

        self.initTableSeries()
        self.initSVBoxes()

        self.Layout()

    def initTableSeries(self):
        self.memDB = MemoryDatabase(self.dbservice)
        self.tableSeries.setColumns(self.memDB.getSeriesColumns())
        self.tableSeries.setObjects(self.memDB.getSeriesCatalog())
        self.tableSeries.EnableSelectionVista(True)


    def initSVBoxes(self):

        self.site_code = None
        self.variable_code = None

        #####INIT drop down boxes for Simple Filter
        self.siteList = self.dbservice.get_all_sites()
        for site in self.siteList:
            self.cbSites.Append(site.code + '-' + site.name)
        self.cbSites.SetSelection(0)
        self.site_code = self.siteList[0].code

        self.varList = self.dbservice.get_all_variables()
        for var in self.varList:
            self.cbVariables.Append(var.code + '-' + var.name)
        self.cbVariables.SetSelection(0)

    def OnTableRightDown(self, event):

        # build pop-up menu for right-click display
        self.selectedIndex = event.m_itemIndex
        self.selectedID = self.tableSeries.getColumnText(event.m_itemIndex, 1)
        # print self.selectedID
        popup_edit_series = wx.NewId()
        popup_plot_series = wx.NewId()
        popup_export_data = wx.NewId()
        popup_series_refresh = wx.NewId()

        popup_export_metadata = wx.NewId()
        popup_select_all = wx.NewId()
        popup_select_none = wx.NewId()
        popup_menu = wx.Menu()
        self.Bind(wx.EVT_MENU, self.onRightPlot, popup_menu.Append(popup_plot_series, 'Plot'))
        self.Bind(wx.EVT_MENU, self.onRightEdit, popup_menu.Append(popup_edit_series, 'Edit'))
        self.Bind(wx.EVT_MENU, self.onRightRefresh, popup_menu.Append(popup_series_refresh, 'Refresh'))
        popup_menu.AppendSeparator()
        self.Bind(wx.EVT_MENU, self.onRightExData, popup_menu.Append(popup_export_data, 'Export Data'))
        self.Bind(wx.EVT_MENU, self.onRightExMeta, popup_menu.Append(popup_export_metadata, 'Export MetaData'))

        self.tableSeries.PopupMenu(popup_menu)
        event.Skip()


    def onPaneChanged(self, event=None):
        if event:
            print 'wx.EVT_COLLAPSIBLEPANE_CHANGED: %s\n' % event.Collapsed
        self.Layout()

    def onRbAdvancedRadiobutton(self, event):
        #open filter window and hide top Panel
        # self.splitter.SetSashPosition(1)
        ##        if self.splitter.IsSplit():
        ##            self.splitter.Unsplit(self.pnlSimple)
        self.cpnlSimple.Collapse(True)
        self.Layout()
        series_filter = frmQueryBuilder.frmQueryBuilder(self)
        self.filterlist = series_filter.ShowModal()
        # print self.filterlist
        event.Skip()

    def onRbAllRadiobutton(self, event):
        #Hide top panel
        ##        if self.splitter.IsSplit():
        ##            self.splitter.Unsplit(self.pnlSimple)
        self.cpnlSimple.Collapse(True)
        self.Layout()
        # self.splitter.SetSashPosition(1)
        self.setFilter()
        event.Skip()


    def onRbSimpleRadiobutton(self, event):
        #show top Panel
        ##        if not self.splitter.IsSplit():
        ##            self.splitter.SplitHorizontally(self.pnlSimple, self.tableSeries, 30)
        # self.splitter.SetSashPosition(70)
        self.cpnlSimple.Expand()
        self.Layout()
        self.setFilter(self.site_code, self.variable_code)
        event.Skip()


    def onRightPlot(self, event):
        # print self.tableSeries.IsItemChecked(self.selectedIndex)
        # self.tableSeries.GetItem(self.selectedID, 0).Check = True
        ##        self.tableSeries.GetColumnText(self.selectedIndex, 1).Check = True
        self.tableSeries.checkItem(self.selectedIndex)
        self.selectForPlot(self.selectedIndex)
        event.Skip()

    def onRightEdit(self, event):
        self.selectForEdit(self.tableSeries.getColumnText(self.selectedIndex, 1))
        event.Skip()

    # allows user to right-click refresh the Series Selector
    def onRightRefresh(self, event):
        self.refreshSeries()
        event.Skip()

    def refreshSeries(self):
        self.resetDB(self.dbservice)
        logger.debug("Refresh Occurred")

    def onEditButton(self, event):
        #
        if self.tableSeries.GetSelectedItemCount() > 0:
            self.selectForEdit(self.tableSeries.getColumnText(self.tableSeries.getSelection(), 1))
        else:
            #toggle ribbon button to be unpressed
            print "no series selected"


    def onRightExData(self, event):
        dlg = wx.FileDialog(self, "Choose a save location", '', "", "*.csv", wx.SAVE | wx.OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            full_path = os.path.join(dlg.GetDirectory(), dlg.GetFilename())

            series_id = self.tableSeries.getColumnText(self.selectedIndex, 1)
            self.export_service.export_series_data(series_id, full_path, True, True, True, True, True, True, True)
            self.Close()

        dlg.Destroy()

        event.Skip()

    def onRightExMeta(self, event):
        dlg = wx.FileDialog(self, "Choose a save location", '', "", "*.xml", wx.SAVE | wx.OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            full_path = os.path.join(dlg.GetDirectory(), dlg.GetFilename())

            series_id = self.tableSeries.getColumnText(self.selectedIndex, 1)
            self.export_service.export_series_metadata(series_id, full_path)
            self.Close()

        dlg.Destroy()

        event.Skip()


    def onCbSitesCombobox(self, event):
        self.site_code = self.siteList[event.GetSelection()].code
        self.varList = self.dbservice.get_variables_by_site_code(self.site_code)

        self.cbVariables.Clear()
        for var in self.varList:
            self.cbVariables.Append(var.code + '-' + var.name)
        self.cbVariables.SetSelection(0)

        if (self.checkSite.GetValue() and not self.checkVariable.GetValue()):
            self.variable_code = None

        self.setFilter(site_code=self.site_code, var_code=self.variable_code)
        event.Skip()


    def onCbVariablesCombobox(self, event):
        self.variable_code = self.varList[event.GetSelection()].code
        if (not self.checkSite.GetValue() and self.checkVariable.GetValue()):
            self.site_code = None
        self.setFilter(site_code=self.site_code, var_code=self.variable_code)
        event.Skip()


    def siteAndVariables(self):
        self.site_code = self.siteList[self.cbSites.Selection].code

        self.cbVariables.Clear()
        self.varList = self.dbservice.get_variables_by_site_code(self.site_code)
        for var in self.varList:
            self.cbVariables.Append(var.code + '-' + var.name)
        self.cbVariables.SetSelection(0)

        self.variable_code = self.varList[self.cbVariables.Selection].code

        self.setFilter(site_code=self.site_code, var_code=self.variable_code)

        self.cbVariables.Enabled = True
        self.cbSites.Enabled = True

    def siteOnly(self):
        self.cbVariables.Enabled = False
        self.cbSites.Enabled = True
        self.variable_code = None

        self.site_code = self.siteList[self.cbSites.Selection].code
        self.setFilter(site_code=self.site_code)

    def variableOnly(self):
        self.site_code = None
        self.cbVariables.Clear()
        self.varList = self.dbservice.get_all_variables()
        for var in self.varList:
            self.cbVariables.Append(var.code + '-' + var.name)
        self.cbVariables.SetSelection(0)
        self.cbSites.Enabled = False
        self.cbVariables.Enabled = True

        self.variable_code = self.varList[0].code

        self.setFilter(var_code=self.variable_code)

    def onCheck(self, event):
        # self.tableSeries.DeleteAllItems()
        if self.checkSite.GetValue():
            logger.debug("checksite: %s" % (self.checkSite.GetValue()))
            if self.checkVariable.GetValue():
                logger.debug("checkvariable: %s" % (self.checkVariable.GetValue()))
                self.siteAndVariables()
            else:
                logger.debug("siteOnly: %s" % (self.siteOnly()))
                self.siteOnly()
        else:
            if self.checkVariable.GetValue():
                logger.debug("VariableOnly: %s" % (self.variableOnly()))
                self.variableOnly()
            else:
                self.cbSites.Enabled = False
                self.cbVariables.Enabled = False
        event.Skip()

    def setFilter(self, site_code='', var_code='', advfilter=''):
        if (site_code and var_code):
            self.siteFilter = TextSearch(self.tableSeries, columns=self.tableSeries.columns[2:4], text=site_code)
            self.variableFilter = TextSearch(self.tableSeries, columns=self.tableSeries.columns[5:7], text=var_code)
            self.tableSeries.setFilter(Chain(self.siteFilter, self.variableFilter))
        elif (site_code):
            self.tableSeries.setFilter(
                TextSearch(self.tableSeries, columns=self.tableSeries.columns[2:4], text=site_code))
        elif (var_code):
            self.tableSeries.setFilter(
                TextSearch(self.tableSeries, columns=self.tableSeries.columns[5:7], text=var_code))
        elif (advfilter):
            self.tableSeries.setFilter(advfilter)
        else:
            self.tableSeries.clearFilter()

        self.tableSeries.repopulateList()


    def onTableSeriesListItemSelected(self, event):
        self.selectForPlot(event.m_itemIndex)

        isActive = False
        if len(self.tableSeries.getChecked()) > 0:
            isActive = True

        Publisher.sendMessage("EnablePlotButtons", plot=0, isActive=isActive)
        event.Skip()

    def selectForPlot(self, selIndex):
        sid = self.tableSeries.innerList[selIndex][0]
        if not self.tableSeries.IsItemChecked(selIndex):
            Publisher.sendMessage("removePlot", seriesID=sid)
            self.tableSeries.innerList[selIndex][-1] = False

        else:
            #set isselected value to True
            self.tableSeries.innerList[selIndex][-1] = True
            self.parent.Parent.addPlot(self.memDB, sid)

        self.Refresh()

    def selectForEdit(self, seriesID):
        self.memDB.initEditValues(seriesID)
        self.parent.Parent.addEdit(seriesID, self.memDB)


    def stopEdit(self):
        self.memDB.stopEdit()


##########only use this section when testing series selector #############
if __name__ == '__main__':
    app = wx.App(False)
    frame = create(None)
    frame.Show()

    app.MainLoop()
##################################################################
