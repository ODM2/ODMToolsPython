#Boa:FramePanel:Panel1

import wx
import wx.lib.agw.ribbon as RB
from wx.lib.pubsub import pub as Publisher

import pnlDatePicker
import frmDataFilters
import frmChangeValue
import frmAddPoint
import frmFlagValues
import frmLinearDrift
import wizSave



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

def CreateBitmap(xpm):
    bmp = wx.Image(xpm, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
    return bmp

class mnuRibbon(RB.RibbonBar):

    def _init_ctrls(self, prnt):
        RB.RibbonBar.__init__(self,  name='ribbon', parent=prnt, id=wxID_PANEL1)#, agwStyle = RB.RIBBON_BAR_ALWAYS_SHOW_TABS)

        #self.GetArtProvider().SetColourScheme("GRAY","LIGHT GRAY","WHITE")
        self.SetArtProvider(RB.RibbonAUIArtProvider())
        self.SetFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, u'Tahoma'))
        fileMenu = RB.RibbonPage(self, wxID_FileMenu, "File", CreateBitmap("images\\3d graph.png"))

#----PlotMenu-------------
        #self.ribbon= RB.RibbonBar(parent=self, id=wx.ID_ANY, name ='ribbon')
        home = RB.RibbonPage(self, wx.ID_ANY, "Plot", CreateBitmap("images\\3d graph.png"))

  #------Plot Type ---------------------------------------------------------------------------

        plot_panel = RB.RibbonPanel(home, wx.ID_ANY, "Plots", wx.NullBitmap, wx.DefaultPosition,
                                        wx.DefaultSize, RB.RIBBON_PANEL_NO_AUTO_MINIMISE)
        plots_bar = RB.RibbonButtonBar(plot_panel, wx.ID_ANY)
        plots_bar.AddSimpleButton(wxID_RIBBONPLOTTIMESERIES, "Time Series",
                                CreateBitmap("images\\TSA_icon.png"), "")
        plots_bar.AddSimpleButton(wxID_RIBBONPLOTPROB, "Probablity",
                                CreateBitmap("images\\Probability.png"), "")
        plots_bar.AddSimpleButton(wxID_RIBBONPLOTHIST, "Histogram",
                                CreateBitmap("images\\Histogram.png"), "")
        plots_bar.AddSimpleButton(wxID_RIBBONPLOTBOX, "Box/Whisker",
                                CreateBitmap("images\\BoxWisker.png"), "")
        plots_bar.AddSimpleButton(wxID_RIBBONPLOTSUMMARY, "Summary",
                                CreateBitmap("images\\Summary.png"), "")

#-- PLOT OPTIONS-----------------------------------------------------------------------------
        PlotOptions_panel = RB.RibbonPanel(home, wx.ID_ANY, "Plot Options", wx.NullBitmap, wx.DefaultPosition,
                                        wx.DefaultSize, RB.RIBBON_PANEL_NO_AUTO_MINIMISE)
        self.PlotsOptions_bar = RB.RibbonButtonBar(PlotOptions_panel, wx.ID_ANY)

        self.PlotsOptions_bar.AddDropdownButton(wxID_RIBBONPLOTTSTYPE, "Plot Type",
                                CreateBitmap("images\\PlotType.png"), "")

        # self.PlotsOptions_bar.AddSimpleButton(wxID_RIBBONPLOTTSCOLOR, "Color Setting",
        #                         CreateBitmap("images\\ColorSetting.png"), "")
        self.PlotsOptions_bar.AddSimpleButton(wxID_RIBBONPLOTTSLEGEND, "Show Legend",
                                CreateBitmap("images\\Legend.png"), help_string="show legend on plot", kind = 0x4)


        self.PlotsOptions_bar.AddSimpleButton( wxID_RIBBONPLOTDATESTART, "# Hist Bins" ,CreateBitmap("images\\Blank.png"), "") #,wx.Size(100, 21))
        self.PlotsOptions_bar.EnableButton(wxID_RIBBONPLOTDATESTART, False)

        self.spnBins = wx.SpinCtrl(id=wxID_FRAME1SPINCTRL1, initial=50,
              max=100, min=1, name='spnBins', parent=self.PlotsOptions_bar,
              #pos=wx.Point(126, 6), #with color button included
              pos= wx.Point(84,6), #without color button
              size=wx.Size(43, 25),style=wx.SP_ARROW_KEYS)
        # self.spnBins.SetValue(50)
        self.spnBins.Enabled = False


        self.PlotsOptions_bar.AddDropdownButton(wxID_RIBBONPLOTBOXTYPE, "Box Whisker Type",
                                CreateBitmap("images\\BoxWhiskerType.png"), "")

        self.PlotsOptions_bar.EnableButton(wxID_RIBBONPLOTTSTYPE, False)
        # self.PlotsOptions_bar.EnableButton(wxID_RIBBONPLOTTSCOLOR, False)
        self.PlotsOptions_bar.EnableButton(wxID_RIBBONPLOTTSLEGEND, False)
        self.PlotsOptions_bar.EnableButton(wxID_RIBBONPLOTBOXTYPE, False)

