
#Boa:FramePanel:Panel1

import datetime

import wx
import wx.lib.agw.ribbon as RB
from wx.lib.pubsub import pub as Publisher
from frmDataFilters import frmDataFilter
from frmChangeValue import frmChangeValue
from frmAddPoint import frmAddPoint
from frmFlagValues import frmFlagValues
from frmLinearDrift import frmLinearDrift
import wizSave
import gui_utils as g_util


## Enable logging
import logging
from common.logger import LoggerTool
tool = LoggerTool()
logger = tool.setupLogger(__name__, __name__ + '.log', 'w', logging.DEBUG)
##

[wxID_PANEL1, wxID_RIBBONPLOTTIMESERIES, wxID_RIBBONPLOTPROB,
 wxID_RIBBONPLOTHIST, wxID_RIBBONPLOTBOX, wxID_RIBBONPLOTSUMMARY,
 wxID_RIBBONPLOTTSTYPE, wxID_RIBBONPLOTTSCOLOR, wxID_RIBBONPLOTTSLEGEND,
 wxID_RIBBONPLOTBOXTYPE, wxID_RIBBONPLOTHISTTYPE, wxID_RIBBONPLOTHISTBIN,
 wxID_RIBBONPLOTDATEEND, wxID_RIBBONPLOTDATEREFRESH, wxID_RIBBONPLOTDATEFULL,
 wxID_RIBBONEDITSERIES, wxID_RIBBONEDITDERIVE, wxID_RIBBONEDITRESTORE,
 wxID_RIBBONEDITSAVE, wxID_RIBBONEDITCHGVALUE, wxID_RIBBONEDITINTEROPOLATE,
 wxID_RIBBONEDITFLAG, wxID_RIBBONEDITADDPOINT, wxID_RIBBONEDITDELPOINT,
 wxID_RIBBONEDITSCRIPTEXECUTE, wxID_RIBBONEDITSCRIPTOPEN, wxID_RIBBONEDITSCRIPTNEW,
 wxID_RIBBONEDITSCRIPTSAVE, wxID_RIBBONVIEWPLOT, wxID_RIBBONVIEWTABLE,
 wxID_RIBBONVIEWSERIES, wxID_RIBBONVIEWCONSOLE, wxID_RIBBONVIEWSCRIPT,
 wxID_RIBBONPLOTBLANKBTN, wxID_FileMenu, wxID_STARTDPDATE, wxID_ENDDPDATE,
 wxID_FRAME1SPINCTRL1, wxID_RIBBONEDITFILTER, wxID_RIBBONEDITRECORD,
 wxID_RIBBONEDITLINFILTER, wxID_RIBBONPLOTDATEAPPLY,wxID_RIBBONEDITRESETFILTER
] = [wx.NewId() for _init_ctrls in range(43)]

## #################################
## Build Menu and Toolbar 
## #################################

