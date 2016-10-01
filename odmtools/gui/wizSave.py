# Boa:Wizard:wizSave

import wx
import wx.wizard as wiz

# import * from WizardPanels
from odmtools.controller import pageIntro, pageExisting
import pageMethod
import pageQCL
import pageVariable
import pageSummary

[wxID_PNLINTRO, wxID_PNLVARIABLE, wxID_PNLMETHOD, wxID_PNLQCL,
 wxID_PNLSUMMARY, wxID_WIZSAVE, wxID_PNLEXISTING,
] = [wx.NewId() for _init_ctrls in range(7)]

from wx.lib.pubsub import pub as Publisher
from odmtools.common.logger import LoggerTool
import logging

# tool = LoggerTool()
# logger = tool.setupLogger(__name__, __name__ + '.log', 'w', logging.DEBUG)
logger =logging.getLogger('main')


########################################################################
class QCLPage(wiz.WizardPageSimple):
    def __init__(self, parent, title, series_service, qcl):
        """Constructor"""
        wiz.WizardPageSimple.__init__(self, parent)

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = sizer
        self.SetSizer(sizer)
        self.qcl = qcl

        title = wx.StaticText(self, -1, title)
        title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        sizer.Add(title, 10, wx.ALIGN_CENTRE | wx.ALL, 5)
        sizer.Add(wx.StaticLine(self, -1), 5, wx.EXPAND | wx.ALL, 5)
        self.panel = pageQCL.pnlQCL(self, id=wxID_PNLQCL, name=u'pnlQCL',
                                    pos=wx.Point(536, 285), size=wx.Size(439, 357),
                                    style=wx.TAB_TRAVERSAL, ss=series_service, qcl=qcl)
        self.sizer.Add(self.panel, 85, wx.ALL, 5)

        self._init_data(self.panel.series_service)

    def _init_data(self, series):
        qcl = series.get_all_qcls()
        index = 0
        for q, i in zip(qcl, range(len(qcl))):
            num_items = self.panel.lstQCL.GetItemCount()
            self.panel.lstQCL.InsertStringItem(num_items, str(q.code))
            self.panel.lstQCL.SetStringItem(num_items, 1, str(q.definition))
            self.panel.lstQCL.SetStringItem(num_items, 2, str(q.explanation))
            self.panel.lstQCL.SetStringItem(num_items, 3, str(q.id))
            if q.code == self.qcl.code:
                index = i
        self.panel.lstQCL.Focus(index)
        self.panel.lstQCL.Select(index)


########################################################################
class VariablePage(wiz.WizardPageSimple):
    def __init__(self, parent, title, service_manager, var):
        """Constructor"""
        wiz.WizardPageSimple.__init__(self, parent)

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = sizer
        self.SetSizer(sizer)
        self.variable = var

        title = wx.StaticText(self, -1, title)
        title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        sizer.Add(title, 10, wx.ALIGN_CENTRE | wx.ALL, 5)
        sizer.Add(wx.StaticLine(self, -1), 5, wx.EXPAND | wx.ALL, 5)
        self.panel = pageVariable.pnlVariable(self, id=wxID_PNLVARIABLE, name=u'pnlVariable',
                                              pos=wx.Point(536, 285), size=wx.Size(439, 357),
                                              style=wx.TAB_TRAVERSAL, sm=service_manager, var=var)
        self.sizer.Add(self.panel, 85, wx.ALL, 5)

        self._init_data(self.panel.series_service)

    def _init_data(self, series_service):
        vars = series_service.get_all_variables()
        index = 0
        for v, i in zip(vars, range(len(vars))):
            num_items = self.panel.lstVariable.GetItemCount()
            self.panel.lstVariable.InsertStringItem(num_items, str(v.code))
            self.panel.lstVariable.SetStringItem(num_items, 1, str(v.name))
            self.panel.lstVariable.SetStringItem(num_items, 2, str(v.speciation))
            self.panel.lstVariable.SetStringItem(num_items, 3, str(v.variable_unit.name))
            self.panel.lstVariable.SetStringItem(num_items, 4, str(v.sample_medium))
            self.panel.lstVariable.SetStringItem(num_items, 5, str(v.value_type))
            self.panel.lstVariable.SetStringItem(num_items, 6, str(v.is_regular))
            self.panel.lstVariable.SetStringItem(num_items, 7, str(v.time_support))
            self.panel.lstVariable.SetStringItem(num_items, 8, str(v.time_unit.name))
            self.panel.lstVariable.SetStringItem(num_items, 9, str(v.data_type))
            self.panel.lstVariable.SetStringItem(num_items, 10, str(v.general_category))
            self.panel.lstVariable.SetStringItem(num_items, 11, str(v.no_data_value))
            self.panel.lstVariable.SetStringItem(num_items, 12, str(v.id))

            if v.code == self.variable.code:
                index = i
        self.panel.lstVariable.Focus(index)
        self.panel.lstVariable.Select(index)


