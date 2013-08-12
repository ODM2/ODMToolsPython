#Boa:FramePanel:Panel1

import wx
import wx.lib.agw.ribbon as RB
from wx.lib.pubsub import pub as Publisher
import datetime

import pnlDatePicker
import frmDataFilters
import frmChangeValue
import frmAddPoint
import frmFlagValues
import frmLinearDrift
import wizSave

import gui_utils



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
 wxID_RIBBONPLOTDATESTART, wxID_FileMenu, wxID_STARTDPDATE, wxID_ENDDPDATE,
 wxID_FRAME1SPINCTRL1, wxID_RIBBONEDITFILTER, wxID_RIBBONEDITRECORD,
 wxID_RIBBONEDITLINFILTER
 ] = [wx.NewId() for _init_ctrls in range(41)]

class mnuRibbon(RB.RibbonBar):

    def _init_ctrls(self, prnt):
        RB.RibbonBar.__init__(self,  name='ribbon', parent=prnt, id=wxID_PANEL1)
        self.SetArtProvider(RB.RibbonAUIArtProvider())
        self.SetFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, u'Tahoma'))
        fileMenu = RB.RibbonPage(self, wxID_FileMenu, "File", wx.Bitmap(gui_utils.get_base_dir() + "\\3d_graph.png"))

#----PlotMenu-------------
        home = RB.RibbonPage(self, wx.ID_ANY, "Plot", wx.Bitmap(gui_utils.get_base_dir() + "\\3d_graph.png"))

  #------Plot Type ---------------------------------------------------------------------------

        plot_panel = RB.RibbonPanel(home, wx.ID_ANY, "Plots", wx.NullBitmap, wx.DefaultPosition,
                                        wx.DefaultSize, RB.RIBBON_PANEL_NO_AUTO_MINIMISE)
        plots_bar = RB.RibbonButtonBar(plot_panel, wx.ID_ANY)
        plots_bar.AddSimpleButton(wxID_RIBBONPLOTTIMESERIES, "Time Series",
                                wx.Bitmap(gui_utils.get_base_dir() + "\\tsa_icon.png"), "")
        plots_bar.AddSimpleButton(wxID_RIBBONPLOTPROB, "Probablity",
                                wx.Bitmap(gui_utils.get_base_dir() + "\\probability.png"), "")
        plots_bar.AddSimpleButton(wxID_RIBBONPLOTHIST, "Histogram",
                                wx.Bitmap(gui_utils.get_base_dir() + "\\histogram.png"), "")
        plots_bar.AddSimpleButton(wxID_RIBBONPLOTBOX, "Box/Whisker",
                                wx.Bitmap(gui_utils.get_base_dir() + "\\box_whisker.png"), "")
        plots_bar.AddSimpleButton(wxID_RIBBONPLOTSUMMARY, "Summary",
                                wx.Bitmap(gui_utils.get_base_dir() + "\\summary.png"), "")