######################TEMPORARILY COMMENTED OUT

        # self.PlotsOptions_bar.AddDropdownButton(wxID_RIBBONPLOTHISTTYPE, "Histogram Type",
        #                         CreateBitmap("images\\HisType.png"), "")
        # self.PlotsOptions_bar.AddDropdownButton(wxID_RIBBONPLOTHISTBIN, "Binning Algorithms",
        #                         CreateBitmap("images\\Binning.png"), "")

#-------------------------------------------------------------------------------





        dateTime_panel = RB.RibbonPanel(home, wx.ID_ANY, "Date Time", wx.NullBitmap, wx.DefaultPosition,
                                        wx.DefaultSize, RB.RIBBON_PANEL_NO_AUTO_MINIMISE)
        #radio1 = wx.RadioButton( dummy_2, -1, " Radio1 ", style =wx.RB_GROUP )

        # dateTime_toolbar= RB.RibbonToolBar(dateTime_panel)
        dateTime_buttonbar = RB.RibbonButtonBar(dateTime_panel)

        # dateTime_buttonbar.AddHybridButton( wxID_RIBBONPLOTDATESTART, "Start" ,CreateBitmap("images\\Calendar.png"), "") #,wx.Size(100, 21))
        # dateTime_buttonbar.AddHybridButton( wxID_RIBBONPLOTDATEEND, "End" ,CreateBitmap("images\\Calendar.png"), "") #,wx.Size(100, 21))
         # dateTime_buttonbar.AddTool(wxID_RIBBONPLOTDATESTART,  CreateBitmap("images\\Calendar.png"), kind=pnlDatePicker.pnlDatePicker, client_data=[wxID_RIBBONPLOTDATESTART, "startDate", "Start Date", wx.DateTimeFromDMY(30, 10, 2010, 0, 0, 0)])


         ###Filler buttons to allow enough room for start and end date drop down menus

        dateTime_buttonbar.AddSimpleButton( wxID_RIBBONPLOTDATESTART, "" ,CreateBitmap("images\\Blank.png"), "") #,wx.Size(100, 21))
        dateTime_buttonbar.AddSimpleButton( wxID_RIBBONPLOTDATESTART, "" ,CreateBitmap("images\\Blank.png"), "") #,wx.Size(100, 21))
        dateTime_buttonbar.AddSimpleButton( wxID_RIBBONPLOTDATESTART, "" ,CreateBitmap("images\\Blank.png"), "") #,wx.Size(100, 21))
        dateTime_buttonbar.EnableButton(wxID_RIBBONPLOTDATESTART, False)



        # self.staticText2 = wx.StaticText(id=wx.ID_ANY,
        #       label=u'Start Date:', name='staticText2', parent=dateTime_buttonbar,
        #       pos=wx.Point(0, 16), size=wx.Size(55, 13), style=0)
        self.dpStartDate = wx.DatePickerCtrl(id=wxID_STARTDPDATE, name=u'dpStartDate',
              parent=dateTime_buttonbar, pos=wx.Point(5, 8), size=wx.Size(120, 24),
              style=wx.DP_DROPDOWN)
        self.dpStartDate.SetValue(wx.DateTimeFromDMY(16, 1, 2008, 0, 0, 0))#wx.DateTimeFromDMY(30, 10, 2010, 0, 0, 0)
        self.dpStartDate.SetLabel(repr(wx.DateTimeFromDMY(16, 1, 2008, 0, 0, 0)))#.strftime("%m-%d-%Y"))#"%Y-%m-%d'"")#'11/30/2010'
        self.dpStartDate.SetToolTipString(u'Start Date')


        # self.staticText1 = wx.StaticText(id=wx.ID_ANY,
        #       label=u'End Date:', name='staticText1', parent=dateTime_buttonbar,
        #       pos=wx.Point(0, 48), size=wx.Size(49, 13), style=0)

        self.dpEndDate = wx.DatePickerCtrl(id=wxID_ENDDPDATE, name=u'dpEndDate',
              parent=dateTime_buttonbar, pos=wx.Point(5, 40), size=wx.Size(120, 24),
              style=wx.DP_DROPDOWN)
        self.dpEndDate.SetValue(wx.DateTimeFromDMY(01, 04, 2008, 0, 0, 0))#wx.DateTimeFromDMY(30, 10, 2010, 0, 0, 0)
        self.dpEndDate.SetLabel(repr(wx.DateTimeFromDMY(1, 04, 2008, 0, 0, 0)))#.strftime("%m-%d-%Y"))#"%Y-%m-%d'"")#'11/30/2010'
        self.dpEndDate.SetToolTipString(u'End Date')


        dateTime_buttonbar.AddSimpleButton(wxID_RIBBONPLOTDATEREFRESH, "Refresh",
                                CreateBitmap("images\\DateSetting.png"), "")
        dateTime_buttonbar.AddSimpleButton(wxID_RIBBONPLOTDATEFULL, "Full Date Range",
                                CreateBitmap("images\\FullDateRange.png"), "")