########################################################################
class MethodPage(wiz.WizardPageSimple):  # Raname this page to page method controller
    def __init__(self, parent):
        # pageMethod.pnlMethod.__init__(self, parent)
        wiz.WizardPageSimple.__init__(self, parent)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.page_method_view = pageMethod.pnlMethod(self)
        main_sizer.Add(self.page_method_view, 1, wx.EXPAND | wx.ALL, 0)
        self.SetSizer(main_sizer)

# class MethodPage(wiz.WizardPageSimple):
#     def __init__(self, parent, title, series_service, method):
#         """Constructor"""
#         wiz.WizardPageSimple.__init__(self, parent)
#
#         sizer = wx.BoxSizer(wx.VERTICAL)
#         self.sizer = sizer
#         self.SetSizer(sizer)
#         self.method = method
#
#         title = wx.StaticText(self, -1, title)
#         title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
#         sizer.Add(title, 10, wx.ALIGN_CENTRE | wx.ALL, 5)
#         sizer.Add(wx.StaticLine(self, -1), 5, wx.EXPAND | wx.ALL, 5)
#         self.panel = pageMethod.pnlMethod(self, id=wxID_PNLMETHOD, name=u'pnlMethod',
#                                           pos=wx.Point(536, 285), size=wx.Size(439, 357),
#                                           style=wx.TAB_TRAVERSAL, ss=series_service, method=method)
#         self.sizer.Add(self.panel, 1, wx.EXPAND, 5)
#
#         self._init_data(self.panel.series_service)
#
#     def _init_data(self, series):
#         meth = series.get_all_methods()
#         index = 0
#         for m, i in zip(meth, range(len(meth))):
#             num_items = self.panel.lstMethods.GetItemCount()
#             self.panel.lstMethods.InsertStringItem(num_items, str(m.description))
#             self.panel.lstMethods.SetStringItem(num_items, 1, str(m.link))
#             self.panel.lstMethods.SetStringItem(num_items, 2, str(m.id))
#
#             if m.description == self.method.description:
#                 index = i
#
#         self.panel.lstMethods.Focus(index)
#         self.panel.lstMethods.Select(index)


########################################################################
class SummaryPage(wiz.WizardPageSimple):
    def __init__(self, parent, title, series_service):
        """Constructor"""
        wiz.WizardPageSimple.__init__(self, parent)
        self.parent = parent
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = sizer
        self.SetSizer(sizer)

        title = wx.StaticText(self, -1, title)
        title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        sizer.Add(title, 10, wx.ALIGN_CENTRE | wx.ALL, 5)
        sizer.Add(wx.StaticLine(self, -1), 5, wx.EXPAND | wx.ALL, 5)
        self.panel = pageSummary.pnlSummary(self, id=wxID_PNLSUMMARY, name=u'pnlSummary',
                                            pos=wx.Point(536, 285), size=wx.Size(439, 357),
                                            style=wx.TAB_TRAVERSAL, ss=series_service)
        self.sizer.Add(self.panel, 85, wx.ALL, 5)


    def fill_summary(self):
        Site, Variable, Method, Source, QCL = self.parent.get_metadata()

        ##        self.panel.treeSummary.SetItemText(self.panel.treeSummary.qc, "Code: "+ str(QCL.code))


        self.panel.treeSummary.SetItemText(self.panel.treeSummary.sc, 'Code: ' + str(Site.code))
        self.panel.treeSummary.SetItemText(self.panel.treeSummary.sn, 'Name: ' + str(Site.name))

        self.panel.treeSummary.SetItemText(self.panel.treeSummary.vc, 'Code: ' + str(Variable.code))
        self.panel.treeSummary.SetItemText(self.panel.treeSummary.vn, 'Name: ' + str(Variable.name))
        self.panel.treeSummary.SetItemText(self.panel.treeSummary.vu, 'Units: ' + str(Variable.variable_unit.name))
        self.panel.treeSummary.SetItemText(self.panel.treeSummary.vsm, 'Sample Medium: ' + str(Variable.sample_medium))
        self.panel.treeSummary.SetItemText(self.panel.treeSummary.vvt, 'Value Type: ' + str(Variable.value_type))
        self.panel.treeSummary.SetItemText(self.panel.treeSummary.vts, 'Time Support: ' + str(Variable.time_support))
        self.panel.treeSummary.SetItemText(self.panel.treeSummary.vtu, 'Time Units: ' + str(Variable.time_unit.name))
        self.panel.treeSummary.SetItemText(self.panel.treeSummary.vdt, 'Data Type: ' + str(Variable.data_type))
        self.panel.treeSummary.SetItemText(self.panel.treeSummary.vgc,
                                           'General Category: ' + str(Variable.general_category))

        self.panel.treeSummary.SetItemText(self.panel.treeSummary.md, 'Description: ' + str(Method.description))

        self.panel.treeSummary.SetItemText(self.panel.treeSummary.soo, 'Organization: ' + str(Source.organization))
        self.panel.treeSummary.SetItemText(self.panel.treeSummary.sod, 'Description: ' + str(Source.description))
        self.panel.treeSummary.SetItemText(self.panel.treeSummary.soc, 'Citation: ' + str(Source.citation))

        self.panel.treeSummary.SetItemText(self.panel.treeSummary.qc, 'Code: ' + str(QCL.code))
        self.panel.treeSummary.SetItemText(self.panel.treeSummary.qd, 'Definition: ' + str(QCL.definition))
        self.panel.treeSummary.SetItemText(self.panel.treeSummary.qe, 'Explanation: ' + str(QCL.explanation))

        self.panel.treeSummary.ExpandAll()