#-- PLOT OPTIONS-----------------------------------------------------------------------------
        PlotOptions_panel = RB.RibbonPanel(home, wx.ID_ANY, "Plot Options", wx.NullBitmap, wx.DefaultPosition,
                                        wx.DefaultSize, RB.RIBBON_PANEL_NO_AUTO_MINIMISE)
        self.PlotsOptions_bar = RB.RibbonButtonBar(PlotOptions_panel, wx.ID_ANY)

        self.PlotsOptions_bar.AddDropdownButton(wxID_RIBBONPLOTTSTYPE, "Plot Type",
                                wx.Bitmap(gui_utils.get_base_dir() + "\\plot_type.png"), "")

        self.PlotsOptions_bar.AddSimpleButton(wxID_RIBBONPLOTTSLEGEND, "Show Legend",
                                wx.Bitmap(gui_utils.get_base_dir() + "\\legend.png"), help_string="show legend on plot", kind = 0x4)


        self.PlotsOptions_bar.AddSimpleButton( wxID_RIBBONPLOTDATESTART, "# Hist Bins", wx.Bitmap(gui_utils.get_base_dir() + "\\blank.png"), "")
        self.PlotsOptions_bar.EnableButton(wxID_RIBBONPLOTDATESTART, False)

        self.spnBins = wx.SpinCtrl(id=wxID_FRAME1SPINCTRL1, initial=50,
              max=100, min=1, name='spnBins', parent=self.PlotsOptions_bar,
              pos= wx.Point(84,6), #without color button
              size=wx.Size(43, 25),style=wx.SP_ARROW_KEYS)
        self.spnBins.Enabled = False


        self.PlotsOptions_bar.AddDropdownButton(wxID_RIBBONPLOTBOXTYPE, "Box Whisker Type",
                                wx.Bitmap(gui_utils.get_base_dir() + "\\box_whisker_type.png"), "")

        self.PlotsOptions_bar.EnableButton(wxID_RIBBONPLOTTSTYPE, False)
        self.PlotsOptions_bar.EnableButton(wxID_RIBBONPLOTTSLEGEND, False)
        self.PlotsOptions_bar.EnableButton(wxID_RIBBONPLOTBOXTYPE, False)




        dateTime_panel = RB.RibbonPanel(home, wx.ID_ANY, "Date Time", wx.NullBitmap, wx.DefaultPosition,
                                        wx.DefaultSize, RB.RIBBON_PANEL_NO_AUTO_MINIMISE)

        self.dateTime_buttonbar = RB.RibbonButtonBar(dateTime_panel)

        self.dateTime_buttonbar.AddSimpleButton( wxID_RIBBONPLOTDATESTART, "" ,wx.Bitmap(gui_utils.get_base_dir() + "\\blank.png"), "")
        self.dateTime_buttonbar.AddSimpleButton( wxID_RIBBONPLOTDATESTART, "" ,wx.Bitmap(gui_utils.get_base_dir() + "\\blank.png"), "")
        self.dateTime_buttonbar.AddSimpleButton( wxID_RIBBONPLOTDATESTART, "" ,wx.Bitmap(gui_utils.get_base_dir() + "\\blank.png"), "")
        self.dateTime_buttonbar.EnableButton(wxID_RIBBONPLOTDATESTART, False)

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


##        dateTime_buttonbar.AddSimpleButton(wxID_RIBBONPLOTDATEREFRESH, "Refresh",
##                                wx.Bitmap(gui_utils.get_base_dir() + "\\date_setting.png"), "")
        self.dateTime_buttonbar.AddSimpleButton(wxID_RIBBONPLOTDATEFULL, "Full Date Range",
                                wx.Bitmap(gui_utils.get_base_dir() + "\\full_date_range.png"), "")
        self.dateTime_buttonbar.EnableButton(wxID_RIBBONPLOTDATEFULL, False)
        self.dpEndDate.Enabled = False
        self.dpStartDate.Enabled= False






