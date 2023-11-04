from collections import OrderedDict

import datetime

import wx
import wx.adv
import wx.lib.agw.ribbon as RB
from wx.lib.pubsub import pub as Publisher
from odmtools.common.exceptions import EmptySelection

from odmtools.controller.frmAddPoints import AddPoints

from odmtools.controller.frmDataFilters import frmDataFilter
from odmtools.controller.frmChangeValue import frmChangeValue
from frmFlagValues import frmFlagValues
from odmtools.controller.frmLinearDrift import frmLinearDrift
from odmtools.controller.frmAbout import frmAbout
from odmtools.controller.frmGapFill import frmGapFill
import wizSave
from odmtools.common.icons import magicwand
from odmtools.common.icons import *
import pandas as pd

# # Enable logging
import logging

# from odmtools.common.logger import LoggerTool
#
# tool = LoggerTool()
# logger = tool.setupLogger(__name__, __name__ + '.log', 'w', logging.DEBUG)
logger = logging.getLogger('main')

[wxID_PANEL1, wxID_RIBBONPLOTTIMESERIES, wxID_RIBBONPLOTPROB, wxID_RIBBONPLOTHIST, wxID_RIBBONPLOTBOX,
 wxID_RIBBONPLOTSUMMARY, wxID_RIBBONPLOTTSTYPE, wxID_RIBBONPLOTTSCOLOR, wxID_RIBBONPLOTTSLEGEND, wxID_RIBBONPLOTBOXTYPE,
 wxID_RIBBONPLOTHISTTYPE, wxID_RIBBONPLOTHISTBIN, wxID_RIBBONPLOTDATEEND, wxID_RIBBONPLOTDATEREFRESH,
 wxID_RIBBONPLOTDATEFULL, wxID_RIBBONEDITSERIES, wxID_RIBBONEDITDERIVE, wxID_RIBBONEDITRESTORE, wxID_RIBBONEDITSAVE,
 wxID_RIBBONEDITCHGVALUE, wxID_RIBBONEDITINTEROPOLATE, wxID_RIBBONEDITFLAG, wxID_RIBBONEDITADDPOINT,
 wxID_RIBBONEDITDELPOINT, wxID_RIBBONEDITSCRIPTEXECUTE, wxID_RIBBONEDITSCRIPTOPEN, wxID_RIBBONEDITSCRIPTNEW,
 wxID_RIBBONEDITSCRIPTSAVE, wxID_RIBBONVIEWPLOT, wxID_RIBBONVIEWTABLE, wxID_RIBBONVIEWSERIES, wxID_RIBBONVIEWCONSOLE,
 wxID_RIBBONVIEWSCRIPT, wxID_RIBBONPLOTBLANKBTN, wxID_FileMenu, wxID_STARTDPDATE, wxID_ENDDPDATE, wxID_FRAME1SPINCTRL1,
 wxID_RIBBONEDITFILTER, wxID_RIBBONEDITRECORD, wxID_RIBBONEDITLINFILTER, wxID_RIBBONPLOTDATEAPPLY,
 wxID_RIBBONEDITRESETFILTER, wxID_RIBBONRECORDNEW, wxID_RIBBONRECORDOPEN, wxID_RIBBONRECORDSAVE, wxID_GAPFILL] = [
    wx.NewId() for
    _init_ctrls in
    range(47)]


## #################################
## Build Menu and Toolbar 
## #################################