#-------------------------------------------------------------------------------
        editPage = RB.RibbonPage(self, wx.ID_ANY, "Edit", CreateBitmap("images\\Brush.png"))

        main_panel = RB.RibbonPanel(editPage, wx.ID_ANY, "Main", wx.NullBitmap, wx.DefaultPosition,
                                        wx.DefaultSize, RB.RIBBON_PANEL_NO_AUTO_MINIMISE)
        self.main_bar = RB.RibbonButtonBar(main_panel)
        self.main_bar.AddSimpleButton(wxID_RIBBONEDITSERIES, "Edit Series",
                                bitmap=CreateBitmap("images\\Edit (2).png"), help_string="", kind = 0x4)

        # self.main_bar.AddButton(wxID_RIBBONEDITSERIES, "Edit Series",
        #                                bitmap=CreateBitmap("images\\Edit (2).png"), help_string="", kind = 0x4)

        # self.main_bar.AddSimpleButton(wxID_RIBBONSTOPEDITSERIES, "Stop Editing",
        #                         CreateBitmap("images\\StopEdit.png"), "")
        # main_bar.AddSimpleButton(wxID_RIBBONEDITDERIVE, "Derive New Series",
        #                        CreateBitmap("images\\DeriveNewSeries.png"), "")
        self.main_bar.AddSimpleButton(wxID_RIBBONEDITRESTORE, "Restore",
                                CreateBitmap("images\\Restore.png"), "")
        self.main_bar.AddSimpleButton(wxID_RIBBONEDITSAVE, "Save",
                                CreateBitmap("images\\Save Data.png"), "")


        self.main_bar.EnableButton(wxID_RIBBONEDITRESTORE, False)
        self.main_bar.EnableButton(wxID_RIBBONEDITSAVE, False)
        # self.main_bar.EnableButton(wxID_RIBBONSTOPEDITSERIES, False)

 #------------------------------------------------------------------------------
        edit_panel = RB.RibbonPanel( editPage, wx.ID_ANY, "Edit Functions" , wx.NullBitmap, wx.DefaultPosition,
                                        wx.DefaultSize, RB.RIBBON_PANEL_NO_AUTO_MINIMISE)
        self.edit_bar= RB.RibbonButtonBar(edit_panel)
        self.edit_bar.AddSimpleButton(wxID_RIBBONEDITFILTER, "Filter Points",
                                CreateBitmap("images\\Filter List.png"), "")
        self.edit_bar.AddSimpleButton(wxID_RIBBONEDITCHGVALUE, "Change Value",
                                CreateBitmap("images\\EditView_icon.png"), "")
        self.edit_bar.AddSimpleButton(wxID_RIBBONEDITINTEROPOLATE, "Interpolate",
                                CreateBitmap("images\\Interpolate.png"), "")
        self.edit_bar.AddSimpleButton(wxID_RIBBONEDITLINFILTER, "Linear Drift",
                                CreateBitmap("images\\LinDrift.png"), "")
        self.edit_bar.AddSimpleButton(wxID_RIBBONEDITFLAG, "Flag",
                                CreateBitmap("images\\Flag.png"), "")
        self.edit_bar.AddSimpleButton(wxID_RIBBONEDITADDPOINT, "Add Point",
                                CreateBitmap("images\\Add (2).png"), "")
        self.edit_bar.AddSimpleButton(wxID_RIBBONEDITDELPOINT, "Delete Point",
                                CreateBitmap("images\\Delete (3).png"), "")
        self.edit_bar.AddSimpleButton(wxID_RIBBONEDITRECORD, "Record",
                                bitmap= CreateBitmap("images\\Record.png"), help_string="", kind = 0x4)

        self.edit_bar.EnableButton(wxID_RIBBONEDITFILTER, False)
        self.edit_bar.EnableButton(wxID_RIBBONEDITCHGVALUE, False)
        self.edit_bar.EnableButton(wxID_RIBBONEDITINTEROPOLATE, False)
        self.edit_bar.EnableButton(wxID_RIBBONEDITLINFILTER, False)
        self.edit_bar.EnableButton(wxID_RIBBONEDITFLAG, False)
        self.edit_bar.EnableButton(wxID_RIBBONEDITADDPOINT, False)
        self.edit_bar.EnableButton(wxID_RIBBONEDITDELPOINT, False)
        self.edit_bar.EnableButton(wxID_RIBBONEDITRECORD, False)