class mnuRibbon(RB.RibbonBar):
    def _init_ctrls(self, prnt):
        RB.RibbonBar.__init__(self, name='ribbon', parent=prnt, id=wxID_PANEL1)
        self.SetArtProvider(RB.RibbonAUIArtProvider())
        self.SetFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.NORMAL,
                             False, u'Tahoma'))

        fileMenu = RB.RibbonPage(self, wxID_FileMenu, "File",
                                 wx.Bitmap(g_util.resource_path("images" + g_util.slash() + "3d_graph.png")))

        #----PlotMenu-------------
        home = RB.RibbonPage(self, wx.ID_ANY, "Plot",
                             wx.Bitmap(g_util.resource_path("images" + g_util.slash() + "3d_graph.png")))


        #------Plot Type ---------------------------------------------------------------------------

        plot_panel = RB.RibbonPanel(home, wx.ID_ANY, "Plots", wx.NullBitmap, wx.DefaultPosition,
                                    wx.DefaultSize, RB.RIBBON_PANEL_NO_AUTO_MINIMISE)
        plots_bar = RB.RibbonButtonBar(plot_panel, wx.ID_ANY)
        plots_bar.AddSimpleButton(wxID_RIBBONPLOTTIMESERIES, "Time Series",
                                  wx.Bitmap(g_util.resource_path("images" + g_util.slash() + "tsa_icon.png")), "")
        plots_bar.AddSimpleButton(wxID_RIBBONPLOTPROB, "Probablity",
                                  wx.Bitmap(g_util.resource_path("images" + g_util.slash() + "probability.png")), "")
        plots_bar.AddSimpleButton(wxID_RIBBONPLOTHIST, "Histogram",
                                  wx.Bitmap(g_util.resource_path("images" + g_util.slash() + "histogram.png")), "")
        plots_bar.AddSimpleButton(wxID_RIBBONPLOTBOX, "Box/Whisker",
                                  wx.Bitmap(g_util.resource_path("images" + g_util.slash() + "box_whisker.png")), "")
        plots_bar.AddSimpleButton(wxID_RIBBONPLOTSUMMARY, "Summary",
                                  wx.Bitmap(g_util.resource_path("images" + g_util.slash() + "summary.png")), "")


        #-- PLOT OPTIONS-----------------------------------------------------------------------------
        PlotOptions_panel = RB.RibbonPanel(home, wx.ID_ANY, "Plot Options", wx.NullBitmap, wx.DefaultPosition,
                                           wx.DefaultSize, RB.RIBBON_PANEL_NO_AUTO_MINIMISE)
        self.PlotsOptions_bar = RB.RibbonButtonBar(PlotOptions_panel, wx.ID_ANY)

        self.PlotsOptions_bar.AddDropdownButton(wxID_RIBBONPLOTTSTYPE, "Plot Type",
                                                wx.Bitmap(
                                                    g_util.resource_path("images" + g_util.slash() + "plot_type.png")),
                                                "")

        self.PlotsOptions_bar.AddSimpleButton(wxID_RIBBONPLOTTSLEGEND, "Show Legend",
                                              wx.Bitmap(g_util.resource_path("images" + g_util.slash() + "legend.png")),
                                              help_string="show legend on plot", kind=0x4)


        self.PlotsOptions_bar.AddSimpleButton( wxID_RIBBONPLOTBLANKBTN, "#Hist Bins",
                                wx.Bitmap(g_util.resource_path("images" + g_util.slash() + "blank.png")), "")


        self.PlotsOptions_bar.EnableButton(wxID_RIBBONPLOTBLANKBTN, False)


        self.spnBins = wx.SpinCtrl(id=wxID_FRAME1SPINCTRL1, initial=50,
                                   max=100, min=1, name='spnBins', parent=self.PlotsOptions_bar,
                                   pos=wx.Point(85, 7),  #without color button
                                   size=wx.Size(44, 25), style=wx.SP_ARROW_KEYS)
        self.spnBins.Enabled = False

        self.PlotsOptions_bar.AddDropdownButton(wxID_RIBBONPLOTBOXTYPE, "Box Whisker Type",
                                                wx.Bitmap(g_util.resource_path(
                                                    "images" + g_util.slash() + "box_whisker_type.png")), "")

        self.PlotsOptions_bar.EnableButton(wxID_RIBBONPLOTTSTYPE, False)
        self.PlotsOptions_bar.EnableButton(wxID_RIBBONPLOTTSLEGEND, False)
        self.PlotsOptions_bar.EnableButton(wxID_RIBBONPLOTBOXTYPE, False)

        dateTime_panel = RB.RibbonPanel(home, wx.ID_ANY, "Date Time", wx.NullBitmap, wx.DefaultPosition,
                                        wx.DefaultSize, RB.RIBBON_PANEL_NO_AUTO_MINIMISE)

        self.dateTime_buttonbar = RB.RibbonButtonBar(dateTime_panel)


        self.dateTime_buttonbar.AddSimpleButton(wxID_RIBBONPLOTBLANKBTN, "",
                                        wx.Bitmap(g_util.resource_path("images" + g_util.slash() + "Blank.png")), "")
        self.dateTime_buttonbar.AddSimpleButton(wxID_RIBBONPLOTBLANKBTN, "",
                                        wx.Bitmap(g_util.resource_path("images" + g_util.slash() + "Blank.png")), "")
        self.dateTime_buttonbar.AddSimpleButton(wxID_RIBBONPLOTBLANKBTN, "",
                                        wx.Bitmap(g_util.resource_path("images" + g_util.slash() + "Blank.png")), "")
        self.dateTime_buttonbar.EnableButton(wxID_RIBBONPLOTBLANKBTN, False)

        self.dpStartDate = wx.DatePickerCtrl(id=wxID_STARTDPDATE, name=u'dpStartDate',
                                             parent=self.dateTime_buttonbar, pos=wx.Point(5, 8), size=wx.Size(120, 24),
                                             style=wx.DP_DROPDOWN)
        self.dpStartDate.SetValue(wx.DateTimeFromDMY(16, 1, 2008, 0, 0, 0))
        self.dpStartDate.SetLabel(repr(wx.DateTimeFromDMY(16, 1, 2008, 0, 0, 0)))
        self.dpStartDate.SetToolTipString(u'Start Date')

        self.dpEndDate = wx.DatePickerCtrl(id=wxID_ENDDPDATE, name=u'dpEndDate',
                                           parent=self.dateTime_buttonbar, pos=wx.Point(5, 40), size=wx.Size(120, 24),
                                           style=wx.DP_DROPDOWN)
        self.dpEndDate.SetValue(wx.DateTimeFromDMY(01, 04, 2008, 0, 0, 0))
        self.dpEndDate.SetLabel(repr(wx.DateTimeFromDMY(1, 04, 2008, 0, 0, 0)))
        self.dpEndDate.SetToolTipString(u'End Date')

        self.dateTime_buttonbar.AddSimpleButton(wxID_RIBBONPLOTDATEAPPLY, "Apply",
                                                wx.Bitmap(g_util.resource_path(
                                                    "images" + g_util.slash() + "date_setting.png")), "")

        self.dateTime_buttonbar.AddSimpleButton(wxID_RIBBONPLOTDATEFULL, "Full Date Range",
                                                wx.Bitmap(g_util.resource_path(
                                                    "images" + g_util.slash() + "full_date_range.png")), "")

        self.dateTime_buttonbar.EnableButton(wxID_RIBBONPLOTDATEFULL, False)
        self.dateTime_buttonbar.EnableButton(wxID_RIBBONPLOTDATEAPPLY, False)
        self.dpEndDate.Enabled = False
        self.dpStartDate.Enabled = False

        #-------------------------------------------------------------------------------
        editPage = RB.RibbonPage(self, wx.ID_ANY, "Edit",
                                 wx.Bitmap(g_util.resource_path("images" + g_util.slash() + "blank.png")))

        main_panel = RB.RibbonPanel(editPage, wx.ID_ANY, "Main", wx.NullBitmap, wx.DefaultPosition,
                                    wx.DefaultSize, RB.RIBBON_PANEL_NO_AUTO_MINIMISE)
        self.main_bar = RB.RibbonButtonBar(main_panel)
        self.editbutton=self.main_bar.AddSimpleButton(wxID_RIBBONEDITSERIES, "Edit Series",
                                      bitmap=wx.Bitmap(g_util.resource_path("images" + g_util.slash() + "edit.png")),
                                      help_string="", kind=0x4)#kind sets the button to be a True or False

        self.main_bar.AddSimpleButton(wxID_RIBBONEDITRESTORE, "Restore Series",
                                      wx.Bitmap(g_util.resource_path("images" + g_util.slash() + "restore.png")), "")
        self.main_bar.AddSimpleButton(wxID_RIBBONEDITSAVE, "Save",
                                      wx.Bitmap(g_util.resource_path("images" + g_util.slash() + "save_data.png")), "")

        self.main_bar.EnableButton(wxID_RIBBONEDITRESTORE, False)
        self.main_bar.EnableButton(wxID_RIBBONEDITSAVE, False)

        #------------------------------------------------------------------------------
        edit_panel = RB.RibbonPanel(editPage, wx.ID_ANY, "Edit Functions", wx.NullBitmap, wx.DefaultPosition,
                                    wx.DefaultSize, RB.RIBBON_PANEL_NO_AUTO_MINIMISE)
        self.edit_bar = RB.RibbonButtonBar(edit_panel)
        self.edit_bar.AddSimpleButton(wxID_RIBBONEDITFILTER, "Filter Points",
                                      wx.Bitmap(g_util.resource_path("images" + g_util.slash() + "filter_list.png")),
                                      "")
        self.edit_bar.AddSimpleButton(wxID_RIBBONEDITRESETFILTER, "Reset Selection",
                                      wx.Bitmap(g_util.resource_path("images" + g_util.slash() + "undo.png")),
                                      "")
        self.edit_bar.AddSimpleButton(wxID_RIBBONEDITCHGVALUE, "Change Value",
                                      wx.Bitmap(g_util.resource_path("images" + g_util.slash() + "edit_view.png")), "")
        self.edit_bar.AddSimpleButton(wxID_RIBBONEDITINTEROPOLATE, "Interpolate",
                                      wx.Bitmap(g_util.resource_path("images" + g_util.slash() + "interpolate.png")),
                                      "")
        self.edit_bar.AddSimpleButton(wxID_RIBBONEDITLINFILTER, "Linear Drift",
                                      wx.Bitmap(g_util.resource_path("images" + g_util.slash() + "lin_drift.png")), "")
        self.edit_bar.AddSimpleButton(wxID_RIBBONEDITFLAG, "Flag",
                                      wx.Bitmap(g_util.resource_path("images" + g_util.slash() + "flag.png")), "")
        self.edit_bar.AddSimpleButton(wxID_RIBBONEDITADDPOINT, "Add Point",
                                      wx.Bitmap(g_util.resource_path("images" + g_util.slash() + "add.png")), "")
        self.edit_bar.AddSimpleButton(wxID_RIBBONEDITDELPOINT, "Delete Point",
                                      wx.Bitmap(g_util.resource_path("images" + g_util.slash() + "delete.png")), "")
        self.edit_bar.AddSimpleButton(wxID_RIBBONEDITRECORD, "Record",
                                      bitmap=wx.Bitmap(g_util.resource_path("images" + g_util.slash() + "record.png")),
                                      help_string="", kind=0x4)

        self.edit_bar.EnableButton(wxID_RIBBONEDITFILTER, False)
        self.edit_bar.EnableButton(wxID_RIBBONEDITCHGVALUE, False)
        self.edit_bar.EnableButton(wxID_RIBBONEDITINTEROPOLATE, False)
        self.edit_bar.EnableButton(wxID_RIBBONEDITLINFILTER, False)
        self.edit_bar.EnableButton(wxID_RIBBONEDITFLAG, False)
        self.edit_bar.EnableButton(wxID_RIBBONEDITADDPOINT, False)
        self.edit_bar.EnableButton(wxID_RIBBONEDITDELPOINT, False)
        self.edit_bar.EnableButton(wxID_RIBBONEDITRECORD, False)

        #-------------------------------------------------------------------------------

        viewPage = RB.RibbonPage(self, wx.ID_ANY, "View",
                                 wx.Bitmap(g_util.resource_path("images" + g_util.slash() + "blank.png")))

        view_panel = RB.RibbonPanel(viewPage, wx.ID_ANY, "Tools", wx.NullBitmap, wx.DefaultPosition,
                                    wx.DefaultSize, RB.RIBBON_PANEL_NO_AUTO_MINIMISE)
        view_bar = RB.RibbonButtonBar(view_panel)
        view_bar.AddSimpleButton(wxID_RIBBONVIEWPLOT, "Plot",
                                 wx.Bitmap(g_util.resource_path("images" + g_util.slash() + "line_chart.png")), "")
        view_bar.AddSimpleButton(wxID_RIBBONVIEWTABLE, "Table",
                                 wx.Bitmap(g_util.resource_path("images" + g_util.slash() + "table.png")), "")
        view_bar.AddSimpleButton(wxID_RIBBONVIEWSERIES, "Series Selector",
                                 wx.Bitmap(g_util.resource_path("images" + g_util.slash() + "bitmap_editor.png")), "")
        view_bar.AddSimpleButton(wxID_RIBBONVIEWCONSOLE, "Python Console",
                                 wx.Bitmap(g_util.resource_path("images" + g_util.slash() + "window_command_line.png")),
                                 "")
        view_bar.AddSimpleButton(wxID_RIBBONVIEWSCRIPT, "PythonScript",
                                 wx.Bitmap(g_util.resource_path("images" + g_util.slash() + "script.png")), "")

        self.CurrPage = 1
        self.SetActivePageByIndex(self.CurrPage)

        self.bindEvents()
        self.initPubSub()



    def __init__(self, parent, id, name):
        self.parent = parent
        self._init_ctrls(parent)

    def bindEvents(self):
        ###Docking Window Selection
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.onDocking, id=wxID_RIBBONVIEWTABLE)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.onDocking, id=wxID_RIBBONVIEWSERIES)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.onDocking, id=wxID_RIBBONVIEWPLOT)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.onDocking, id=wxID_RIBBONVIEWCONSOLE)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.onDocking, id=wxID_RIBBONVIEWSCRIPT)

        ###Plot type Selection
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.onPlotSelection, id=wxID_RIBBONPLOTTIMESERIES)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.onPlotSelection, id=wxID_RIBBONPLOTPROB)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.onPlotSelection, id=wxID_RIBBONPLOTBOX)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.onPlotSelection, id=wxID_RIBBONPLOTHIST)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.onPlotSelection, id=wxID_RIBBONPLOTSUMMARY)

        ###Dropdownbox events
        self.Bind(RB.EVT_RIBBONBUTTONBAR_DROPDOWN_CLICKED, self.onPlotTypeDropdown, id=wxID_RIBBONPLOTTSTYPE)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_DROPDOWN_CLICKED, self.onBoxTypeDropdown, id=wxID_RIBBONPLOTBOXTYPE)
        self.Bind(wx.EVT_SPINCTRL, self.onBinChanged, id=wxID_FRAME1SPINCTRL1)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.onShowLegend, id=wxID_RIBBONPLOTTSLEGEND)

        ###date changed
        #self.Bind(wx.EVT_DATE_CHANGED, self.onDateChanged, id=wxID_ENDDPDATE)
        #self.Bind(wx.EVT_DATE_CHANGED, self.onDateChanged, id=wxID_STARTDPDATE)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.onFullDate, id=wxID_RIBBONPLOTDATEFULL)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.onDateChanged, id = wxID_RIBBONPLOTDATEAPPLY)

        ###Add event  to edit tab
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.onExecuteScript, id=wxID_RIBBONEDITSCRIPTEXECUTE)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.onEditSeries, id=wxID_RIBBONEDITSERIES)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.onRestore, id=wxID_RIBBONEDITRESTORE)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.onSave, id=wxID_RIBBONEDITSAVE)

        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.onEditFilter, id=wxID_RIBBONEDITFILTER)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.onResetFilter, id = wxID_RIBBONEDITRESETFILTER)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.onEditChangeValue, id=wxID_RIBBONEDITCHGVALUE)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.onEditInterpolate, id=wxID_RIBBONEDITINTEROPOLATE)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.onEditFlag, id=wxID_RIBBONEDITFLAG)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.onEditAddPoint, id=wxID_RIBBONEDITADDPOINT)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.onEditDelPoint, id=wxID_RIBBONEDITDELPOINT)

        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.onRecord, id=wxID_RIBBONEDITRECORD)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.onLineDrift, id=wxID_RIBBONEDITLINFILTER)

        self.edit_bar.EnableButton(wxID_RIBBONEDITLINFILTER, False)

        ###Ribbon Event
        self.Bind(RB.EVT_RIBBONBAR_PAGE_CHANGED, self.onFileMenu, id=wxID_PANEL1)

    def initPubSub(self):
        Publisher.subscribe(self.toggleEditButtons, "EnableEditButtons")
        Publisher.subscribe(self.enableButtons, "EnablePlotButtons")
        Publisher.subscribe(self.resetDateRange, "resetdate")
        #Publisher.subscribe(self.updateSeriesCurrentDateTime, "updateSeriesCurrentDateTime")

    def onFileMenu(self, event):
        if not self.GetActivePage() == 0:
            self.CurrPage = self.GetActivePage()

        if self.GetActivePage() == 0:
            #reset activepage to original
            self.SetActivePageByIndex(self.CurrPage)
            menu = wx.Menu()
            self.Bind(wx.EVT_MENU, self.onChangeDBConfig, menu.Append(wx.ID_ANY, "Change DB Configuration"))
            self.Bind(wx.EVT_MENU, self.onClose, menu.Append(wx.ID_ANY, "Close"))

            self.PopupMenu(menu, wx.Point(50, 25))
        event.Skip()

    def onFullDate(self, event):
        Publisher.sendMessage("onDateFull")

    def onDateChanged(self, event):

        date=self.dpStartDate.GetValue()
        startDate = datetime.datetime(date.Year, date.Month + 1, date.Day, 0, 0, 0)
        date=self.dpEndDate.GetValue()
        endDate = datetime.datetime(date.Year, date.Month + 1, date.Day, 0, 0, 0)

        # check conditions
        logger.debug("startDate: %s" % (startDate))
        logger.debug("endDate: %s" % (endDate))

        if startDate.date() <= endDate.date():
            endDate = endDate.replace(hour=11, minute=59, second=59)
        else:
            startDate = startDate.replace(hour=11, minute=59, second=59)

        Publisher.sendMessage("onDateChanged", startDate=startDate, endDate=endDate)
        event.Skip()

    def resetDateRange(self, startDate, endDate):
        start = wx.DateTimeFromDMY(startDate.day, startDate.month - 1, startDate.year)
        end = wx.DateTimeFromDMY(endDate.day, endDate.month - 1, endDate.year)
        self.dpEndDate.SetRange(start, end)
        self.dpStartDate.SetRange(start, end)
        #self.dpEndDate.SetValue(end)
        #self.dpStartDate.SetValue(start)

    def onResetFilter(self, event):
        recordService=self.parent.getRecordService()
        recordService.reset_filter()
        Publisher.sendMessage("changeSelection", sellist=recordService.get_filter_list(), datetime_list=None)
        Publisher.sendMessage("changeTableSelection", sellist=recordService.get_filter_list(), datetime_list=None)


    def onLineDrift(self, event):
        lin_drift = frmLinearDrift(self, self.parent.getRecordService())
        lin_drift.ShowModal()
        event.Skip()

    def onRecord(self, event):
        record_service = self.parent.getRecordService()
        record_service.toggle_record()
        if event.IsChecked():
            panedet = self.parent._mgr.GetPane(self.parent.txtPythonScript)
            if not panedet.IsShown():
                panedet.Show(show=True)

            script = self.parent.txtPythonScript
            script.OnNew(event)
            record_service.write_header()

        event.Skip()

    def onSave(self, event):
        # send  db connection inof to wizard
        # get site, Variable and Source from current dataset

        savewiz = wizSave.wizSave(self, self.parent.getDBService(), self.parent.getRecordService())
        event.Skip()

    def onEditFilter(self, event):
        logger.debug("Entered!")
        data_filter = frmDataFilter(self, self.parent.getRecordService())
        data_filter.ShowModal()
        data_filter.Destroy()
        event.Skip()

    def onEditChangeValue(self, event):
        change_value = frmChangeValue(self, self.parent.getRecordService())
        change_value.ShowModal()
        event.Skip()

    def onEditInterpolate(self, event):
        self.parent.getRecordService().interpolate()
        Publisher.sendMessage(("updateValues"), event=event)
        event.Skip()

    def onEditFlag(self, event):
        add_flag = frmFlagValues(self)
        val = add_flag.ShowModal()
        logger.debug("FLAG Value: %s, type: %s" % (val, type(val)))
        if val == 5101:#wx.ID_OK:
            self.parent.getRecordService().flag(add_flag.GetValue())
            Publisher.sendMessage(("updateValues"), event=event)
        add_flag.Destroy()
        event.Skip()

    def onEditAddPoint(self, event):
        add_value = frmAddPoint(self, self.parent.getRecordService())
        add_value.ShowModal()
        Publisher.sendMessage(("updateValues"), event=event)
        event.Skip()

    def onEditDelPoint(self, event):
        numPoints=len(self.parent.getRecordService().get_filtered_points())
        val = wx.MessageBox("You have chosen to delete the %s selected points.\nDo you want to continue?"% numPoints,
                               'Deleting Points',
                               wx.YES_NO|wx.ICON_QUESTION)
        if val == 2:#wx.ID_YES:
            self.parent.getRecordService().delete_points()
            Publisher.sendMessage(("updateValues"), event=event)
        event.Skip()

    def onRestore(self, event):
        self.parent.getRecordService().restore()
        Publisher.sendMessage(("updateValues"), event=event)
        event.Skip()

    def onPushEdit(self):
        print ""

    def onEditSeries(self, event=None):
        logger.debug(dir(event))

        if event.IsChecked():
            Publisher.sendMessage(("selectEdit"), event=event)

            #self.parent.addEdit()
        else:
            Publisher.sendMessage(("stopEdit"), event=event)
            #self.parent.stopEdit()
        if True:
            event.Checked=False
            event.Skip()

    def onBinChanged(self, event):
        Publisher.sendMessage(("onNumBins"), numBins=event.Selection)
        event.Skip()

    def onShowLegend(self, event):
        Publisher.sendMessage(("onShowLegend"), event=event, isVisible=event.IsChecked())
        event.Skip()

    def onClose(self, event):
        Publisher.sendMessage(("onClose"), event=event)
        event.Skip()

    def onChangeDBConfig(self, event):
        Publisher.sendMessage(("change.dbConfig"), event=event)
        self.CurrPage = 1
        self.SetActivePageByIndex(self.CurrPage)
        event.Skip()

    def onExecuteScript(self, event):
        Publisher.sendMessage(("execute.script"), event=event)
        event.Skip()

    def onBoxTypeDropdown(self, event):
        menu = wx.Menu()
        self.Bind(wx.EVT_MENU, self.onBoxMonthly, menu.Append(wx.ID_ANY, "Monthly"))
        self.Bind(wx.EVT_MENU, self.onBoxYearly, menu.Append(wx.ID_ANY, "Yearly"))
        self.Bind(wx.EVT_MENU, self.onBoxSeasonal, menu.Append(wx.ID_ANY, "Seasonal"))
        self.Bind(wx.EVT_MENU, self.onBoxOverall, menu.Append(wx.ID_ANY, "Overall"))

        event.PopupMenu(menu)
        event.Skip()

    def onBoxMonthly(self, event):
        Publisher.sendMessage(("box.Monthly"), str=event)
        event.Skip()

    def onBoxYearly(self, event):
        Publisher.sendMessage(("box.Yearly"), str=event)
        event.Skip()

    def onBoxSeasonal(self, event):
        Publisher.sendMessage(("box.Seasonal"), str=event)
        event.Skip()

    def onBoxOverall(self, event):
        Publisher.sendMessage(("box.Overall"), str=event)
        event.Skip()

    def onPlotTypeDropdown(self, event):
        menu = wx.Menu()
        self.Bind(wx.EVT_MENU, self.onPlotTypeLine, menu.Append(wx.ID_ANY, "Line"))
        self.Bind(wx.EVT_MENU, self.onPlotTypePoint, menu.Append(wx.ID_ANY, "Point"))
        self.Bind(wx.EVT_MENU, self.onPlotTypeBoth, menu.Append(wx.ID_ANY, "Both"))

        event.PopupMenu(menu)
        event.Skip()

    def onPlotTypeLine(self, event):
        Publisher.sendMessage(("onPlotType"), event=event, ptype="line")
        event.Skip()

    def onPlotTypePoint(self, event):
        Publisher.sendMessage(("onPlotType"), event=event, ptype="point")
        event.Skip()

    def onPlotTypeBoth(self, event):
        Publisher.sendMessage(("onPlotType"), event=event, ptype="both")
        event.Skip()

    def onPlotSelection(self, event):
        if event.Id == wxID_RIBBONPLOTTIMESERIES:
            value = 0
        elif event.Id == wxID_RIBBONPLOTPROB:
            value = 1
        elif event.Id == wxID_RIBBONPLOTHIST:
            value = 2
        elif event.Id == wxID_RIBBONPLOTBOX:
            value = 3
        elif event.Id == wxID_RIBBONPLOTSUMMARY:
            value = 4
        # TODO fix case where the plot enables the buttons without checking if series is actually selected
        self.enableButtons(value, True)
        Publisher.sendMessage(("select.Plot"), value=value)
        event.Skip()

    def onDocking(self, event):

        if event.Id == wxID_RIBBONVIEWSCRIPT:
            value = "Script"
        elif event.Id == wxID_RIBBONVIEWCONSOLE:
            value = "Console"
        elif event.Id == wxID_RIBBONVIEWSERIES:
            value = "Selector"
        elif event.Id == wxID_RIBBONVIEWTABLE:
            value = "Table"
        elif event.Id == wxID_RIBBONVIEWPLOT:
            value = "Plot"

        Publisher.sendMessage(("adjust.Docking"), value=value)
        event.Skip()

    def enableDateSelection(self, isActive):
        self.dateTime_buttonbar.EnableButton(wxID_RIBBONPLOTDATEFULL, isActive)
        self.dateTime_buttonbar.EnableButton(wxID_RIBBONPLOTDATEAPPLY, isActive)
        self.dpEndDate.Enabled = isActive
        self.dpStartDate.Enabled = isActive

    def enableButtons(self, plot, isActive):

        if not isActive:
            self.PlotsOptions_bar.EnableButton(wxID_RIBBONPLOTTSTYPE, False)
            self.PlotsOptions_bar.EnableButton(wxID_RIBBONPLOTTSLEGEND, False)
            self.PlotsOptions_bar.EnableButton(wxID_RIBBONPLOTBOXTYPE, False)
            self.spnBins.Enabled = False
            self.enableDateSelection(False)

        ##tims series or probability
        elif plot == 0 or plot == 1:
            self.PlotsOptions_bar.EnableButton(wxID_RIBBONPLOTTSTYPE, True)
            self.PlotsOptions_bar.EnableButton(wxID_RIBBONPLOTTSLEGEND, True)
            self.PlotsOptions_bar.EnableButton(wxID_RIBBONPLOTBOXTYPE, False)
            self.spnBins.Enabled = False
            self.enableDateSelection( True)

        ##HIstogram
        elif plot == 2:
            self.PlotsOptions_bar.EnableButton(wxID_RIBBONPLOTTSTYPE, False)
            self.PlotsOptions_bar.EnableButton(wxID_RIBBONPLOTTSLEGEND, False)
            self.PlotsOptions_bar.EnableButton(wxID_RIBBONPLOTBOXTYPE, False)
            self.spnBins.Enabled = True
            self.enableDateSelection(True)

        ##Box Plot
        elif plot == 3:
            self.PlotsOptions_bar.EnableButton(wxID_RIBBONPLOTTSTYPE, False)
            self.PlotsOptions_bar.EnableButton(wxID_RIBBONPLOTTSLEGEND, False)
            self.PlotsOptions_bar.EnableButton(wxID_RIBBONPLOTBOXTYPE, True)
            self.spnBins.Enabled = False
            self.enableDateSelection(True)

        #Summary
        elif plot == 4:
            self.PlotsOptions_bar.EnableButton(wxID_RIBBONPLOTTSTYPE, False)
            self.PlotsOptions_bar.EnableButton(wxID_RIBBONPLOTTSLEGEND, False)
            self.PlotsOptions_bar.EnableButton(wxID_RIBBONPLOTBOXTYPE, False)
            self.spnBins.Enabled = False
            self.enableDateSelection(True)


    # TODO change states when points are selected rather than all at once
    def toggleEditButtons(self, state):

        # edit when series is selected for editing
        self.main_bar.EnableButton(wxID_RIBBONEDITRESTORE, state)
        self.main_bar.EnableButton(wxID_RIBBONEDITSAVE, state)
        self.edit_bar.EnableButton(wxID_RIBBONEDITFILTER, state)

        # when points are selected
        self.edit_bar.EnableButton(wxID_RIBBONEDITLINFILTER, state)
        self.edit_bar.EnableButton(wxID_RIBBONEDITCHGVALUE, state)
        self.edit_bar.EnableButton(wxID_RIBBONEDITINTEROPOLATE, state)
        self.edit_bar.EnableButton(wxID_RIBBONEDITFLAG, state)
        self.edit_bar.EnableButton(wxID_RIBBONEDITADDPOINT, state)
        self.edit_bar.EnableButton(wxID_RIBBONEDITDELPOINT, state)
        self.edit_bar.EnableButton(wxID_RIBBONEDITRECORD, state)

        self.enableDateSelection(not(state))
