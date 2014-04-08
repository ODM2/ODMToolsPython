#!/usr/bin/env
#Boa:Frame:ODMTools
import sys
import os

this_file = os.path.realpath(__file__)
directory = os.path.dirname(os.path.dirname(this_file))
sys.path.insert(0, directory)

import wx
import wx.grid
#import wx.aui

try:
    from agw import aui
except ImportError:  # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.aui as aui

import wx.richtext
import wx.stc
import wx.lib.agw.aui as aui
from wx.lib.pubsub import pub as Publisher
import wx.py.crust
import frmDBConfiguration

from odmservices import ServiceManager
from odmservices import utilities as util
from pnlScript import pnlScript
import pnlSeriesSelector
import pnlPlot
import mnuRibbon
import pnlDataTable

from odmconsole import ConsoleTools


def create(parent):
    return frmODMToolsMain(parent)

[
    wxID_ODMTOOLS, wxID_ODMTOOLSCHECKLISTBOX2, wxID_ODMTOOLSCOMBOBOX1,
    wxID_ODMTOOLSCOMBOBOX2, wxID_ODMTOOLSCOMBOBOX4, wxID_ODMTOOLSCOMBOBOX5,
    wxID_ODMTOOLSGRID1, wxID_ODMTOOLSPANEL1, wxID_ODMTOOLSPANEL2,
    wxID_ODMTOOLSTOOLBAR1, wxID_PNLSELECTOR, wxID_TXTPYTHONSCRIPT,
    wxID_TXTPYTHONCONSOLE,
] = [wx.NewId() for _init_ctrls in range(13)]