class mnuRibbon(RB.RibbonBar):
    def _init_ctrls(self, prnt):
        RB.RibbonBar.__init__(self, name='ribbon', parent=prnt, id=wxID_PANEL1)
        # self.SetArtProvider(RB.RibbonMSWArtProvider())
        self.SetArtProvider(RB.RibbonAUIArtProvider())
        self.SetFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.NORMAL, False, u'Tahoma'))

        fileMenu = RB.RibbonPage(self, wxID_FileMenu, "File")

        # ----PlotMenu-------------
        home = RB.RibbonPage(self, wx.ID_ANY, "Plot")

        # ------Plot Type ---------------------------------------------------------------------------

        plot_panel = RB.RibbonPanel(home, wx.ID_ANY, "Plots", wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize,
                                    RB.RIBBON_PANEL_NO_AUTO_MINIMISE)
        self.plots_bar = RB.RibbonButtonBar(plot_panel, wx.ID_ANY)
        self.plots_bar.AddSimpleButton(wxID_RIBBONPLOTTIMESERIES, "Time Series", tsa_icon.GetBitmap(), "")
        self.plots_bar.AddSimpleButton(wxID_RIBBONPLOTPROB, "Exceedance Frequency", probability.GetBitmap(), "")
        self.plots_bar.AddSimpleButton(wxID_RIBBONPLOTHIST, "Histogram", histogram.GetBitmap(), "")
        self.plots_bar.AddSimpleButton(wxID_RIBBONPLOTBOX, "Box/Whisker", box_whisker.GetBitmap(), "")
        self.plots_bar.AddSimpleButton(wxID_RIBBONPLOTSUMMARY, "Summary", summary.GetBitmap(), "")

        # -- PLOT OPTIONS-----------------------------------------------------------------------------
        PlotOptions_panel = RB.RibbonPanel(home, wx.ID_ANY, "Plot Options", wx.NullBitmap, wx.DefaultPosition,
                                           wx.DefaultSize, RB.RIBBON_PANEL_NO_AUTO_MINIMISE)
        self.PlotsOptions_bar = RB.RibbonButtonBar(PlotOptions_panel, wx.ID_ANY)

        self.PlotsOptions_bar.AddDropdownButton(wxID_RIBBONPLOTTSTYPE, "Plot Type", plot_type.GetBitmap(), "")

        self.PlotsOptions_bar.AddSimpleButton(wxID_RIBBONPLOTTSLEGEND, "Show Legend", legend.GetBitmap(),
                                              help_string="show legend on plot", kind=0x4)

        self.PlotsOptions_bar.AddSimpleButton(wxID_RIBBONPLOTBLANKBTN, "#Hist Bins", blank.GetBitmap(), "")

        self.PlotsOptions_bar.EnableButton(wxID_RIBBONPLOTBLANKBTN, False)

        self.spnBins = wx.SpinCtrl(id=wxID_FRAME1SPINCTRL1, initial=50, max=100, min=1, name='spnBins',
                                   parent=self.PlotsOptions_bar, pos=wx.Point(85, 7),  # without color button
                                   size=wx.Size(44, 25), style=wx.SP_ARROW_KEYS)
        self.spnBins.Enabled = False

        self.PlotsOptions_bar.AddDropdownButton(wxID_RIBBONPLOTBOXTYPE, "Box Whisker Type",
                                                box_whisker_type.GetBitmap(), "")

        self.PlotsOptions_bar.EnableButton(wxID_RIBBONPLOTTSTYPE, False)
        self.PlotsOptions_bar.EnableButton(wxID_RIBBONPLOTTSLEGEND, False)
        self.PlotsOptions_bar.EnableButton(wxID_RIBBONPLOTBOXTYPE, False)

        dateTime_panel = RB.RibbonPanel(home, wx.ID_ANY, "Date Time", wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize,
                                        RB.RIBBON_PANEL_NO_AUTO_MINIMISE)

        self.dateTime_buttonbar = RB.RibbonButtonBar(dateTime_panel)

        self.dateTime_buttonbar.AddSimpleButton(wxID_RIBBONPLOTBLANKBTN, "", blank.GetBitmap(), "")
        self.dateTime_buttonbar.AddSimpleButton(wxID_RIBBONPLOTBLANKBTN, "", blank.GetBitmap(), "")
        self.dateTime_buttonbar.AddSimpleButton(wxID_RIBBONPLOTBLANKBTN, "", blank.GetBitmap(), "")
        self.dateTime_buttonbar.EnableButton(wxID_RIBBONPLOTBLANKBTN, False)

        self.dpStartDate = wx.adv.DatePickerCtrl(id=wxID_STARTDPDATE, name=u'dpStartDate', parent=self.dateTime_buttonbar,
                                             pos=wx.Point(5, 8), size=wx.Size(120, 24), style=wx.adv.DP_DROPDOWN)

        self.dpStartDate.SetToolTipString(u'Start Date')

        self.dpEndDate = wx.adv.DatePickerCtrl(id=wxID_ENDDPDATE, name=u'dpEndDate', parent=self.dateTime_buttonbar,
                                           pos=wx.Point(5, 40), size=wx.Size(120, 24), style=wx.adv.DP_DROPDOWN)
        self.dpEndDate.SetToolTipString(u'End Date')

        self.dateTime_buttonbar.AddSimpleButton(wxID_RIBBONPLOTDATEAPPLY, "Apply", date_setting.GetBitmap(), "")

        self.dateTime_buttonbar.AddSimpleButton(wxID_RIBBONPLOTDATEFULL, "Full Date Range", full_date_range.GetBitmap(),
                                                "")

        self.dateTime_buttonbar.EnableButton(wxID_RIBBONPLOTDATEFULL, False)
        self.dateTime_buttonbar.EnableButton(wxID_RIBBONPLOTDATEAPPLY, False)
        self.dpEndDate.Enabled = False
        self.dpStartDate.Enabled = False

        # -------------------------------------------------------------------------------
        editPage = RB.RibbonPage(self, wx.ID_ANY, "Edit")

        main_panel = RB.RibbonPanel(editPage, wx.ID_ANY, "Main", wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize,
                                    RB.RIBBON_PANEL_NO_AUTO_MINIMISE)
        self.main_bar = RB.RibbonButtonBar(main_panel)
        self.editbutton = self.main_bar.AddSimpleButton(wxID_RIBBONEDITSERIES, "Edit Series", bitmap=edit.GetBitmap(),
                                                        help_string="",
                                                        kind=0x4)  # kind sets the button to be a True or False

        self.main_bar.AddSimpleButton(wxID_RIBBONEDITRESTORE, "Restore Series", restore.GetBitmap(), "")
        self.main_bar.AddSimpleButton(wxID_RIBBONEDITSAVE, "Save", save_data.GetBitmap(), "")

        self.main_bar.EnableButton(wxID_RIBBONEDITRESTORE, False)
        self.main_bar.EnableButton(wxID_RIBBONEDITSAVE, False)

        # ------------------------------------------------------------------------------
        edit_panel = RB.RibbonPanel(editPage, wx.ID_ANY, "Edit Functions", wx.NullBitmap, wx.DefaultPosition,
                                    wx.DefaultSize, RB.RIBBON_PANEL_NO_AUTO_MINIMISE)
        self.edit_bar = RB.RibbonButtonBar(edit_panel)
        self.edit_bar.AddSimpleButton(wxID_RIBBONEDITFILTER, "Filter Points", filter_list.GetBitmap(), "")
        self.edit_bar.AddSimpleButton(wxID_RIBBONEDITRESETFILTER, "Reset Selection", Undo.GetBitmap(), "")
        self.edit_bar.AddSimpleButton(wxID_RIBBONEDITCHGVALUE, "Change Value", edit_view.GetBitmap(), "")
        self.edit_bar.AddSimpleButton(wxID_RIBBONEDITINTEROPOLATE, "Interpolate", interpolate.GetBitmap(), "")
        self.edit_bar.AddSimpleButton(wxID_RIBBONEDITLINFILTER, "Linear Drift", lin_drift.GetBitmap(), "")
        self.edit_bar.AddSimpleButton(wxID_RIBBONEDITFLAG, "Flag", flag.GetBitmap(), "")
        self.edit_bar.AddSimpleButton(wxID_RIBBONEDITADDPOINT, "Add Point", add.GetBitmap(), "")
        self.edit_bar.AddSimpleButton(wxID_RIBBONEDITDELPOINT, "Delete Point", delete.GetBitmap(), "")
        self.edit_bar.AddSimpleButton(wxID_GAPFILL, "Fill Gap", magicwand.GetBitmap(), "")

        self.edit_bar.EnableButton(wxID_RIBBONEDITFILTER, False)
        self.edit_bar.EnableButton(wxID_RIBBONEDITCHGVALUE, False)
        self.edit_bar.EnableButton(wxID_RIBBONEDITRESETFILTER, False)
        self.edit_bar.EnableButton(wxID_RIBBONEDITINTEROPOLATE, False)
        self.edit_bar.EnableButton(wxID_RIBBONEDITLINFILTER, False)
        self.edit_bar.EnableButton(wxID_RIBBONEDITFLAG, False)
        self.edit_bar.EnableButton(wxID_RIBBONEDITADDPOINT, False)
        self.edit_bar.EnableButton(wxID_RIBBONEDITDELPOINT, False)
        self.edit_bar.EnableButton(wxID_GAPFILL, False)

        self.record_panel = RB.RibbonPanel(editPage, wx.ID_ANY, "Recording Options", wx.NullBitmap, wx.DefaultPosition,
                                           wx.DefaultSize, RB.RIBBON_PANEL_NO_AUTO_MINIMISE)

        self.record_bar = RB.RibbonButtonBar(self.record_panel)
        self.record_bar.AddSimpleButton(wxID_RIBBONRECORDNEW, "New Script", newscript.GetBitmap(), "")
        self.record_bar.AddSimpleButton(wxID_RIBBONRECORDOPEN, "Open Script", openscript.GetBitmap(), "")
        self.record_bar.AddSimpleButton(wxID_RIBBONRECORDSAVE, "Save Script", savescript.GetBitmap(), "")

        self.record_bar.EnableButton(wxID_RIBBONRECORDNEW, False)
        self.record_bar.EnableButton(wxID_RIBBONRECORDOPEN, False)
        self.record_bar.EnableButton(wxID_RIBBONRECORDSAVE, False)

        # -------------------------------------------------------------------------------

        viewPage = RB.RibbonPage(self, wx.ID_ANY, "View")

        view_panel = RB.RibbonPanel(viewPage, wx.ID_ANY, "Tools", wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize,
                                    RB.RIBBON_PANEL_NO_AUTO_MINIMISE)
        view_bar = RB.RibbonButtonBar(view_panel)
        view_bar.AddSimpleButton(wxID_RIBBONVIEWPLOT, "Plot", line_chart.GetBitmap(), "")
        view_bar.AddSimpleButton(wxID_RIBBONVIEWTABLE, "Table", table.GetBitmap(), "")
        view_bar.AddSimpleButton(wxID_RIBBONVIEWSERIES, "Series Selector", bitmap_editor.GetBitmap(), "")
        view_bar.AddSimpleButton(wxID_RIBBONVIEWCONSOLE, "Python Console", window_command_line.GetBitmap(), "")
        view_bar.AddSimpleButton(wxID_RIBBONVIEWSCRIPT, "PythonScript", script.GetBitmap(), "")

        self.scriptPanel = RB.RibbonPanel(viewPage, wx.ID_ANY, "Script Options", wx.NullBitmap, wx.DefaultPosition,
                                          wx.DefaultSize, RB.RIBBON_PANEL_NO_AUTO_MINIMISE)

        self.scriptBar = RB.RibbonButtonBar(self.scriptPanel)
        self.scriptBar.AddSimpleButton(wxID_RIBBONRECORDNEW, "New Script", newscript.GetBitmap(), "")
        self.scriptBar.AddSimpleButton(wxID_RIBBONRECORDOPEN, "Open Script", openscript.GetBitmap(), "")
        self.scriptBar.AddSimpleButton(wxID_RIBBONRECORDSAVE, "Save Script", savescript.GetBitmap(), "")
        self.scriptPanel.Hide()

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
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.onFullDate, id=wxID_RIBBONPLOTDATEFULL)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.onDateChanged, id=wxID_RIBBONPLOTDATEAPPLY)

        ###Add event  to edit tab
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.onExecuteScript, id=wxID_RIBBONEDITSCRIPTEXECUTE)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.onEditSeries, id=wxID_RIBBONEDITSERIES)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.onRestore, id=wxID_RIBBONEDITRESTORE)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.onSave, id=wxID_RIBBONEDITSAVE)

        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.onEditFilter, id=wxID_RIBBONEDITFILTER)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.onResetFilter, id=wxID_RIBBONEDITRESETFILTER)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.onEditChangeValue, id=wxID_RIBBONEDITCHGVALUE)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.onEditInterpolate, id=wxID_RIBBONEDITINTEROPOLATE)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.onEditFlag, id=wxID_RIBBONEDITFLAG)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.onEditAddPoint, id=wxID_RIBBONEDITADDPOINT)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.onEditDelPoint, id=wxID_RIBBONEDITDELPOINT)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.onGapFill, id=wxID_GAPFILL)

        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.onRecordNew, id=wxID_RIBBONRECORDNEW)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.onRecordOpen, id=wxID_RIBBONRECORDOPEN)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.onRecordSave, id=wxID_RIBBONRECORDSAVE)

        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.onLineDrift, id=wxID_RIBBONEDITLINFILTER)

        self.edit_bar.EnableButton(wxID_RIBBONEDITLINFILTER, False)

        ###Ribbon Event
        self.Bind(RB.EVT_RIBBONBAR_PAGE_CHANGED, self.onFileMenu, id=wxID_PANEL1)

    def initPubSub(self):
        Publisher.subscribe(self.toggleEditButtons, "EnableEditButtons")
        Publisher.subscribe(self.enableButtons, "EnablePlotButtons")
        Publisher.subscribe(self.resetDateRange, "resetdate")
        Publisher.subscribe(self.onToggleEdit, "toggleEdit")
        Publisher.subscribe(self.setEdit, "setEdit")
        # Publisher.subscribe(self.updateSeriesCurrentDateTime, "updateSeriesCurrentDateTime")

    def onFileMenu(self, event):
        if not self.GetActivePage() == 0:
            self.CurrPage = self.GetActivePage()

        if self.GetActivePage() == 0:
            # reset activepage to original
            self.SetActivePageByIndex(self.CurrPage)
            menu = wx.Menu()
            self.Bind(wx.EVT_MENU, self.onChangeDBConfig, menu.Append(wx.ID_ANY, "Change DB Configuration"))
            self.Bind(wx.EVT_MENU, self.onAbout, menu.Append(wx.ID_ANY, "About"))
            self.Bind(wx.EVT_MENU, self.onClose, menu.Append(wx.ID_ANY, "Close"))

            self.PopupMenu(menu, wx.Point(50, 25))
        event.Skip()

    def onFullDate(self, event):
        Publisher.sendMessage("onDateFull")

    def onDateChanged(self, event):

        date = self.dpStartDate.GetValue()
        startDate = datetime.datetime(date.Year, date.Month + 1, date.Day, 0, 0, 0)
        date = self.dpEndDate.GetValue()
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

    def resetDateRange(self, startDate, endDate, currStart=None, currEnd=None):
        maxStart = _pydate2wxdate(startDate)
        maxEnd = _pydate2wxdate(endDate)

        self.dpStartDate.SetRange(maxStart, maxEnd)
        if currStart:
            self.dpStartDate.SetValue(_pydate2wxdate(currStart))
        else:
            self.dpEndDate.SetValue(self.maxStart)

        self.dpEndDate.SetRange(maxStart, maxEnd)
        if currEnd:
            self.dpEndDate.SetValue(_pydate2wxdate(currEnd))
        else:
            self.dpEndDate.SetValue(self.maxEnd)

    def onResetFilter(self, event):
        recordService = self.parent.getRecordService()
        recordService.reset_filter()

    def isEmptySelection(self, dataframe):
        if isinstance(dataframe, pd.DataFrame):
            if dataframe.empty:
                raise EmptySelection
        else:
            if not dataframe:
                raise EmptySelection

    # ###################################
    #   Linear Drift Correction
    # ###################################

    def onLineDrift(self, event):
        dataframe = self.parent.getRecordService().get_filtered_points()
        try:
            self.isEmptySelection(dataframe)
        except EmptySelection:
            val = wx.MessageBox("You have no points selected, "
                                "Please select points before applying a Linear Drift Correction",
                                'Linear Drift Correction', wx.OK | wx.ICON_WARNING)
            return

        lin_drift = frmLinearDrift(self.parent, self.parent.getRecordService())
        lin_drift.CenterOnParent()
        lin_drift.ShowModal()
        lin_drift.Destroy()
        event.Skip()

    # ###################################
    #   Record Script
    # ###################################
    def onRecordNew(self, event):
        panedet = self.parent._mgr.GetPane(self.parent.txtPythonScript)
        if not panedet.IsShown():
            panedet.Show(show=True)
        script = self.parent.txtPythonScript
        script.OnNew(event)

    def onRecordOpen(self, event):
        script = self.parent.txtPythonScript
        panedet = self.parent._mgr.GetPane(self.parent.txtPythonScript)
        if not panedet.IsShown():
            panedet.Show(show=True)
        script.OnOpen(event)

    def onRecordSave(self, event):
        script = self.parent.txtPythonScript
        script.OnSaveAs(event)
        # pass

    # ###################################
    #   Save Wizard
    # ###################################
    def onSave(self, event):
        # send  db connection info to wizard
        # get site, Variable and Source from current dataset

        wiz = wizSave.wizSave(self.parent, self.parent.getServiceManager(), self.parent.getRecordService())
        wiz.Close()
        event.Skip()

    # ###################################
    #   Data Filter
    # ###################################

    def onEditFilter(self, event):
        data_filter = frmDataFilter(self.parent, self.parent.getRecordService())

        if data_filter.Show() == wx.OK:
            print "OK"
            data_filter.Destroy()

        event.Skip()

    # ###################################
    #   Change Value
    # ###################################

    def onEditChangeValue(self, event):
        change_value = frmChangeValue(self.parent, self.parent.getRecordService())
        change_value.CenterOnParent()
        change_value.ShowModal()
        change_value.Destroy()
        event.Skip()

    # ###################################
    #   Interpolate
    # ###################################
    def onEditInterpolate(self, event):

        dataframe = self.parent.getRecordService().get_filtered_points()
        try:
            self.isEmptySelection(dataframe)
        except EmptySelection:
            val = wx.MessageBox("You have no points selected, Please select points before interpolating.",
                                'Interpolation', wx.OK | wx.ICON_EXCLAMATION, parent=self.parent)
            return

        val = wx.MessageBox(
            "You have chosen to interpolate the %s selected points.\nDo you want to continue?" % len(dataframe),
            'Interpolation', wx.YES_NO | wx.ICON_QUESTION | wx.CENTRE, parent=self.parent)
        if val == 2:  # wx.ID_YES:
            self.parent.getRecordService().interpolate()

        event.Skip()

    # ###################################
    #   Flag
    # ###################################
    def onEditFlag(self, event):

        serviceManager = self.parent.getDBService()
        series_service = serviceManager.get_series_service()
        qualifierChoices = OrderedDict((x.code + '-' + x.description, x.id) for x in series_service.get_all_qualifiers()
                                       if x.code and x.description)
        add_flag = frmFlagValues(self.parent, series_service, qualifierChoices)
        val = add_flag.ShowModal()

        if val == wx.ID_OK:
            logger.debug("FLAG Value: %s, type: %s" % (val, type(val)))
            self.parent.getRecordService().flag(add_flag.GetValue())
        add_flag.Destroy()
        event.Skip()

    # ###################################
    #   Add Point
    # ###################################
    def onEditAddPoint(self, event):
        recordService = self.parent.getRecordService()
        serviceManager = self.parent.getServiceManager()

        addPoint = AddPoints(self.parent, serviceManager=serviceManager, recordService=recordService)
        addPoint.Center()
        addPoint.ShowModal()

        event.Skip()

    # ###################################
    #   Gap fill
    # ###################################
    def onGapFill(self, event):

        gap_fill = frmGapFill(self.parent, self.parent.getRecordService())

        if gap_fill.Show() == wx.OK:
            gap_fill.Destroy()

        event.Skip()

    # ###################################
    #   Delete Point
    # ###################################
    def onEditDelPoint(self, event):
        dataframe = self.parent.getRecordService().get_filtered_points()
        try:
            self.isEmptySelection(dataframe)
        except EmptySelection:
            wx.MessageBox("There are no points to delete",
                          'Delete Points', wx.OK | wx.ICON_WARNING, parent=self.parent)
            return

        val = wx.MessageBox(
            "You have chosen to delete the %s selected points.\nDo you want to continue?" % len(dataframe),
            'Deleting Points', wx.YES_NO | wx.ICON_QUESTION, parent=self.parent)
        if val == 2:  # wx.ID_YES:
            self.parent.getRecordService().delete_points()
        event.Skip()

    def onRestore(self, event):
        self.parent.getRecordService().restore()
        event.Skip()

    def onToggleEdit(self, checked=True):
        self.main_bar.ToggleButton(self.editbutton.id, checked)

    def setEdit(self, isEdit):
        self.isEdit = isEdit

    def getEditStatus(self):
        try:
            return self.isEdit
        except:
            return None

    def onEditSeries(self, event=None):

        if event.IsChecked():
            Publisher.sendMessage("selectEdit", event=event)
            logging.debug("is editing: %s" % self.isEdit)

            if not self.isEdit:
                self.onToggleEdit(False)
        else:
            Publisher.sendMessage(("stopEdit"), event=event)


        event.Skip()

    def onBinChanged(self, event):
        Publisher.sendMessage(("onNumBins"), numBins=event.Selection)
        event.Skip()

    def onShowLegend(self, event):
        Publisher.sendMessage(("onShowLegend"), event=event, isVisible=event.IsChecked())
        event.Skip()

    def onAbout(self, event):

        frmAbout(self)
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
            ''' TODO add the ability to modify the script outside of editing...
            if self.scriptPanel.IsShown():
                self.scriptPanel.Hide()
            else:
                self.scriptPanel.Show()
            '''
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
            self.enableDateSelection(True)

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

        # Summary
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
        self.edit_bar.EnableButton(wxID_RIBBONEDITRESETFILTER, state)
        self.edit_bar.EnableButton(wxID_RIBBONEDITCHGVALUE, state)
        self.edit_bar.EnableButton(wxID_RIBBONEDITINTEROPOLATE, state)
        self.edit_bar.EnableButton(wxID_RIBBONEDITFLAG, state)
        self.edit_bar.EnableButton(wxID_RIBBONEDITADDPOINT, state)
        self.edit_bar.EnableButton(wxID_RIBBONEDITDELPOINT, state)
        self.edit_bar.EnableButton(wxID_GAPFILL, state)

        self.record_bar.EnableButton(wxID_RIBBONRECORDOPEN, state)
        self.record_bar.EnableButton(wxID_RIBBONRECORDNEW, state)
        self.record_bar.EnableButton(wxID_RIBBONRECORDSAVE, state)

        self.enableDateSelection(not state)


def _pydate2wxdate(date):
    import datetime
    assert isinstance(date, (datetime.datetime, datetime.date))
    tt = date.timetuple()
    dmy = (tt[2], tt[1] - 1, tt[0])
    return wx.DateTimeFromDMY(*dmy)