########################################################################
class wizSave(wx.wizard.Wizard):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wiz.Wizard.__init__(self, id=wxID_WIZSAVE,
                            parent=prnt, title=u'Save...')
        self.SetToolTipString(u'Save Wizard')
        self.SetName(u'wizSave')
        ##self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED,  self.onPlotSelection, id=wxID_RIBBONPLOTTIMESERIES)
        self.Bind(wx.wizard.EVT_WIZARD_PAGE_CHANGED, self.on_page_changed)
        Publisher.subscribe(self.on_page_changing, ("wizChangeSave"))
        #self.Bind( wx.wizard.EVT_WIZARD_PAGE_CHANGING, self.on_page_changing )

        self.Bind(wx.wizard.EVT_WIZARD_FINISHED, self.on_wizard_finished)

    def get_metadata(self):

        if self.pgIntro.pnlIntroduction.rbSaveAs.GetValue():
            logger.debug("SaveAs")
            method = self.pgMethod.panel.getMethod()
            qcl = self.pgQCL.panel.getQCL()
            variable = self.pgVariable.panel.getVariable()
        elif self.pgIntro.pnlIntroduction.rbSave.GetValue():
            logger.debug("Save")
            method = self.currSeries.method
            qcl = self.currSeries.quality_control_level
            variable = self.currSeries.variable
        elif self.pgIntro.pnlIntroduction.rbSaveExisting.GetValue():
            logger.debug("Existing")
            method, qcl, variable = self.pgExisting.getSeries()
        site = self.currSeries.site
        source = self.currSeries.source
        logger.debug("site: %s, variable: %s, method: %s, source: %s, qcl: %s" % (
        str(site), str(variable), str(method), str(source), str(qcl)))
        return site, variable, method, source, qcl

    def __init__(self, parent, service_manager, record_service):
        self._init_ctrls(parent)
        try:
            self.series_service = record_service._edit_service.memDB.series_service #service_man.get_series_service()
        except:
            #for testing
            self.series_service = record_service.memDB.series_service
        self.record_service = record_service
        # self.is_changing_series = False
        self.currSeries = record_service.get_series()

        self.pgIntro = pageIntro.pageIntro(self, "Intro")
        # self.pgMethod = MethodPage(self, "Method", self.series_service, self.currSeries.method)
        self.pgMethod = MethodPage(self)
        self.pgQCL = QCLPage(self, "Quality Control Level", self.series_service, self.currSeries.quality_control_level)
        self.pgVariable = VariablePage(self, "Variable", service_manager, self.currSeries.variable)
        self.pgExisting = pageExisting.pageExisting(self, "Existing Series", self.series_service, self.currSeries.site)
        self.pgSummary = SummaryPage(self, "Summary", self.series_service)

        self.FitToPage(self.pgIntro)

        # Set the initial order of the pages
        self.pgIntro.SetNext(self.pgSummary)
        self.pgSummary.SetPrev(self.pgIntro)


        #SaveAs Pages
        self.pgMethod.SetPrev(self.pgIntro)
        self.pgMethod.SetNext(self.pgQCL)

        self.pgQCL.SetPrev(self.pgMethod)
        self.pgQCL.SetNext(self.pgVariable)

        self.pgVariable.SetPrev(self.pgQCL)
        self.pgVariable.SetNext(self.pgSummary)

        #Save existing  page
        self.pgExisting.SetPrev(self.pgIntro)
        self.pgExisting.SetNext(self.pgSummary)

        self.GetPageAreaSizer().Add(self.pgIntro)
        self.RunWizard(self.pgIntro)
        self.Destroy()

    def on_page_changed(self, event):
        #if  isinstance(event.Page, pageSummary.pnlSummary):
        if event.Page == self.pgSummary:
            self.pgSummary.fill_summary()

    def on_page_changing(self, event):
       # if isinstance(event.Page, pageIntro):
        if self.pgIntro.pnlIntroduction.rbSave.GetValue():
            self.pgIntro.SetNext(self.pgSummary)
            self.pgSummary.SetPrev(self.pgIntro)

        elif self.pgIntro.pnlIntroduction.rbSaveAs.GetValue():
            self.pgIntro.SetNext(self.pgMethod)
            self.pgSummary.SetPrev(self.pgVariable)

        else:
            self.pgIntro.SetNext(self.pgExisting)
            self.pgSummary.SetPrev(self.pgExisting)

    def on_wizard_finishedtest(self, event):
        self.Destroy()
        self.Close()

    def on_wizard_finished(self, event):
        Site, Variable, Method, Source, QCL = self.get_metadata()
        #if qcl exits use its its
        closeSuccessful = False

        rbSave = self.pgIntro.pnlIntroduction.rbSave.GetValue()
        rbSaveAsNew = self.pgIntro.pnlIntroduction.rbSaveAs.GetValue()
        rbSaveAsExisting = self.pgIntro.pnlIntroduction.rbSaveExisting.GetValue()
        if rbSaveAsExisting:
            append = self.pgExisting.pnlExisting.rbAppend.GetValue()
            overwrite = self.pgExisting.pnlExisting.rbOverwrite.GetValue()
            if append:
                original = self.pgExisting.pnlExisting.rbOriginal.GetValue()
                new = self.pgExisting.pnlExisting.rbNew.GetValue()

        if QCL.id == 0 and not rbSaveAsNew:
            """
            If we're looking at a QCL with Control level 0 and the following cases:
                Save
                SaveExisting
            """
            val = wx.MessageBox("You are writing a level 0 dataset, which is usually reserved for raw data.\n"
                                "Are you sure you want to save?",
                                'Are you Sure?',
                                wx.YES_NO | wx.ICON_QUESTION)
            if val == 2:
                logger.info("User selected yes to save a level 0 dataset")
                val_2 = wx.MessageBox("This action cannot be undone.\nAre you sure you are sure?\n",
                                      'Are you REALLY sure?',
                                      wx.YES_NO | wx.ICON_QUESTION)
                if val_2 == 2:
                    closeSuccessful = True

        elif rbSaveAsExisting:
            keyword = "overwrite"

            if self.pgExisting.pnlExisting.rbAppend.GetValue():
                keyword = "append to"

            message = "You are about to " + keyword + " an existing series,\nthis action cannot be undone.\nWould you like to continue?\n"
            cont = wx.MessageBox(message, 'Are you sure?', wx.YES_NO | wx.ICON_QUESTION)
            if cont == 2:
                closeSuccessful = True
            else:
                closeSuccessful = False
        else:
            closeSuccessful = True

        if closeSuccessful:
            #if qcl exists use its id
            if self.series_service.qcl_exists(QCL):
                if QCL == self.currSeries.quality_control_level:
                    QCL = None
                else:
                    QCL = self.record_service.get_qcl(QCL)
            else:
                QCL = self.record_service.create_qcl(QCL.code, QCL.definition, QCL.explanation)

            #if variable exists use its id
            if self.series_service.variable_exists(Variable):
                Variable = self.record_service.get_variable(Variable)
            else:
                Variable = self.record_service.create_variable(Variable)

            #if method exists use its id
            if self.series_service.method_exists(Method):
                if Method == self.currSeries.method:
                    Method = None
                else:
                    Method = self.record_service.get_method(Method)
            else:
                Method = self.record_service.create_method(Method)

            # initiate either "Save as" or "Save"
            '''
            if self.page1.pnlIntroduction.rbSave.GetValue():
                result = self.record_service.save(Variable, Method, QCL, False)
            else:
                result = self.record_service.saveAs(Variable, Method, QCL, True)
            '''

            try:
                if rbSave:
                    result = self.record_service.save()
                elif rbSaveAsNew:
                    result = self.record_service.save_as(Variable, Method, QCL)
                elif rbSaveAsExisting:
                    if overwrite:
                        result = self.record_service.save_existing(Variable, Method, QCL)
                    elif append:
                        #def save_appending(self, var = None, method =None, qcl = None, overwrite = False):
                        #TODO if i require that original or new is selected I can call once with overwrite = original
                        if original:
                            result = self.record_service.save_appending(Variable, Method, QCL, overwrite = False)
                        elif new:
                            result = self.record_service.save_appending(Variable, Method, QCL, overwrite = True)

                Publisher.sendMessage("refreshSeries")

                    #self.page1.pnlIntroduction.rb
            except Exception as e:
                message = "Save was unsuccessful %s" % e.message
                logger.error(message)
                wx.MessageBox(message, "Error!", wx.ICON_ERROR | wx.ICON_EXCLAMATION)
            event.Skip()
            self.Close()