#-------------------------------------------------------------------------------
        editPage = RB.RibbonPage(self, wx.ID_ANY, "Edit", wx.Bitmap(gui_utils.get_base_dir() + "\\blank.png"))

        main_panel = RB.RibbonPanel(editPage, wx.ID_ANY, "Main", wx.NullBitmap, wx.DefaultPosition,
                                        wx.DefaultSize, RB.RIBBON_PANEL_NO_AUTO_MINIMISE)
        self.main_bar = RB.RibbonButtonBar(main_panel)
        self.main_bar.AddSimpleButton(wxID_RIBBONEDITSERIES, "Edit Series",
                                bitmap=wx.Bitmap(gui_utils.get_base_dir() + "\\edit.png"), help_string="", kind = 0x4)

        self.main_bar.AddSimpleButton(wxID_RIBBONEDITRESTORE, "Restore",
                                wx.Bitmap(gui_utils.get_base_dir() + "\\restore.png"), "")
        self.main_bar.AddSimpleButton(wxID_RIBBONEDITSAVE, "Save",
                                wx.Bitmap(gui_utils.get_base_dir() + "\\save_data.png"), "")


        self.main_bar.EnableButton(wxID_RIBBONEDITRESTORE, False)
        self.main_bar.EnableButton(wxID_RIBBONEDITSAVE, False)

 #------------------------------------------------------------------------------
        edit_panel = RB.RibbonPanel( editPage, wx.ID_ANY, "Edit Functions" , wx.NullBitmap, wx.DefaultPosition,
                                        wx.DefaultSize, RB.RIBBON_PANEL_NO_AUTO_MINIMISE)
        self.edit_bar= RB.RibbonButtonBar(edit_panel)
        self.edit_bar.AddSimpleButton(wxID_RIBBONEDITFILTER, "Filter Points",
                                wx.Bitmap(gui_utils.get_base_dir() + "\\filter_list.png"), "")
        self.edit_bar.AddSimpleButton(wxID_RIBBONEDITCHGVALUE, "Change Value",
                                wx.Bitmap(gui_utils.get_base_dir() + "\\edit_view.png"), "")
        self.edit_bar.AddSimpleButton(wxID_RIBBONEDITINTEROPOLATE, "Interpolate",
                                wx.Bitmap(gui_utils.get_base_dir() + "\\interpolate.png"), "")
        self.edit_bar.AddSimpleButton(wxID_RIBBONEDITLINFILTER, "Linear Drift",
                                wx.Bitmap(gui_utils.get_base_dir() + "\\lin_drift.png"), "")
        self.edit_bar.AddSimpleButton(wxID_RIBBONEDITFLAG, "Flag",
                                wx.Bitmap(gui_utils.get_base_dir() + "\\flag.png"), "")
        self.edit_bar.AddSimpleButton(wxID_RIBBONEDITADDPOINT, "Add Point",
                                wx.Bitmap(gui_utils.get_base_dir() + "\\add.png"), "")
        self.edit_bar.AddSimpleButton(wxID_RIBBONEDITDELPOINT, "Delete Point",
                                wx.Bitmap(gui_utils.get_base_dir() + "\\delete.png"), "")
        self.edit_bar.AddSimpleButton(wxID_RIBBONEDITRECORD, "Record",
                                bitmap= wx.Bitmap(gui_utils.get_base_dir() + "\\record.png"), help_string="", kind = 0x4)

        self.edit_bar.EnableButton(wxID_RIBBONEDITFILTER, False)
        self.edit_bar.EnableButton(wxID_RIBBONEDITCHGVALUE, False)
        self.edit_bar.EnableButton(wxID_RIBBONEDITINTEROPOLATE, False)
        self.edit_bar.EnableButton(wxID_RIBBONEDITLINFILTER, False)
        self.edit_bar.EnableButton(wxID_RIBBONEDITFLAG, False)
        self.edit_bar.EnableButton(wxID_RIBBONEDITADDPOINT, False)
        self.edit_bar.EnableButton(wxID_RIBBONEDITDELPOINT, False)
        self.edit_bar.EnableButton(wxID_RIBBONEDITRECORD, False)

