import logging
import os

import wx


from wx.lib.pubsub import pub as Publisher
from ObjectListView import ColumnDefn
from ObjectListView.Filter import TextSearch, Chain

import frmQueryBuilder

#from clsSeriesTable import clsSeriesTable, TextSearch, Chain, EVT_OVL_CHECK_EVENT
from odmtools.controller.odmObjectListView import EVT_OVL_CHECK_EVENT

from odmtools.common.logger import LoggerTool
from odmtools.controller import odmObjectListView
from odmtools.odmdata import MemoryDatabase, series
from odmtools.odmservices import ServiceManager


tool = LoggerTool()
logger = tool.setupLogger(__name__, __name__ + '.log', 'w', logging.DEBUG)


##########only use this section when testing series selector #############


def create(parent):
    return test_ss(parent)


class test_ss(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, id=2, name=u'test_ss', parent=parent, size=wx.Size(900, 700),
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
 wxID_PNLSERIESSELECTORCHECKSITE, wxID_PNLSERIESSELECTORCHECKVARIABLE, wxID_PNLSERIESSELECTORLBLSITE,
 wxID_PNLSERIESSELECTORLBLVARIABLE, wxID_PNLSERIESSELECTORtableSeries, wxID_PNLSERIESSELECTORPANEL1,
 wxID_PNLSERIESSELECTORPANEL2, wxID_PNLSIMPLE, wxID_PNLRADIO, wxID_FRAME1RBADVANCED, wxID_FRAME1RBALL,
 wxID_FRAME1RBSIMPLE, wxID_FRAME1SPLITTER, wxID_PNLSPLITTER, wxID_PNLSERIESSELECTORtableSeriesTest, ] = [
    wx.NewId() for _init_ctrls in range(18)]


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

    def _init_ctrls(self, prnt):
        # generated method, don't edit

        wx.Panel.__init__(self, id=wxID_PNLSERIESSELECTOR, name=u'pnlSeriesSelector', parent=prnt,
                          size=wx.Size(935, 270), style=wx.TAB_TRAVERSAL)
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
        #self.rbAll.Bind(wx.EVT_RADIOBUTTON, self.onRbAllRadiobutton, id=wxID_FRAME1RBALL)
        wx.EVT_RADIOBUTTON(self, self.rbAll.Id, self.onRbAllRadiobutton)
        self.rbSimple.Bind(wx.EVT_RADIOBUTTON, self.onRbSimpleRadiobutton, id=wxID_FRAME1RBSIMPLE)
        self.rbAdvanced.Bind(wx.EVT_RADIOBUTTON, self.onRbAdvancedRadiobutton, id=wxID_FRAME1RBADVANCED)
        self.rbAdvanced.Enable(False)

        ## Splitter panel
        self.pnlData = wx.Panel(id=wxID_PNLSPLITTER, name='pnlData', parent=self, pos=wx.Point(0, -10),
                                size=wx.Size(900, 349), style=wx.TAB_TRAVERSAL)

        self.cpnlSimple = wx.CollapsiblePane(self.pnlData, label="", style=wx.CP_DEFAULT_STYLE | wx.CP_NO_TLW_RESIZE)
        self.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.onPaneChanged, self.cpnlSimple)

        ## Site Panel
        self.pnlSite = wx.Panel(id=wxID_PNLSERIESSELECTORPANEL1, name='pnlSite', parent=self.cpnlSimple.GetPane(),
                                pos=wx.Point(3, 0), size=wx.Size(800, 25), style=wx.TAB_TRAVERSAL)

        self.cbSites = wx.ComboBox(choices=[], id=wxID_PNLSERIESSELECTORCBSITES, name=u'cbSites', parent=self.pnlSite,
                                   pos=wx.Point(100, 0), size=wx.Size(700, 23), style=0, value=u'')

        self.checkSite = wx.CheckBox(id=wxID_PNLSERIESSELECTORCHECKSITE, label=u'', name=u'checkSite',
                                     parent=self.pnlSite, pos=wx.Point(3, 0), size=wx.Size(21, 21), style=0)

        self.lblSite = wx.StaticText(id=wxID_PNLSERIESSELECTORLBLSITE, label=u'Site', name=u'lblSite',
                                     parent=self.pnlSite, pos=wx.Point(30, 0), size=wx.Size(60, 21), style=0)
        self.lblSite.SetToolTipString(u'staticText1')

        self.cbSites.SetLabel(u'')
        self.cbSites.Bind(wx.EVT_COMBOBOX, self.onCbSitesCombobox, id=wxID_PNLSERIESSELECTORCBSITES)
        self.checkSite.SetValue(True)
        self.checkSite.Bind(wx.EVT_CHECKBOX, self.onCheck, id=wxID_PNLSERIESSELECTORCHECKSITE)

        ### Variable Panel
        self.pnlVar = wx.Panel(id=wxID_PNLSERIESSELECTORPANEL2, name='pnlVar', parent=self.cpnlSimple.GetPane(),
                               pos=wx.Point(3, 26), size=wx.Size(800, 25), style=wx.TAB_TRAVERSAL)

        self.lblVariable = wx.StaticText(id=wxID_PNLSERIESSELECTORLBLVARIABLE, label=u'Variable', name=u'lblVariable',
                                         parent=self.pnlVar, pos=wx.Point(30, 0), size=wx.Size(60, 21), style=0)

        self.checkVariable = wx.CheckBox(id=wxID_PNLSERIESSELECTORCHECKVARIABLE, label=u'', name=u'checkVariable',
                                         parent=self.pnlVar, pos=wx.Point(3, 0), size=wx.Size(21, 21), style=0)
        self.checkVariable.Bind(wx.EVT_CHECKBOX, self.onCheck, id=wxID_PNLSERIESSELECTORCHECKVARIABLE)

        self.cbVariables = wx.ComboBox(choices=[], id=wxID_PNLSERIESSELECTORCBVARIABLES, name=u'cbVariables',
                                       parent=self.pnlVar, pos=wx.Point(100, 0), size=wx.Size(700, 25), style=0,
                                       value='comboBox4')
        self.cbVariables.SetLabel(u'')
        self.cbVariables.Enable(False)
        self.cbVariables.Bind(wx.EVT_COMBOBOX, self.onCbVariablesCombobox, id=wxID_PNLSERIESSELECTORCBVARIABLES)


        ### New Stuff ##################################################################################################

        self.tblSeries = odmObjectListView.clsSeriesTable(id=wxID_PNLSERIESSELECTORtableSeries, parent=self.pnlData,

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

    def initPubSub(self):
        #Publisher.subscribe(self.onEditButton, ("selectEdit"))
        Publisher.subscribe(self.refreshSeries, "refreshSeries")

    def resetDB(self, dbservice):

        if not self.rbAll.GetValue():
            wx.PostEvent(self.GetEventHandler(), wx.PyCommandEvent(wx.EVT_RADIOBUTTON.typeId, self.rbAll.Id))
            self.rbAll.SetValue(True)

        #####INIT DB Connection
        #with Timer() as t:
        self.dbservice = dbservice
        #logger.debug("self.dbservice = dbservice: %d" % t.interval)

        #with Timer() as t:
        #self.tableSeries.clear()
        self.cbVariables.Clear()
        self.cbSites.Clear()
        #logger.debug("clear cbVariables & cbSites: %d" % t.interval)

        self.siteList = None
        self.varList = None

        #with Timer() as t:
        self.initTableSeries()
        #logger.debug("self.initTableSeries(): %d" % t.interval)

        #with Timer() as t:
        self.initSVBoxes()
        #logger.debug("self.initSVBoxes(): %d" % t.interval)

        #with Timer() as t:
        self.Layout()
        #logger.debug("self.Layout(): %d" % t.interval)

    def initTableSeries(self):
        """Set up columns and objects to be used in the objectlistview to be visible in the series selector"""

        self.memDB = MemoryDatabase(self.dbservice)
        seriesColumns = [ColumnDefn(key, align="left", minimumWidth=-1, valueGetter=value)
                         for key, value in series.returnDict().iteritems()]
        self.tblSeries.SetColumns(seriesColumns)
        self.tblSeries.CreateCheckStateColumn()
        object = self.dbservice.get_all_series()
        self.tblSeries.SetObjects(object)
        #self.tblSeries.SaveObject(object)


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
        """
        Right click down menu
        """
        # build pop-up menu for right-click display
        self.selectedIndex = event.m_itemIndex
        #self.selectedID = self.tableSeries.getColumnText(event.m_itemIndex, 1)
        self.selectedID = self.tblSeries.GetSelectedObject().id

        # print self.selectedID
        popup_edit_series = wx.NewId()
        popup_plot_series = wx.NewId()
        popup_export_data = wx.NewId()
        popup_series_refresh = wx.NewId()
        popup_clear_selected = wx.NewId()

        popup_export_metadata = wx.NewId()
        popup_select_all = wx.NewId()
        popup_select_none = wx.NewId()
        popup_menu = wx.Menu()
        self.Bind(wx.EVT_MENU, self.onRightPlot, popup_menu.Append(popup_plot_series, 'Plot'))
        self.Bind(wx.EVT_MENU, self.onRightEdit, popup_menu.Append(popup_edit_series, 'Edit'))
        # TODO @jmeline will refresh and clear selected as an enhancement
        #self.Bind(wx.EVT_MENU, self.onRightRefresh, popup_menu.Append(popup_series_refresh, 'Refresh'))
        #self.Bind(wx.EVT_MENU, self.onRightClearSelected, popup_menu.Append(popup_series_refresh, 'Clear Selected'))

        popup_menu.AppendSeparator()
        self.Bind(wx.EVT_MENU, self.onRightExData, popup_menu.Append(popup_export_data, 'Export Data'))
        self.Bind(wx.EVT_MENU, self.onRightExMeta, popup_menu.Append(popup_export_metadata, 'Export MetaData'))

        self.tblSeries.PopupMenu(popup_menu)
        event.Skip()

    def onPaneChanged(self, event=None):
        #if event:
        #    print 'wx.EVT_COLLAPSIBLEPANE_CHANGED: %s\n' % event.Collapsed
        self.Layout()

    def onRbAdvancedRadiobutton(self, event):

        self.cpnlSimple.Collapse(True)
        self.Layout()
        series_filter = frmQueryBuilder.frmQueryBuilder(self)
        self.filterlist = series_filter.ShowModal()
        # print self.filterlist
        event.Skip()

    def onRbAllRadiobutton(self, event):

        logger.debug("onRbAllRadioButton called! ")
        self.cpnlSimple.Collapse(True)
        self.Layout()
        self.setFilter()
        event.Skip()

    def onRbSimpleRadiobutton(self, event):

        self.cpnlSimple.Expand()
        self.Layout()
        self.setFilter(self.site_code, self.variable_code)

        event.Skip()

    def onRightPlot(self, event):
        object = self.tblSeries.GetSelectedObject()
        self.tblSeries.ToggleCheck(object)
        self.onReadyToPlot(event)
        event.Skip()

    def onRightEdit(self, event):
        Publisher.sendMessage(("selectEdit"), event=event)
        if self.isEditing:
            Publisher.sendMessage("toggleEdit", checked=True)
        event.Skip()

    # allows user to right-click refresh the Series Selector
    def onRightRefresh(self, event):
        self.refreshSeries()
        event.Skip()

    def onRightClearSelected(self, event):
        #self.
        event.Skip()

    def refreshSeries(self):
        self.dbservice = None
        self.dbservice = self.parent.Parent.createService()
        self.resetDB(self.dbservice)
        logger.debug("Refresh Occurred")

    def onRightExData(self, event):
        dlg = wx.FileDialog(self, "Choose a save location", '', "", "*.csv", wx.SAVE | wx.OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            full_path = os.path.join(dlg.GetDirectory(), dlg.GetFilename())

            #series_id = self.tableSeries.getColumnText(self.selectedIndex, 1)
            series_id = self.tblSeries.GetSelectedObject().id
            self.export_service.export_series_data(series_id, full_path, True, True, True, True, True, True, True)
            self.Close()

        dlg.Destroy()

        event.Skip()

    def onRightExMeta(self, event):
        dlg = wx.FileDialog(self, "Choose a save location", '', "", "*.xml", wx.SAVE | wx.OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            full_path = os.path.join(dlg.GetDirectory(), dlg.GetFilename())

            self.selectedIndex = self.tblSeries.GetSelectedObject().id
            #series_id = self.tableSeries.getColumnText(self.selectedIndex, 1)
            #print "series_id", series_id

            self.export_service.export_series_metadata(self.selectedIndex, full_path)
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

        try:
            self.variable_code = self.varList[self.cbVariables.Selection].code
            self.setFilter(site_code=self.site_code, var_code=self.variable_code)
            self.cbVariables.Enabled = True
            self.cbSites.Enabled = True
        except IndexError:
            pass

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
            if self.checkVariable.GetValue():
                self.siteAndVariables()
            else:
                self.siteOnly()
        else:
            if self.checkVariable.GetValue():
                self.variableOnly()
            else:
                self.cbSites.Enabled = False
                self.cbVariables.Enabled = False
        event.Skip()

    def setFilter(self, site_code='', var_code='', advfilter=''):
        if site_code and var_code:
            self.siteFilter = TextSearch(self.tblSeries, columns=self.tblSeries.columns[3:4],text=site_code)
            self.variableFilter = TextSearch(self.tblSeries, columns=self.tblSeries.columns[6:7],text=var_code)
            self.tblSeries.SetFilter(Chain(self.siteFilter, self.variableFilter))
        elif site_code:
            self.tblSeries.SetFilter(TextSearch(self.tblSeries, columns=self.tblSeries.columns[3:4], text=site_code))
        elif var_code:
            self.tblSeries.SetFilter(TextSearch(self.tblSeries, columns=self.tblSeries.columns[6:7], text=var_code))
        elif advfilter:
            self.tblSeries.SetFilter(advfilter)
        else:
            self.tblSeries.SetFilter(TextSearch(self.tblSeries, columns=self.tblSeries.columns[0:1]))
        self.tblSeries.RepopulateList()


    def onReadyToPlot(self, event):
        """Plots a series selected from the series selector

        :param event: EVT_OVL_CHECK_EVENT type
        """

        checkedCount = len(self.tblSeries.GetCheckedObjects())
        Publisher.sendMessage("EnablePlotButtons", plot=0, isActive=(checkedCount > 0))

        try:
            object = event.object
        except:
            object = self.tblSeries.GetSelectedObject()

        if not self.tblSeries.IsChecked(object):
            Publisher.sendMessage("removePlot", seriesID=object.id)
        else:
            #logger.debug("%d" % (len(self.tblSeries.GetCheckedObjects())))
            self.parent.Parent.addPlot(self.memDB, object.id)


        self.Refresh()

    def getSelectedObject(self, event):
        """Capture the currently selected Object to be used for editing

        :param event: wx.EVT_LIST_ITEM_FOCUSED type
        """

        object = event.GetEventObject()
        editingObject = object.innerList[object.FocusedItem]

        self.tblSeries.currentlySelectedObject = editingObject

        ## update Cursor
        Publisher.sendMessage("updateCursor", selectedObject=editingObject)

    def onReadyToEdit(self):
        """Choose a series to edit from the series selector"""

        ovl = self.tblSeries

        object = ovl.currentlySelectedObject
        if object is None:
            # # Select the first one
            if len(ovl.modelObjects) == 0:
                logger.fatal("There are no model objects available to edit")
                raise Exception()
            object = ovl.modelObjects[0]

        if len(ovl.GetCheckedObjects()) <= ovl.allowedLimit:
            if object not in ovl.GetCheckedObjects():
                ovl.ToggleCheck(object)

            self.memDB.initEditValues(object.id)
            self.isEditing = True
            ovl.editingObject = object
            ovl.RefreshObject(ovl.editingObject)

            return True, object.id, self.memDB
        else:
            isSelected = False
            logger.debug("series was not checked")
            val_2 = wx.MessageBox("Visualization is limited to 6 series.", "Can't add plot",
                                  wx.OK | wx.ICON_INFORMATION)

        self.isEditing = False
        ovl.editingObject = None
        return False, object.id, self.memDB

    def stopEdit(self):
        """When edit button is untoggled, the editing feature closes"""
        self.isEditing = False
        self.tblSeries.RefreshObject(self.tblSeries.editingObject)
        self.tblSeries.editingObject = None
        self.memDB.stopEdit()

    def isEditing(self):
        return self.isEditing


    def _rowFormatter(self, listItem, object):
        """Handles the formatting of rows for object list view
        :param: wx.ListCtrl listitem
        :param: ModelObject object

        :rtype: None
        """
        '''
        if self.tblSeries.editingObject and \
                        object.id == self.tblSeries.editingObject.id:
            #listItem.SetTextColour(wx.Colour(255, 25, 112))
            # font type: wx.DEFAULT, wx.DECORATIVE, wx.ROMAN, wx.SCRIPT, wx.SWISS, wx.MODERN
            # slant: wx.NORMAL, wx.SLANT or wx.ITALIC
            # weight: wx.NORMAL, wx.LIGHT or wx.BOLD
            #font1 = wx.Font(10, wx.SWISS, wx.ITALIC, wx.NORMAL)
            # use additional fonts this way ...
            #font1 = wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL, False, u'Comic Sans MS')
            listItem.SetFont(
                wx.Font(9, family=wx.DEFAULT, weight=wx.BOLD, style=wx.ITALIC))
        else:
            listItem.SetTextColour(wx.Colour())
            listItem.SetFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.NORMAL, False))
        '''

##########only use this section when testing series selector #############
if __name__ == '__main__':
    app = wx.App(False)
    frame = create(None)
    frame.Show()

    app.MainLoop()
##################################################################

