#!/usr/bin/env
#Boa:Frame:ODMTools

'''
this_file = os.path.realpath(__file__)
directory = os.path.dirname(os.path.dirname(this_file))
sys.path.insert(0, directory)
'''

import wx
import sys
import os
import logging
import mnuRibbon
from odmtools.gui.frmConsole import ODMConsole
import pnlSeriesSelector
import pnlPlot
import pnlDataTable
import wx.lib.agw.aui as aui
import wx.py.crust
import wx.stc
from odmtools.common import gtk_execute
from odmtools.lib.Appdirs.appdirs import user_config_dir
from wx.lib.pubsub import pub as Publisher
from odmtools.odmservices import ServiceManager
from pnlScript import pnlScript
from odmtools.common.logger import LoggerTool
from odmtools.controller import frmDBConfig
from odmtools.controller.frmAbout import  frmAbout


def create(parent):
    return frmODMToolsMain(parent)
[
    wxID_ODMTOOLS, wxID_ODMTOOLSCHECKLISTBOX2, wxID_ODMTOOLSCOMBOBOX1,
    wxID_ODMTOOLSCOMBOBOX2, wxID_ODMTOOLSCOMBOBOX4, wxID_ODMTOOLSCOMBOBOX5,
    wxID_ODMTOOLSGRID1, wxID_ODMTOOLSPANEL1, wxID_ODMTOOLSPANEL2,
    wxID_ODMTOOLSTOOLBAR1, wxID_PNLSELECTOR, wxID_TXTPYTHONSCRIPT,
    wxID_TXTPYTHONCONSOLE,
] = [wx.NewId() for _init_ctrls in range(13)]

tool = LoggerTool()
logger = tool.setupLogger(__name__, __name__ + '.log', 'w', logging.DEBUG)