#-------------------------------------------------------------------------------
        viewPage = RB.RibbonPage(self, wx.ID_ANY, "View", wx.Bitmap("images\\blank.png"))
        view_panel = RB.RibbonPanel( viewPage, wx.ID_ANY, "Tools" , wx.NullBitmap, wx.DefaultPosition,
                                        wx.DefaultSize, RB.RIBBON_PANEL_NO_AUTO_MINIMISE)
        view_bar= RB.RibbonButtonBar(view_panel)
        view_bar.AddSimpleButton(wxID_RIBBONVIEWPLOT, "Plot",
                                wx.Bitmap(gui_utils.get_base_dir() + "\\line_chart.png"), "")
        view_bar.AddSimpleButton(wxID_RIBBONVIEWTABLE, "Table",
                                wx.Bitmap(gui_utils.get_base_dir() + "\\table.png"), "")
        view_bar.AddSimpleButton(wxID_RIBBONVIEWSERIES, "Series Selector",
                                wx.Bitmap(gui_utils.get_base_dir() + "\\bitmap_editor.png"), "")
        view_bar.AddSimpleButton(wxID_RIBBONVIEWCONSOLE, "Python Console",
                                wx.Bitmap(gui_utils.get_base_dir() + "\\window_command_line.png"), "")
        view_bar.AddSimpleButton(wxID_RIBBONVIEWSCRIPT, "PythonScript",
                                wx.Bitmap(gui_utils.get_base_dir() + "\\script.png"), "")
        self.CurrPage = 1
        self.SetActivePageByIndex(self.CurrPage)

        self.BindEvents()
        Publisher.subscribe(self.toggleEditButtons, ("edit.EnableButtons"))
        Publisher.subscribe(self.resetDateRange, ("resetdate"))


    def __init__(self, parent, id, name):
        self.parent=parent
        self._init_ctrls(parent)

    def BindEvents(self):
        ###Docking Window Selection
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED,  self.onDocking, id=wxID_RIBBONVIEWTABLE)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED,  self.onDocking, id=wxID_RIBBONVIEWSERIES)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED,  self.onDocking, id=wxID_RIBBONVIEWPLOT)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED,  self.onDocking, id=wxID_RIBBONVIEWCONSOLE)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED,  self.onDocking, id=wxID_RIBBONVIEWSCRIPT)


        ###Plot type Selection
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED,  self.onPlotSelection, id=wxID_RIBBONPLOTTIMESERIES)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED,  self.onPlotSelection, id=wxID_RIBBONPLOTPROB)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED,  self.onPlotSelection, id=wxID_RIBBONPLOTBOX)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED,  self.onPlotSelection, id=wxID_RIBBONPLOTHIST)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED,  self.onPlotSelection, id=wxID_RIBBONPLOTSUMMARY)


        ###Dropdownbox events
        self.Bind(RB.EVT_RIBBONBUTTONBAR_DROPDOWN_CLICKED, self.OnPlotTypeDropdown, id=wxID_RIBBONPLOTTSTYPE)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_DROPDOWN_CLICKED, self.OnBoxTypeDropdown, id=wxID_RIBBONPLOTBOXTYPE)
        self.Bind(wx.EVT_SPINCTRL, self.OnNumBins, id=wxID_FRAME1SPINCTRL1)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.OnShowLegend, id=wxID_RIBBONPLOTTSLEGEND)

        ###date changed
        self.Bind(wx.EVT_DATE_CHANGED, self.oneDateChanged, id = wxID_ENDDPDATE)
        self.Bind(wx.EVT_DATE_CHANGED, self.onsDateChanged, id = wxID_STARTDPDATE)
##        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.OnChangeDate, id= wxID_RIBBONPLOTDATEREFRESH)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.OnFullDate, id= wxID_RIBBONPLOTDATEFULL)



        ###Add event  to editab
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED,  self.onExecuteScript, id= wxID_RIBBONEDITSCRIPTEXECUTE)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED,  self.OnEditSeries, id= wxID_RIBBONEDITSERIES)
        # self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED,  self.OnStopEdit, id= wxID_RIBBONSTOPEDITSERIES)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED,  self.OnRestore, id= wxID_RIBBONEDITRESTORE)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED,  self.OnSave, id= wxID_RIBBONEDITSAVE)



        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.OnEditFilter, id= wxID_RIBBONEDITFILTER)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.OnEditChangeValue, id= wxID_RIBBONEDITCHGVALUE)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.OnEditInterpolate, id= wxID_RIBBONEDITINTEROPOLATE)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.OnEditFlag, id= wxID_RIBBONEDITFLAG)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.OnEditAddPoint, id= wxID_RIBBONEDITADDPOINT)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.OnEditDelPoint, id= wxID_RIBBONEDITDELPOINT)

        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.OnRecord, id= wxID_RIBBONEDITRECORD)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.OnLineDrift, id= wxID_RIBBONEDITLINFILTER)

        self.edit_bar.EnableButton(wxID_RIBBONEDITLINFILTER, False)

        ###Ribbon Event
        self.Bind(RB.EVT_RIBBONBAR_PAGE_CHANGED, self.OnFileMenu, id=wxID_PANEL1)

