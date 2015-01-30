import os
import wx
import logging

from wx.lib.pubsub import pub as Publisher
from odmtools.lib.ObjectListView.Filter import TextSearch, Chain
import odmtools.gui.frmQueryBuilder as frmQueryBuilder

from odmtools.common.logger import LoggerTool
from odmtools.odmdata import MemoryDatabase
from odmtools.view import clsSeriesSelector

tool = LoggerTool()
logger = tool.setupLogger(__name__, __name__ + '.log', 'w', logging.DEBUG)

__author__ = 'Jacob'

class FrmSeriesSelector(clsSeriesSelector.ClsSeriesSelector):
    """

    """
    def __init__(self, *args, **kwargs):
        """

        """

        self.taskserver = kwargs.pop("taskserver")
        self.pnlPlot = kwargs.pop("plot")

        clsSeriesSelector.ClsSeriesSelector.__init__(self, *args, **kwargs)

    def initPubSub(self):
        #Publisher.subscribe(self.onEditButton, ("selectEdit"))
        Publisher.subscribe(self.refreshSeries, "refreshSeries")

    def resetDB(self, dbservice):
        """

        :param dbservice:
        :return:
        """

        if not self.rbAll.GetValue():
            #self.GetEventHandler().ProcessEvent(wx.PyCommandEvent(wx.EVT_RADIOBUTTON.typeId, self.rbAll.Id))
            wx.PostEvent(self.GetEventHandler(), wx.PyCommandEvent(wx.EVT_RADIOBUTTON.typeId, self.rbAll.Id))
            self.rbAll.SetValue(True)

        #####INIT DB Connection
        self.dbservice = dbservice
        self.cbVariables.Clear()
        self.cbSites.Clear()

        self.siteList = None
        self.varList = None

        self.initTableSeries()
        self.initSVBoxes()
        self.Layout()

    def initTableSeries(self):
        """Set up columns and objects to be used in the objectlistview to be visible in the series selector

        :return:
        """
        try:
            self.memDB = MemoryDatabase(self.dbservice)
            object = self.dbservice.get_all_series()

            if object:
                self.tblSeries.SetObjects(object)
            else:
                self.tblSeries.SetObjects(None)

        except AttributeError as e:
            logger.error(e)
            #self.tblSeries.SaveObject(object)

    def refreshTableSeries(self, db):
        """ Refreshes the objectlistview to include newly saved database series and preserve which series was 'checked'
        for plotting/editing

        :return:
        """
        self.memDB = MemoryDatabase(db)
        object = self.dbservice.get_all_series()
        #checkedObjs = self.tblSeries.GetCheckedObjects()
        idList = [x.id for x in self.tblSeries.modelObjects]

        for x in object:
            if x.id not in idList:
                self.tblSeries.AddObject(x)

        #for x in checkedObjs:
        #    super(FastObjectListView, self.tblSeries).SetCheckState(x, True)

    def refreshSeries(self):
        """

        :return:
        """
        self.dbservice = None
        self.dbservice = self.parent.Parent.createService()
        self.refreshTableSeries(self.dbservice)
        #self.resetDB(self.dbservice)
        logger.debug("Refresh Occurred")

    def initSVBoxes(self):
        """

        :return:
        """

        self.site_code = None
        self.variable_code = None

        #####INIT drop down boxes for Simple Filter
        try:
            self.siteList = self.dbservice.get_all_used_sites()
            for site in self.siteList:
                self.cbSites.Append(site.code + '-' + site.name)
            self.cbSites.SetSelection(0)
            self.site_code = self.siteList[0].code

            self.varList = self.dbservice.get_all_used_variables()
            for var in self.varList:
                self.cbVariables.Append(var.code + '-' + var.name)
            self.cbVariables.SetSelection(0)
        except AttributeError as e:
            logger.error(e)

    def OnTableRightDown(self, event):
        """Right click down menu

        :param event:
        :return:
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
        plotItem = popup_menu.Append(popup_plot_series, 'Plot')
        editItem = popup_menu.Append(popup_edit_series, 'Edit')

        self.Bind(wx.EVT_MENU, self.onRightPlot, plotItem)
        # TODO @jmeline needs to fix edit, it doesn't unedit when a plot is being edited
        self.Bind(wx.EVT_MENU, self.onRightEdit, editItem)
        # TODO @jmeline will refresh and clear selected as an enhancement
        #self.Bind(wx.EVT_MENU, self.onRightRefresh, popup_menu.Append(popup_series_refresh, 'Refresh'))
        #self.Bind(wx.EVT_MENU, self.onRightClearSelected, popup_menu.Append(popup_series_refresh, 'Clear Selected'))

        popup_menu.AppendSeparator()
        self.Bind(wx.EVT_MENU, self.onRightExData, popup_menu.Append(popup_export_data, 'Export Data'))
        self.Bind(wx.EVT_MENU, self.onRightExMeta, popup_menu.Append(popup_export_metadata, 'Export MetaData'))

        if self.isEditing:
            popup_menu.Enable(popup_edit_series, False)

        self.tblSeries.PopupMenu(popup_menu)
        event.Skip()

    def onPaneChanged(self, event=None):
        #if event:
        #    print 'wx.EVT_COLLAPSIBLEPANE_CHANGED: %s\n' % event.Collapsed
        self.Layout()

    def onRbAdvancedRadiobutton(self, event):
        """

        :param event:
        :return:
        """

        self.cpnlSimple.Collapse(True)
        self.Layout()
        series_filter = frmQueryBuilder.frmQueryBuilder(self)
        self.filterlist = series_filter.ShowModal()
        event.Skip()

    def onRbAllRadiobutton(self, event):
        """

        :param event:
        :return:
        """

        logger.debug("onRbAllRadioButton called! ")
        self.cpnlSimple.Collapse(True)
        self.Layout()
        self.setFilter()
        event.Skip()

    def onRbSimpleRadiobutton(self, event):
        """

        :param event:
        :return:
        """

        self.cpnlSimple.Expand()
        self.Layout()

        if not self.checkSite.GetValue() and not self.checkVariable.GetValue():
            self.setFilter()
            return

        self.setFilter(self.site_code, self.variable_code)

        event.Skip()

    def onRightPlot(self, event):
        """

        :param event:
        :return:
        """
        object = self.tblSeries.GetSelectedObject()
        self.tblSeries.ToggleCheck(object)
        self.onReadyToPlot(event)
        event.Skip()

    def onRightEdit(self, event):
        """

        :param event:
        :return:
        """
        Publisher.sendMessage(("selectEdit"), event=event)
        if self.isEditing:
            Publisher.sendMessage("toggleEdit", checked=True)
        event.Skip()

    # allows user to right-click refresh the Series Selector
    def onRightRefresh(self, event):
        """

        :param event:
        :return:
        """
        self.refreshSeries()
        event.Skip()

    def onRightClearSelected(self, event):
        """

        :param event:
        :return:
        """
        event.Skip()



    def onRightExData(self, event):
        """

        :param event:
        :return:
        """
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
        """

        :param event:
        :return:
        """
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
        """

        :param event:
        :return:
        """
        if self.checkSite.GetValue():
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
        """

        :param event:
        :return:
        """
        if self.checkVariable.GetValue():
            self.variable_code = self.varList[event.GetSelection()].code
            if (not self.checkSite.GetValue() and self.checkVariable.GetValue()):
                self.site_code = None
            self.setFilter(site_code=self.site_code, var_code=self.variable_code)
        event.Skip()

    def siteAndVariables(self):
        """

        :return:
        """
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
        """

        :return:
        """
        self.cbVariables.Enabled = False
        self.cbSites.Enabled = True
        self.variable_code = None

        self.site_code = self.siteList[self.cbSites.Selection].code
        self.setFilter(site_code=self.site_code)

    def variableOnly(self):
        """

        :return:
        """
        self.site_code = None
        self.cbVariables.Clear()
        self.varList = self.dbservice.get_all_used_variables()
        for var in self.varList:
            self.cbVariables.Append(var.code + '-' + var.name)
        self.cbVariables.SetSelection(0)
        self.cbSites.Enabled = False
        self.cbVariables.Enabled = True

        self.variable_code = self.varList[0].code

        self.setFilter(var_code=self.variable_code)

    def onCheck(self, event):
        """

        :param event:
        :return:
        """
        # self.tableSeries.DeleteAllItems()
        if not self.checkSite.GetValue() and not self.checkVariable.GetValue():
            self.setFilter()
            self.cbSites.Enabled = False
            self.cbVariables.Enabled = False

        elif self.checkSite.GetValue():
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
        """

        :param site_code:
        :param var_code:
        :param advfilter:
        :return:
        """
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
        logger.debug("Starting to Plot")

        checkedCount = len(self.tblSeries.GetCheckedObjects())

        Publisher.sendMessage("EnablePlotButtons", plot=0, isActive=(checkedCount > 0))

        logger.debug("Obtain object")
        try:
            object = event.object
        except:
            object = self.tblSeries.GetSelectedObject()

        if not self.tblSeries.IsChecked(object):
            Publisher.sendMessage("removePlot", seriesID=object.id)
        else:
            logger.debug("Obtained object, entering addplot")
            self.pnlPlot.addPlot(self.memDB, object.id)
            #Publisher.sendMessage("updateCursor", selectedObject=object)

        logger.debug("refreshing...")
        self.Refresh()

        logger.debug("Finish Plotting")


        #from meliae import scanner
        #scanner.dump_all_objects("plot_plotting.dat")

    def getSelectedObject(self, event):
        """Capture the currently selected Object to be used for editing

        :param event: wx.EVT_LIST_ITEM_FOCUSED type
        """

        object = event.GetEventObject()
        editingObject = object.innerList[object.FocusedItem]

        self.tblSeries.currentlySelectedObject = editingObject

        ## update Cursor
        if self.parent.Parent.pnlPlot._seriesPlotInfo:
            if self.parent.Parent.pnlPlot._seriesPlotInfo.isPlotted(editingObject.id):
                #print "Updating Cursor", editingObject.id
                Publisher.sendMessage("updateCursor", selectedObject=editingObject)


    def onReadyToEdit(self):
        """Choose a series to edit from the series selector

        :return:
        """

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

            logger.debug("Initializing Memory Database")
            self.memDB.initEditValues(object.id)
            logger.debug("Finished Initializing Memory Database")

            # logger.debug("Initializing DataTable")
            #
            # tasks = [("dataTable", self.memDB.conn)]
            # self.taskserver.setTasks(tasks)
            # self.taskserver.processTasks()

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
        """When edit button is untoggled, the editing feature closes

        :return:
        """
        self.isEditing = False
        self.tblSeries.RefreshObject(self.tblSeries.editingObject)
        self.tblSeries.editingObject = None
        self.memDB.stopEdit()

    def isEditing(self):
        """

        :return:
        """
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