#-------------------------------------------------------------------------------
        # script_panel = RB.RibbonPanel(editPage, wx.ID_ANY, "Script", wx.NullBitmap, wx.DefaultPosition,
        #                                 wx.DefaultSize, RB.RIBBON_PANEL_NO_AUTO_MINIMISE)
        # script_bar = RB.RibbonButtonBar(script_panel)
        # script_bar.AddSimpleButton(wxID_RIBBONEDITSCRIPTEXECUTE, "Execute",
        #                         CreateBitmap("images\\Window Enter.png"), "")
        # script_bar.AddSimpleButton(wxID_RIBBONEDITSCRIPTOPEN, "Open",
        #                         CreateBitmap("images\\Open file.png"), "")
        # script_bar.AddSimpleButton(wxID_RIBBONEDITSCRIPTNEW, "New",
        #                         CreateBitmap("images\\File New.png"), "")
        # script_bar.AddHybridButton(wxID_RIBBONEDITSCRIPTSAVE, "Save",
        #                         CreateBitmap("images\\Save (2).png"), "")

#-------------------------------------------------------------------------------
        viewPage = RB.RibbonPage(self, wx.ID_ANY, "View", CreateBitmap("images\\Brush.png"))
        view_panel = RB.RibbonPanel( viewPage, wx.ID_ANY, "Tools" , wx.NullBitmap, wx.DefaultPosition,
                                        wx.DefaultSize, RB.RIBBON_PANEL_NO_AUTO_MINIMISE)
        view_bar= RB.RibbonButtonBar(view_panel)
        view_bar.AddSimpleButton(wxID_RIBBONVIEWPLOT, "Plot",
                                CreateBitmap("images\\Line Chart.png"), "")
        view_bar.AddSimpleButton(wxID_RIBBONVIEWTABLE, "Table",
                                CreateBitmap("images\\Table.png"), "")
        view_bar.AddSimpleButton(wxID_RIBBONVIEWSERIES, "Series Selector",
                                CreateBitmap("images\\Bitmap editor.png"), "")
        view_bar.AddSimpleButton(wxID_RIBBONVIEWCONSOLE, "Python Console",
                                CreateBitmap("images\\Window Command Line.png"), "")
        view_bar.AddSimpleButton(wxID_RIBBONVIEWSCRIPT, "PythonScript",
                                CreateBitmap("images\\Script.png"), "")
        self.CurrPage = 1
        self.SetActivePageByIndex(self.CurrPage)

        self.BindEvents()
        Publisher.subscribe(self.toggleEditButtons, ("edit.EnableButtons"))


    def __init__(self, parent, id, name):
        self.parent=parent
        self._init_ctrls(parent)

    def BindEvents(self):
        #self.Bind(wx.EVT_MENU, self.test, None, 1)
        #self.Bind(wx.EVT_BUTTON, self.OnBtnAdvButton, id = )

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

        ###date changed
        self.Bind(wx.EVT_DATE_CHANGED, self.oneDateChanged, id = wxID_ENDDPDATE)
        self.Bind(wx.EVT_DATE_CHANGED, self.onsDateChanged, id = wxID_STARTDPDATE)
        self.Bind(wx.EVT_SPINCTRL, self.OnNumBins, id=wxID_FRAME1SPINCTRL1)


        ###Add event  to editab
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED,  self.onExecuteScript, id= wxID_RIBBONEDITSCRIPTEXECUTE)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED,  self.OnEditSeries, id= wxID_RIBBONEDITSERIES)
        # self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED,  self.OnStopEdit, id= wxID_RIBBONSTOPEDITSERIES)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED,  self.OnRestore, id= wxID_RIBBONEDITRESTORE)
        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED,  self.OnSave, id= wxID_RIBBONEDITSAVE)

        self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.OnShowLegend, id=wxID_RIBBONPLOTTSLEGEND)
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
        # self.Bind(RB.EVT_RIBBONBAR_PAGE_CHANGED, self.OnFileMenutest, id=wxID_PANEL1)

        self.isLegendVisible = False;

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

        savewiz =wizSave.wizSave(self, self.parent.GetDBService(), self.parent.get_edit_metadata())
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

    # def OnStopEdit(self, event):
    #     # print type(self.parent), dir(self.parent)
    #     self.parent.stopEdit()

    def OnRestore(self, event):
        self.parent.getRecordService().restore()
        Publisher.sendMessage(("updateValues"), event=event)
        event.Skip()

    def OnEditSeries(self, event):
        # self.parent.
        if event.IsChecked():
            Publisher.sendMessage(("selectEdit"), event=event)
        else:
            self.parent.stopEdit()
        # Publisher.sendMessage(("selectEdit"), event=event)
        event.Skip()


    def OnNumBins(self, event):
        Publisher.sendMessage(("OnNumBins"), numBins=event.Selection)
        event.Skip()

    def OnShowLegend(self, event):
        if event.IsChecked():
            Publisher.sendMessage(("OnShowLegend"), event= event, isVisible=True)
        else:
            Publisher.sendMessage(("OnShowLegend"), event= event, isVisible=False)

        event.Skip()

        # Publisher.sendMessage(("OnShowLegend"), event= event, isVisible=self.isLegendVisible)
        # self.isLegendVisible = not self.isLegendVisible

    def oneDateChanged(self,event):
        # print dir(event)
        Publisher.sendMessage(("onDateChanged"), date=event.Date, time="end")
        event.Skip()

    def onsDateChanged(self,event):
        # print event.Date
        Publisher.sendMessage(("onDateChanged"), date=event.Date, time="start")
        event.Skip()

    # def OnFileMenutest(self, event):
    #     print dir(event)

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
        Publisher.sendMessage(("box.Monthly"), event=event)
        event.Skip()

    def OnBoxYearly(self, event):
        Publisher.sendMessage(("box.Yearly"), event=event)
        event.Skip()

    def OnBoxSeasonal(self, event):
        Publisher.sendMessage(("box.Seasonal"), event=event)
        event.Skip()

    def OnBoxOverall(self, event):
        Publisher.sendMessage(("box.Overall"), event=event)
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
            # self.PlotsOptions_bar.EnableButton(wxID_RIBBONPLOTTSCOLOR, True)
            self.PlotsOptions_bar.EnableButton(wxID_RIBBONPLOTTSLEGEND, True)
            self.PlotsOptions_bar.EnableButton(wxID_RIBBONPLOTBOXTYPE, False)
            self.spnBins.Enabled = False
        ##HIstogram
        elif plot == 2:
            self.PlotsOptions_bar.EnableButton(wxID_RIBBONPLOTTSTYPE, False)
            # self.PlotsOptions_bar.EnableButton(wxID_RIBBONPLOTTSCOLOR, False)
            self.PlotsOptions_bar.EnableButton(wxID_RIBBONPLOTTSLEGEND, False)
            self.PlotsOptions_bar.EnableButton(wxID_RIBBONPLOTBOXTYPE, False)
            self.spnBins.Enabled = True
        ##Box Plot
        elif plot == 3:
            self.PlotsOptions_bar.EnableButton(wxID_RIBBONPLOTTSTYPE, False)
            # self.PlotsOptions_bar.EnableButton(wxID_RIBBONPLOTTSCOLOR, False)
            self.PlotsOptions_bar.EnableButton(wxID_RIBBONPLOTTSLEGEND, False)
            self.PlotsOptions_bar.EnableButton(wxID_RIBBONPLOTBOXTYPE, True)
            self.spnBins.Enabled = False
         #Summary
        elif plot == 4:
            self.PlotsOptions_bar.EnableButton(wxID_RIBBONPLOTTSTYPE, False)
            # self.PlotsOptions_bar.EnableButton(wxID_RIBBONPLOTTSCOLOR, False)
            self.PlotsOptions_bar.EnableButton(wxID_RIBBONPLOTTSLEGEND, False)
            self.PlotsOptions_bar.EnableButton(wxID_RIBBONPLOTBOXTYPE, False)
            self.spnBins.Enabled = False


    def toggleEditButtons(self, state):
        self.main_bar.EnableButton(wxID_RIBBONEDITRESTORE, state)
        self.main_bar.EnableButton(wxID_RIBBONEDITSAVE, state)
        # self.main_bar.EnableButton(wxID_RIBBONEDITSERIES, not state)

        self.edit_bar.EnableButton(wxID_RIBBONEDITLINFILTER, state)
        self.edit_bar.EnableButton(wxID_RIBBONEDITFILTER, state)
        self.edit_bar.EnableButton(wxID_RIBBONEDITCHGVALUE, state)
        self.edit_bar.EnableButton(wxID_RIBBONEDITINTEROPOLATE, state)
        self.edit_bar.EnableButton(wxID_RIBBONEDITFLAG, state)
        self.edit_bar.EnableButton(wxID_RIBBONEDITADDPOINT, state)
        self.edit_bar.EnableButton(wxID_RIBBONEDITDELPOINT, state)
        self.edit_bar.EnableButton(wxID_RIBBONEDITRECORD, state)


##
##    def OnBtnAdvButton(self, event):
##        self.new = NewWindow(parent=None, id=-1)
##        self.new.Show()