##    def OnChangeDate(self, event):
##        print 'on change date'
#        Publisher.sendMessage(("onDateChanged"), date = ev)

    def OnFullDate(self, event):
        Publisher.sendMessage(("onDateChanged"), date=datetime.datetime.now(), time = "full")

    def oneDateChanged(self,event):
        # print dir(event)
        date=event.Date
        Publisher.sendMessage(("onDateChanged"), date= datetime.datetime(date.Year, date.Month+1, date.Day, 0, 0, 0), time="end")
        event.Skip()

    def onsDateChanged(self,event):
        # print event.Date
        date=event.date
        Publisher.sendMessage(("onDateChanged"), date= datetime.datetime(date.Year, date.Month+1, date.Day, 0, 0, 0), time="start")
        event.Skip()

    def resetDateRange(self, startDate, endDate):
        start=wx.DateTimeFromDMY(startDate.day, startDate.month-1, startDate.year)
        end =wx.DateTimeFromDMY(endDate.day, endDate.month-1, endDate.year)
        self.dpEndDate.SetRange(start, end)
        self.dpStartDate.SetRange(start, end)
        self.dpEndDate.SetValue(end)
        self.dpStartDate.SetValue(start)


    def OnLineDrift(self, event):
        lin_drift = frmLinearDrift.frmLinearDrift(self, self.parent.getRecordService())
        lin_drift.ShowModal()
        event.Skip()

    def OnRecord(self, event):
        record_service = self.parent.getRecordService()
        record_service.toggle_record()
        if event.IsChecked():
            panedet=self.parent._mgr.GetPane(self.parent.txtPythonScript)
            if not panedet.IsShown():
                panedet.Show(show=True)

            script = self.parent.txtPythonScript
            script.OnNew(event)
            record_service.write_header()

        event.Skip()

    def OnSave(self, event):
        # send  db connection inof to wizard
        # get site, Variable and Source from current dataset

        savewiz =wizSave.wizSave(self, self.parent.GetDBService(), self.parent.getRecordService())
        event.Skip()

    def OnEditFilter(self, event):
        data_filter = frmDataFilters.frmDataFilter(self, self.parent.getRecordService())
        self.filterlist = data_filter.ShowModal()
        data_filter.Destroy()
        event.Skip()

    def OnEditChangeValue(self, event):
        change_value=frmChangeValue.frmChangeValue(self, self.parent.getRecordService())
        change_value.ShowModal()
        event.Skip()

    def OnEditInterpolate(self, event):
        self.parent.getRecordService().interpolate()
        Publisher.sendMessage(("updateValues"), event=event)
        event.Skip()

    def OnEditFlag(self, event):
        add_flag= frmFlagValues.frmFlagValues(self)
        if add_flag.ShowModal() == wx.ID_OK:
            self.parent.getRecordService().flag(add_flag.GetValue())
            Publisher.sendMessage(("updateValues"), event = event)
        add_flag.Destroy()
        event.Skip()

    def OnEditAddPoint(self, event):
        add_value=frmAddPoint.frmAddPoint(self, self.parent.getRecordService())
        add_value.ShowModal()
        Publisher.sendMessage(("updateValues"), event=event)
        event.Skip()

    def OnEditDelPoint(self, event):
        self.parent.getRecordService().delete_points()
        Publisher.sendMessage(("updateValues"), event=event)
        event.Skip()

    def OnRestore(self, event):
        self.parent.getRecordService().restore()
        Publisher.sendMessage(("updateValues"), event=event)
        event.Skip()

    def OnEditSeries(self, event):
        if event.IsChecked():
            Publisher.sendMessage(("selectEdit"), event=event)
        else:
            self.parent.stopEdit()
        event.Skip()


    def OnNumBins(self, event):
        Publisher.sendMessage(("OnNumBins"), numBins=event.Selection)
        event.Skip()

    def OnShowLegend(self, event):
        Publisher.sendMessage(("OnShowLegend"), event = event, isVisible = event.IsChecked())