class frmODMToolsMain(wx.Frame):
    def __init__(self, parent):
        self._init_database()
        self.createService()
        self._init_ctrls(parent)
        self.Refresh()

    #############Entire Form Sizers##########
    def _init_sizers(self):
        # generated method, don't edit
        self.s = wx.BoxSizer(wx.VERTICAL)
        self._init_s_Items(self.s)
        self.SetSizer(self.s)

    def _init_s_Items(self, parent):
        # generated method, don't edit
        parent.AddWindow(self._ribbon, 0, wx.EXPAND)
        parent.AddWindow(self.pnlDocking, 85, flag=wx.ALL | wx.EXPAND)

    def _init_database(self):
        logger.debug("Loading Database...")

        self.service_manager = ServiceManager()
        self.record_service = None
        if not self.service_manager.is_valid_connection():
            db_config = frmDBConfig.frmDBConfig(None, self.service_manager, False)
            value = db_config.ShowModal()
            db_config.Destroy()

            if value == wx.ID_CANCEL:
                logger.fatal("ODMTools is now closing because there is no database connection.")
                sys.exit(0)
    def on_about_request(self, event):
        frmAbout(self)


    def MacReopenApp(self):
        """Called when the doc icon is clicked, and ???"""

        try: # it's possible for this event to come when the frame is closed
            self.GetTopWindow().Raise()
        except:
            pass

    ###################### Frame ################
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        logger.debug("Loading frame...")
        wx.Frame.__init__(self, id=wxID_ODMTOOLS, name=u'ODMTools', parent=prnt,
                          size=wx.Size(1000, 900),
                          style=wx.DEFAULT_FRAME_STYLE, title=u'ODM Tools')

        self.SetIcon(gtk_execute.getIcon())

        self.SetFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.NORMAL,
                             False, u'Tahoma'))

        ############### Ribbon ###################
        logger.debug("Loading Ribbon Menu...")
        self._ribbon = mnuRibbon.mnuRibbon(parent=self, id=wx.ID_ANY, name='ribbon')


        if sys.platform == 'darwin':
            self.menu_bar  = wx.MenuBar()
            self.help_menu = wx.Menu()

            self.help_menu.Append(wx.ID_ABOUT,   "&About MyApp")
            self.menu_bar.Append(self.help_menu, "&Help")

            self.SetMenuBar(self.menu_bar)
            self.Bind(wx.EVT_MENU, self.on_about_request, id=wx.ID_ABOUT)

    #        self.menu_bar.SetAutoWindowMenu()


        ################ Docking Tools##############
        self.pnlDocking = wx.Panel(id=wxID_ODMTOOLSPANEL1, name='pnlDocking',
                                   parent=self, size=wx.Size(605, 458),
                                   style=wx.TAB_TRAVERSAL)

        ################ Series Selection Panel ##################
        logger.debug("Loading Series Selector ...")
        self.pnlSelector = pnlSeriesSelector.pnlSeriesSelector(id=wxID_PNLSELECTOR, name=u'pnlSelector',
                                                               parent=self.pnlDocking, size=wx.Size(770, 388),
                                                               style=wx.TAB_TRAVERSAL, dbservice=self.sc)

        ####################grid Table View##################
        logger.debug("Loading DataTable ...")
        self.dataTable = pnlDataTable.pnlDataTable(id=wxID_ODMTOOLSGRID1, name='dataTable',
                                                   parent=self.pnlDocking, size=wx.Size(376, 280),
                                                   style=0)

        ############# Graph ###############
        logger.debug("Loading Plot ...")
        self.pnlPlot = pnlPlot.pnlPlot(id=wxID_ODMTOOLSPANEL1, name='pnlPlot',
                                       parent=self.pnlDocking, size=wx.Size(605, 458),
                                       style=wx.TAB_TRAVERSAL)


        ############# Script & Console ###############
        logger.debug("Loading Python Console ...")
        self.txtPythonConsole = ODMConsole(id=wxID_TXTPYTHONCONSOLE, size=wx.Size(200, 200), )
        wx.CallAfter(self._postStartup)

        # FIXME closing the txtPythonConsole from menu crashes the python console. We will need to extend pyCrust to remove this so that we don't have issues in the future.

        self.txtPythonConsole.shell.run("import datetime", prompt=False, verbose=False)

        self.txtPythonConsole.shell.run("edit_service = app.TopWindow.record_service", prompt=False, verbose=False)
        self.txtPythonConsole.shell.run("import datetime", prompt=False, verbose=False)

        logger.debug("Loading Python Script ...")
        self.txtPythonScript = pnlScript(id=wxID_TXTPYTHONSCRIPT, name=u'txtPython', parent=self,
                                         size=wx.Size(200, 200))

        ############ Docking ###################
        logger.debug("Loading AuiManager ...")
        self._mgr = aui.AuiManager()
        self._mgr.SetManagedWindow(self.pnlDocking)

        self._mgr.AddPane(self.pnlPlot, aui.AuiPaneInfo().CenterPane()
                          .Name("Plot").Caption("Plot").MaximizeButton(True))

        self._mgr.AddPane(self.dataTable, aui.AuiPaneInfo().Right().Name("Table").
                          Show(show=False).Caption('Table View').MinSize(wx.Size(200, 200)).Floatable().Movable().
                          Position(1).MinimizeButton(True).MaximizeButton(True))

        self._mgr.AddPane(self.pnlSelector, aui.AuiPaneInfo().Bottom().Name("Selector").MinSize(wx.Size(50, 200)).
                          Movable().Floatable().Position(0).MinimizeButton(True).MaximizeButton(True).CloseButton(True))
        self.refreshConnectionInfo()

        self._mgr.AddPane(self.txtPythonScript, aui.AuiPaneInfo().Caption('Script').
                          Name("Script").Movable().Floatable().Right()
                          .MinimizeButton(True).MaximizeButton(True).FloatingSize(size=(600, 800))
                          .CloseButton(True).Float().FloatingPosition(pos=(self.Position))
                          .Show(show=False).Hide().CloseButton(False)
        )
        self._mgr.AddPane(self.txtPythonConsole, aui.AuiPaneInfo().Caption('Python Console').
                          Name("Console").FloatingSize(size=(600, 800)).MinimizeButton(
            True).Movable().Floatable().MaximizeButton(True).CloseButton(True).Float().Show(
            show=False).Hide())

        ## TODO Fix loadingDockingSettings as it doesn't load it correctly.
        #self.loadDockingSettings()

        self._mgr.Update()
        self.Bind(wx.EVT_CLOSE, self.onClose)

        Publisher.subscribe(self.onDocking, ("adjust.Docking"))
        Publisher.subscribe(self.onPlotSelection, ("select.Plot"))
        Publisher.subscribe(self.onExecuteScript, ("execute.script"))
        Publisher.subscribe(self.onChangeDBConn, ("change.dbConfig"))
        Publisher.subscribe(self.onSetScriptTitle, ("script.title"))
        #.subscribe(self.onSetScriptTitle, ("script.title"))
        Publisher.subscribe(self.onClose, ("onClose"))
        Publisher.subscribe(self.addEdit, ("selectEdit"))
        Publisher.subscribe(self.stopEdit, ("stopEdit"))

        self._init_sizers()
        self._ribbon.Realize()
        logger.debug("System starting ...")

    def refreshConnectionInfo(self):
        """Updates the Series Selector Connection Information for the user"""

        conn_dict = self.service_manager.get_current_conn_dict()

        msg = 'Series: %s://%s@%s/%s' % (
            conn_dict['engine'], conn_dict['user'], conn_dict['address'], conn_dict['db']
        )

        self._mgr.GetPane('Selector').Caption(msg)
        self._mgr.RefreshCaptions()


    def onDocking(self, value):
        paneDetails = self._mgr.GetPane(self.pnlPlot)

        if value == "Table":
            paneDetails = self._mgr.GetPane(self.dataTable)

        elif value == "Selector":
            paneDetails = self._mgr.GetPane(self.pnlSelector)

        elif value == "Script":
            paneDetails = self._mgr.GetPane(self.txtPythonScript)
            if paneDetails.IsNotebookPage():
                paneDetails.Float()
            if paneDetails.IsFloating():
                paneDetails.Dock()
            paneDetails.FloatingPosition(pos=self.Position)

        elif value == "Console":
            paneDetails = self._mgr.GetPane(self.txtPythonConsole)
            self.txtPythonConsole.crust.OnSashDClick(event=None)
            if paneDetails.IsNotebookPage():
                paneDetails.Float()
            paneDetails.FloatingPosition(pos=self.Position)

        if paneDetails.IsShown():
            paneDetails.Show(show=False)
        else:
            paneDetails.Show(show=True)
        #print "Shown?", paneDetails.IsShown()


        self._mgr.Update()

    def onPlotSelection(self, value):
        self.pnlPlot.selectPlot(value)

    def addPlot(self, memDB, seriesID):
        #Memory Database
        self.pnlPlot.addPlot(memDB, seriesID)
        Publisher.sendMessage("EnablePlotButton", plot=self.pnlPlot.getActivePlotID(), isActive=True)
        #self._ribbon.enableButtons(self.pnlPlot.getActivePlotID)

    def onSetScriptTitle(self, title):
        scriptPane = self._mgr.GetPane(self.txtPythonScript)
        scriptPane.Caption(title)
        if scriptPane.IsFloating():
            scriptPane.Restore()
        self._mgr.Update()

    def addEdit(self, event):
        isSelected, seriesID, memDB = self.pnlSelector.onReadyToEdit()

        if isSelected:
            self.record_service = self.service_manager.get_record_service(self.txtPythonScript, seriesID,
                                                                          connection=memDB.conn)
            self._ribbon.toggleEditButtons(True)
            self.pnlPlot.addEditPlot(memDB, seriesID, self.record_service)
            self.dataTable.init(memDB, self.record_service)

            # set record service for console
            Publisher.sendMessage("setEdit", isEdit=True)
            logger.debug("Enabling Edit")
            self.record_service.toggle_record()
            #self._mgr.GetPane(self.txtPythonScript).Show(show=True)


        else:
            logger.debug("disabling Edit")
            Publisher.sendMessage("setEdit", isEdit=False)
            self.record_service.toggle_record()
            #self._mgr.GetPane(self.txtPythonScript).Show(show=False)

        #self._mgr.Update()

        logger.debug("Recording? %s" % self.record_service._record)


            #self.record_service = None
        self.txtPythonConsole.shell.run("edit_service = app.TopWindow.record_service", prompt=False, verbose=False)
        self.txtPythonConsole.shell.run("series_service = edit_service.get_series_service()", prompt=False, verbose=False)



    def stopEdit(self, event):

        self.pnlSelector.stopEdit()
        self.dataTable.stopEdit()
        self.pnlPlot.stopEdit()
        Publisher.sendMessage("toggleEdit", checked=False)
        self.record_service = None
        self._ribbon.toggleEditButtons(False)


    def getRecordService(self):
        return self.record_service

    def onChangeDBConn(self, event):
        db_config = frmDBConfig.frmDBConfig(None, self.service_manager, False)
        value = db_config.ShowModal()

        #print "Value: ", value
        #print "wxID_FRMDBCONFIGBTNSAVE: ", db_config._init_ctrls[2] #wxID_FRMDBCONFIGBTNSAVE
        #print "wxID_FRMDBCONFIGBTNCANCEL: ", db_config._init_ctrls[3] #wxID_FRMDBCONFIGBTNCANCEL
        #print "wxID_FRMDBCONFIGBTNTEST: ", db_config._init_ctrls[4] #wxID_FRMDBCONFIGBTNTEST

        if value == wx.ID_OK:
            self.createService()
            self.pnlSelector.resetDB(self.sc)
            self.refreshConnectionInfo()
            self.pnlPlot.clear()
            #self.pnlSelector.tableSeries.clearFilter()
            self.dataTable.clear()
            #self.pnlSelector.tableSeries.checkCount = 0

    def createService(self):
        self.sc = self.service_manager.get_series_service()
        return self.sc

    def getDBService(self):
        return self.service_manager

    def toggleConsoleTools(self):
        self.txtPythonConsole.ToggleTools()

    def onExecuteScript(self, value):
        for i in ('red', 'blue', 'green', 'magenta', 'gold', 'cyan', 'brown', 'lime', 'purple', 'navy'):
            self.txtPythonScript('This is a test\n', i)

    def loadDockingSettings(self):
        #test if there is a perspective to load
        try:
            # TODO Fix resource_path to appdirs
            os.path.join(user_config_dir("ODMTools", "UCHIC"), 'ODMTools.config')
            f = open(os.path.join(user_config_dir("ODMTools", "UCHIC"), 'ODMTools.config'), 'r')
        except:
            # Create the file if it doesn't exist
            open(os.path.join(user_config_dir("ODMTools", "UCHIC"), 'ODMTools.config'), 'w').close()
            f = open(os.path.join(user_config_dir("ODMTools", "UCHIC"), 'ODMTools.config'), 'r')

        self._mgr.LoadPerspective(f.read(), True)

    def onClose(self, event):
        """
            Closes ODMTools Python
            Closes AUI Manager then closes MainWindow
        """
        # deinitialize the frame manager
        self.pnlPlot.Close()
        try:
            f = open(os.path.join(user_config_dir("ODMTools", "UCHIC"), 'ODMTools.config'), 'w')
            f.write(self._mgr.SavePerspective())
        except:
            print "error saving docking data"
        self._mgr.UnInit()

        # IMPORTANT! if wx.TaskBarIcons exist, it will keep mainloop running

        windowsRemaining = len(wx.GetTopLevelWindows())
        if windowsRemaining > 0:
            import wx.lib.agw.aui.framemanager as aui
            # logger.debug("Windows left to close: %d" % windowsRemaining)
            for item in wx.GetTopLevelWindows():
                #logger.debug("Windows %s" % item)
                if not isinstance(item, self.__class__):
                    if isinstance(item, aui.AuiFloatingFrame):
                        item.Destroy()
                    elif isinstance(item, aui.AuiSingleDockingGuide):
                        item.Destroy()
                    elif isinstance(item, aui.AuiDockingHintWindow):
                        item.Destroy()
                    elif isinstance(item, wx.Dialog):
                        item.Destroy()
                    item.Close()
        self.Destroy()

        wx.GetApp().ExitMainLoop()

    def _postStartup(self):
        """
            Called after MainLoop is initialized
                Hides Python Console Tools
        """
        if self.txtPythonConsole.ToolsShown():
            self.txtPythonConsole.ToggleTools()