class frmODMToolsMain(wx.Frame):
    def __init__(self, parent):
        self.service_manager = ServiceManager()
        self.record_service = None
        conn_dict = self.service_manager.get_current_connection()
        #there is a connection but it is unsuccessful
        if (conn_dict == None
            or (conn_dict != None and not self.service_manager.test_connection(conn_dict))):
            # Create a DB form which will set a connection for the service manager
            db_config = frmDBConfiguration.frmDBConfig(None, self.service_manager, False)
            db_config.ShowModal()
        if (conn_dict != None and self.service_manager.get_db_version(conn_dict) != u'1.1.1'):
            wx.MessageBox('The ODM database must be version 1.1.1 to use ODMToolsPython',
                          'Database Version Incompatible', wx.OK)
            db_config = frmDBConfiguration.frmDBConfig(None, self.service_manager, False)
            db_config.ShowModal()

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


    ###################### Form ################
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_ODMTOOLS, name=u'ODMTools', parent=prnt,
                          size=wx.Size(1000, 900),
                          style=wx.DEFAULT_FRAME_STYLE, title=u'ODM Tools')
        self.SetFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.NORMAL,
                             False, u'Tahoma'))

        Publisher.subscribe(self.onDocking, ("adjust.Docking"))
        Publisher.subscribe(self.onPlotSelection, ("select.Plot"))
        Publisher.subscribe(self.onExecuteScript, ("execute.script"))

        Publisher.subscribe(self.onExecuteScript, ("execute.script"))
        Publisher.subscribe(self.onChangeDBConn, ("change.dbConfig"))
        Publisher.subscribe(self.onSetScriptTitle, ("script.title"))
        Publisher.subscribe(self.onClose, ("onClose"))


        ############### Ribbon ###################
        self._ribbon = mnuRibbon.mnuRibbon(parent=self, id=wx.ID_ANY, name='ribbon')


        ################ Docking Tools##############
        self.pnlDocking = wx.Panel(id=wxID_ODMTOOLSPANEL1, name='pnlDocking',
                                   parent=self, size=wx.Size(605, 458),
                                   style=wx.TAB_TRAVERSAL)

        ################ Series Selection Panel ##################
        self.pnlSelector = pnlSeriesSelector.pnlSeriesSelector(id=wxID_PNLSELECTOR, name=u'pnlSelector',
                                                               parent=self.pnlDocking, size=wx.Size(770, 388),
                                                               style=wx.TAB_TRAVERSAL, dbservice=self.sc)

        ####################grid Table View##################
        self.dataTable = pnlDataTable.pnlDataTable(id=wxID_ODMTOOLSGRID1, name='dataTable',
                                                   parent=self.pnlDocking, size=wx.Size(376, 280),
                                                   style=0)

        ############# Graph ###############
        self.pnlPlot = pnlPlot.pnlPlot(id=wxID_ODMTOOLSPANEL1, name='pnlPlot',
                                       parent=self.pnlDocking, size=wx.Size(605, 458),
                                       style=wx.TAB_TRAVERSAL)


        ############# Script & Console ###############
        self.txtPythonConsole = wx.py.crust.CrustFrame(id=wxID_TXTPYTHONCONSOLE,
                                                       size=wx.Size(500, 800), style=0)

        # Console tools object for usability
        self.console_tools = ConsoleTools(self._ribbon)
        self.txtPythonConsole.shell.run("Tools = app.TopWindow.console_tools", prompt=False, verbose=False)

        self.txtPythonScript = pnlScript(id=wxID_TXTPYTHONSCRIPT,
                                         name=u'txtPython', parent=self,
                                         size=wx.Size(200, 200))

        ############ Docking ###################
        self._mgr = aui.AuiManager()
        self._mgr.SetManagedWindow(self.pnlDocking)
        self._mgr.AddPane(self.dataTable, aui.AuiPaneInfo().Right().Name("Table").
                          Show(show=False).Caption('Table View').MinSize(wx.Size(200, 200)))
        self._mgr.AddPane(self.pnlSelector, aui.AuiPaneInfo().Bottom().Name("Selector").
                          Layer(0).Caption('Series Selector').MinSize(wx.Size(100, 200)))
        self._mgr.AddPane(self.txtPythonScript, aui.AuiPaneInfo().Caption('Script').
                          Name("Script").Show(show=False).Layer(0).MinSize(wx.Size(200, 200)))
        self._mgr.AddPane(self.txtPythonConsole, aui.AuiPaneInfo().Caption('Python Console').
                          Name("Console").Layer(1).Show(show=False))

        self._mgr.AddPane(self.pnlPlot, aui.AuiPaneInfo().CenterPane().Name("Plot").Caption("Plot"))

        self.loadDockingSettings()

        self._mgr.Update()

        self.Bind(wx.EVT_CLOSE, self.onClose)

        self._init_sizers()
        self._ribbon.Realize()

    def onDocking(self, value):
        panedet = self._mgr.GetPane(self.pnlPlot)
        if value == "Table":
            panedet = self._mgr.GetPane(self.dataTable)
        elif value == "Selector":
            panedet = self._mgr.GetPane(self.pnlSelector)
        elif value == "Script":
            panedet = self._mgr.GetPane(self.txtPythonScript)
        elif value == "Console":
            panedet = self._mgr.GetPane(self.txtPythonConsole)

        if panedet.IsShown():
            panedet.Show(show=False)
        else:
            panedet.Show(show=True)
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

    def addEdit(self, seriesID, memDB):

        self.record_service = self.service_manager.get_record_service(self.txtPythonScript, seriesID,
                                                                      connection=memDB.conn)
        self.pnlPlot.addEditPlot(memDB, seriesID, self.record_service)
        self.dataTable.init(memDB, self.record_service)
        self._ribbon.toggleEditButtons(True)

        # set record service for console
        self.console_tools.set_record_service(self.record_service)

    def stopEdit(self):
        self.pnlPlot.stopEdit()
        self.dataTable.stopEdit()
        self.pnlSelector.stopEdit()
        self.record_service = None
        self._ribbon.toggleEditButtons(False)

    def getRecordService(self):
        return self.record_service

    def onChangeDBConn(self, event):
        db_config = frmDBConfiguration.frmDBConfig(None, self.service_manager, False)
        value = db_config.ShowModal()

        print "Value: ", value
        #print "wxID_FRMDBCONFIGBTNSAVE: ", db_config._init_ctrls[2] #wxID_FRMDBCONFIGBTNSAVE
        #print "wxID_FRMDBCONFIGBTNCANCEL: ", db_config._init_ctrls[3] #wxID_FRMDBCONFIGBTNCANCEL
        #print "wxID_FRMDBCONFIGBTNTEST: ", db_config._init_ctrls[4] #wxID_FRMDBCONFIGBTNTEST

        if value == wx.ID_OK:
            #reset Series Selector
            self.createService()
            self.pnlSelector.resetDB(self.sc)
            #clear all plots
            self.pnlPlot.clear()
            #clear table
            self.dataTable.clear()



    def createService(self):
        self.sc = self.service_manager.get_series_service()

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
            f = open(util.resource_path('ODMTools.config'), 'r')
        except:
            # Create the file if it doesn't exist
            open(util.resource_path('ODMTools.config'), 'w').close()
            f = open(util.resource_path('ODMTools.config'), 'r')

        self._mgr.LoadPerspective(f.read(), True)

    def onClose(self, event):
        # deinitialize the frame manager
        self.pnlPlot.Close()
        try:
            f = open(util.resource_path('ODMTools.config'), 'w')
            f.write(self._mgr.SavePerspective())
        except:
            print "error saving docking data"
        self._mgr.UnInit()
        # delete the frame
        self.Destroy()


if __name__ == '__main__':
    app = wx.App(False)
    frame = create(None)
    frame.Show()

    app.MainLoop()