##        if event.IsChecked():
##            Publisher.sendMessage(("OnShowLegend"), event= event, isVisible=True)
##        else:
##            Publisher.sendMessage(("OnShowLegend"), event= event, isVisible=False)

        event.Skip()



    def OnFileMenu(self, event):

        if not self.GetActivePage()==0:
            self.CurrPage = self.GetActivePage()

        if self.GetActivePage()==0:
            #reset activepage to original
            self.SetActivePageByIndex(self.CurrPage)
            menu = wx.Menu()
            self.Bind(wx.EVT_MENU,  self.onChangeDBConfig, menu.Append(wx.ID_ANY, "Change DB Configuration"))
            self.Bind(wx.EVT_MENU, self.onClose, menu.Append(wx.ID_ANY, "Close"))

            self.PopupMenu(menu, wx.Point(50, 25))
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

    def OnBoxTypeDropdown(self, event):
        menu = wx.Menu()
        self.Bind(wx.EVT_MENU,  self.OnBoxMonthly, menu.Append(wx.ID_ANY, "Monthly") )
        self.Bind(wx.EVT_MENU,  self.OnBoxYearly, menu.Append(wx.ID_ANY, "Yearly"))
        self.Bind(wx.EVT_MENU,  self.OnBoxSeasonal, menu.Append(wx.ID_ANY, "Seasonal"))
        self.Bind(wx.EVT_MENU,  self.OnBoxOverall, menu.Append(wx.ID_ANY, "Overall"))

        event.PopupMenu(menu)
        event.Skip()

    def OnBoxMonthly(self, event):
        Publisher.sendMessage(("box.Monthly"), str=event)
        event.Skip()

    def OnBoxYearly(self, event):
        Publisher.sendMessage(("box.Yearly"), str=event)
        event.Skip()

    def OnBoxSeasonal(self, event):
        Publisher.sendMessage(("box.Seasonal"), str=event)
        event.Skip()

    def OnBoxOverall(self, event):
        Publisher.sendMessage(("box.Overall"), str=event)
        event.Skip()

    def OnPlotTypeDropdown(self, event):
        menu = wx.Menu()
        self.Bind(wx.EVT_MENU,  self.OnPlotTypeLine, menu.Append(wx.ID_ANY, "Line"))
        self.Bind(wx.EVT_MENU,  self.OnPlotTypePoint, menu.Append(wx.ID_ANY, "Point"))
        self.Bind(wx.EVT_MENU,  self.OnPlotTypeBoth, menu.Append(wx.ID_ANY, "Both"))

        event.PopupMenu(menu)
        event.Skip()

    def OnPlotTypeLine(self, event):
        Publisher.sendMessage(("onPlotType"), event=event, ptype="line")
        event.Skip()

    def OnPlotTypePoint(self, event):
        Publisher.sendMessage(("onPlotType"), event=event, ptype="point")
        event.Skip()

    def OnPlotTypeBoth(self, event):
        Publisher.sendMessage(("onPlotType"), event=event, ptype="both")
        event.Skip()

    def onPlotSelection(self, event):
        if event.Id == wxID_RIBBONPLOTTIMESERIES:
            value = 0
        elif event.Id ==wxID_RIBBONPLOTPROB:
            value= 1
        elif event.Id == wxID_RIBBONPLOTHIST:
            value=2
        elif event.Id == wxID_RIBBONPLOTBOX:
            value=3
        elif event.Id == wxID_RIBBONPLOTSUMMARY:
            value= 4
        self.enableButtons(value)
        Publisher.sendMessage(("select.Plot"), value=value)
        event.Skip()

    def onDocking(self, event):

        if event.Id == wxID_RIBBONVIEWSCRIPT:
            value = "Script"
        elif event.Id ==wxID_RIBBONVIEWCONSOLE:
            value= "Console"
        elif event.Id == wxID_RIBBONVIEWSERIES:
            value="Selector"
        elif event.Id == wxID_RIBBONVIEWTABLE:
            value="Table"
        elif event.Id == wxID_RIBBONVIEWPLOT:
            value= "Plot"

        Publisher.sendMessage(("adjust.Docking"), value=value)
        event.Skip()

    def enableButtons(self, plot):
        ##tims series or probability
        if plot == 0 or plot == 1:
            self.PlotsOptions_bar.EnableButton(wxID_RIBBONPLOTTSTYPE, True)
            self.PlotsOptions_bar.EnableButton(wxID_RIBBONPLOTTSLEGEND, True)
            self.PlotsOptions_bar.EnableButton(wxID_RIBBONPLOTBOXTYPE, False)
            self.dateTime_buttonbar.EnableButton(wxID_RIBBONPLOTDATEFULL, True)
            self.dpEndDate.Enabled = True
            self.dpStartDate.Enabled= True

        ##HIstogram
        elif plot == 2:
            self.PlotsOptions_bar.EnableButton(wxID_RIBBONPLOTTSTYPE, False)
            self.PlotsOptions_bar.EnableButton(wxID_RIBBONPLOTTSLEGEND, False)
            self.PlotsOptions_bar.EnableButton(wxID_RIBBONPLOTBOXTYPE, False)
            self.spnBins.Enabled = True
            self.dateTime_buttonbar.EnableButton(wxID_RIBBONPLOTDATEFULL, False)
            self.dpEndDate.Enabled = False
            self.dpStartDate.Enabled= False
        ##Box Plot
        elif plot == 3:
            self.PlotsOptions_bar.EnableButton(wxID_RIBBONPLOTTSTYPE, False)
            self.PlotsOptions_bar.EnableButton(wxID_RIBBONPLOTTSLEGEND, False)
            self.PlotsOptions_bar.EnableButton(wxID_RIBBONPLOTBOXTYPE, True)
            self.spnBins.Enabled = False
            self.dateTime_buttonbar.EnableButton(wxID_RIBBONPLOTDATEFULL, False)
            self.dpEndDate.Enabled = False
            self.dpStartDate.Enabled= False
         #Summary
        elif plot == 4:
            self.PlotsOptions_bar.EnableButton(wxID_RIBBONPLOTTSTYPE, False)
            self.PlotsOptions_bar.EnableButton(wxID_RIBBONPLOTTSLEGEND, False)
            self.PlotsOptions_bar.EnableButton(wxID_RIBBONPLOTBOXTYPE, False)
            self.spnBins.Enabled = False
            self.dateTime_buttonbar.EnableButton(wxID_RIBBONPLOTDATEFULL, False)
            self.dpEndDate.Enabled = False
            self.dpStartDate.Enabled= False


    def toggleEditButtons(self, state):
        self.main_bar.EnableButton(wxID_RIBBONEDITRESTORE, state)
        self.main_bar.EnableButton(wxID_RIBBONEDITSAVE, state)

        self.edit_bar.EnableButton(wxID_RIBBONEDITLINFILTER, state)
        self.edit_bar.EnableButton(wxID_RIBBONEDITFILTER, state)
        self.edit_bar.EnableButton(wxID_RIBBONEDITCHGVALUE, state)
        self.edit_bar.EnableButton(wxID_RIBBONEDITINTEROPOLATE, state)
        self.edit_bar.EnableButton(wxID_RIBBONEDITFLAG, state)
        self.edit_bar.EnableButton(wxID_RIBBONEDITADDPOINT, state)
        self.edit_bar.EnableButton(wxID_RIBBONEDITDELPOINT, state)
        self.edit_bar.EnableButton(wxID_RIBBONEDITRECORD, state)
