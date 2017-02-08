import wx
import wx.wizard as wiz
from odmtools.controller import pageIntro, pageExisting
import pageSummary
from odm2api.ODM2.models import *
from odmtools.controller.WizardMethodController import WizardMethodController
from odmtools.controller.WizardProcessLevelController import WizardProcessLevelController
from odmtools.controller.WizardVariableController import WizardVariableController
from odmtools.controller.WizardActionController import WizardActionController

[wxID_PNLINTRO, wxID_PNLVARIABLE, wxID_PNLMETHOD, wxID_PNLQCL,
 wxID_PNLSUMMARY, wxID_WIZSAVE, wxID_PNLEXISTING,
] = [wx.NewId() for _init_ctrls in range(7)]

from wx.lib.pubsub import pub as Publisher
from odmtools.common.logger import LoggerTool
import logging
logger = logging.getLogger('main')



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
        sampling_feature, variable, method, action, processing_level = self.parent.get_metadata()

        self.panel.treeSummary.SetItemText(self.panel.treeSummary.sc, 'Code: ' + str(sampling_feature.SamplingFeatureCode))
        self.panel.treeSummary.SetItemText(self.panel.treeSummary.sn, 'Name: ' + str(sampling_feature.SamplingFeatureName))

        self.panel.treeSummary.SetItemText(self.panel.treeSummary.vc, 'Code: ' + str(variable.VariableCode))
        self.panel.treeSummary.SetItemText(self.panel.treeSummary.vn, 'Name: ' + str(variable.VariableNameCV))

        self.panel.treeSummary.SetItemText(self.panel.treeSummary.md, 'Description: ' + str(method.MethodDescription))

        self.panel.treeSummary.SetItemText(self.panel.treeSummary.soo, 'Organization: ' + str(action.MethodObj.OrganizationObj.OrganizationName))
        self.panel.treeSummary.SetItemText(self.panel.treeSummary.sod, 'Description: ' + str(action.MethodObj.OrganizationObj.OrganizationDescription))

        self.panel.treeSummary.SetItemText(self.panel.treeSummary.qc, 'Code: ' + str(processing_level.ProcessingLevelCode))
        self.panel.treeSummary.SetItemText(self.panel.treeSummary.qd, 'Definition: ' + str(processing_level.Definition))
        self.panel.treeSummary.SetItemText(self.panel.treeSummary.qe, 'Explanation: ' + str(processing_level.Explanation))

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
        method = self.__method_from_series
        processing_level = self.__processing_level_from_series
        variable = self.__variable_from_series
        affiliation = self.action_page.get_affiliation()
        site = self.__site_from_series


        if self.pgIntro.pnlIntroduction.rbSaveAs.GetValue():
            # Selected a new series
            method = self.pgMethod.get_method()
            processing_level = self.pgQCL.get_processing_level()
            variable = self.pgVariable.get_variable()

        elif self.pgIntro.pnlIntroduction.rbSaveExisting.GetValue():
            # selected an existing series
            method, processing_level, variable, result = self.pgExisting.get_selected_series()

        # Create action
        action = Actions()
        action.MethodObj = method
        action.MethodID = method.MethodID
        action.ActionDescription = self.action_page.action_view.description_text_box.GetValue()
        action.ActionFileLink = self.action_page.action_view.action_file_link_text_box.GetValue()
        action.MethodObj.OrganizationObj = affiliation.OrganizationObj
        action.BeginDateTime = self.currSeries.ResultDateTime
        action.BeginDateTimeUTCOffset = self.currSeries.ResultDateTimeUTCOffset

        return site, variable, method, action, processing_level

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

        self.__method_from_series = self.currSeries.FeatureActionObj.ActionObj.MethodObj
        self.__variable_from_series = self.currSeries.VariableObj
        self.__processing_level_from_series = self.currSeries.ProcessingLevelObj
        self.__all_affiliations = self.series_service.get_all_affiliations()
        self.__site_from_series = self.currSeries.FeatureActionObj.SamplingFeatureObj

        self.pgMethod = WizardMethodController(self, self.series_service, current_method=self.__method_from_series)
        self.pgQCL = WizardProcessLevelController(self, service_manager=service_manager, current_processing_level=self.__processing_level_from_series)
        self.pgVariable = WizardVariableController(self, service_manager=service_manager, current_variable=self.__variable_from_series)
        self.action_page = WizardActionController(self, affiliations=self.__all_affiliations)

        self.pgExisting = pageExisting.pageExisting(self, "Existing Series", self.series_service, self.__site_from_series)


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
        self.pgVariable.SetNext(self.action_page)

        self.action_page.SetPrev(self.pgVariable)
        self.action_page.SetNext(self.pgSummary)

        #Save existing  page
        self.pgExisting.SetPrev(self.pgIntro)
        self.pgExisting.SetNext(self.pgSummary)

        self.GetPageAreaSizer().Add(self.pgIntro)
        self.RunWizard(self.pgIntro)
        self.Destroy()

    def on_page_changed(self, event):
        if event.Page == self.pgSummary:
            self.pgSummary.fill_summary()

    def on_page_changing(self, event):
       # if isinstance(event.Page, pageIntro):
        if self.pgIntro.pnlIntroduction.rbSave.GetValue():
            self.pgIntro.SetNext(self.pgSummary)
            self.pgSummary.SetPrev(self.pgIntro)

        elif self.pgIntro.pnlIntroduction.rbSaveAs.GetValue():
            self.pgIntro.SetNext(self.pgMethod)
            self.pgSummary.SetPrev(self.action_page)

        else:
            self.pgIntro.SetNext(self.pgExisting)
            self.pgSummary.SetPrev(self.pgExisting)

    def on_wizard_finishedtest(self, event):
        self.Destroy()
        self.Close()

    def on_wizard_finished(self, event):
        site, variable, method, action, proc_level = self.get_metadata()
        #if qcl exits use its its
        closeSuccessful = False
        saveSuccessful=False

        self.rbSave = self.pgIntro.pnlIntroduction.rbSave.GetValue()
        self.rbSaveAsNew = self.pgIntro.pnlIntroduction.rbSaveAs.GetValue()
        self.rbSaveAsExisting = self.pgIntro.pnlIntroduction.rbSaveExisting.GetValue()
        if self.rbSaveAsExisting:
            self.append = self.pgExisting.pnlExisting.rbAppend.GetValue()
            self.overwrite = self.pgExisting.pnlExisting.rbOverwrite.GetValue()
            if self.append:
                self.original = self.pgExisting.pnlExisting.rbOriginal.GetValue()
                self.new = self.pgExisting.pnlExisting.rbNew.GetValue()

        if proc_level.ProcessingLevelID == 0 and not self.rbSaveAsNew:
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
                val_2 = wx.MessageBox("This  cannot be undone.\nAre you sure you are sure?\n",
                                      'Are you REALLY sure?',
                                      wx.YES_NO | wx.ICON_QUESTION)
                if val_2 == 2:
                    closeSuccessful = True

        elif self.rbSaveAsExisting:
            keyword = "overwrite"

            if self.pgExisting.pnlExisting.rbAppend.GetValue():
                keyword = "append to"

            message = "You are about to " + keyword + " an existing series_service,\nthis cannot be undone.\nWould you like to continue?\n"
            cont = wx.MessageBox(message, 'Are you sure?', wx.YES_NO | wx.ICON_QUESTION)
            if cont == 2:
                closeSuccessful = True
            else:
                closeSuccessful = False
        else:
            closeSuccessful = True

        if closeSuccessful:
            try:
                saveSuccessful = self.try_to_save(variable, method, proc_level, action)
            except Exception as e:
                message = "Save was unsuccessful %s" % e.message
                logger.error(message)
                wx.MessageBox(message, "Error!", wx.ICON_ERROR | wx.ICON_EXCLAMATION)
                saveSuccessful=False

        if saveSuccessful:
            event.Skip()
            self.Close()
            self.Destroy()

    def create_needed_meta(self, proc_level,variable, method):
        if self.series_service.get_processing_level_by_code(proc_level.ProcessingLevelCode) is None:
            proc_level = self.series_service.create_processing_level(proc_level.ProcessingLevelCode, proc_level.Definition, proc_level.Explanation)
        elif proc_level.ProcessingLevelCode == self.__processing_level_from_series.ProcessingLevelCode:
            proc_level = None
        else:
            proc_level = self.series_service.get_processing_level_by_code(proc_level.ProcessingLevelCode)



        if self.series_service.get_variable_by_code(variable.VariableCode) is None:
            variable = self.series_service.create_variable_by_var(variable)
        else:
            variable = self.series_service.get_variable_by_code(variable.VariableCode)



        if self.series_service.get_method_by_code(method.MethodCode) is None:
            method = self.series_service.create_method(method.MethodDescription, method.MethodLink)
        elif method == self.__method_from_series:
            method = None
        else:
            method = self.series_service.get_method_by_code(method.MethodCode)


    def try_to_save(self, variable, method, proc_level, action):
        self.create_needed_meta(proc_level, variable, method)
        affiliation = self.action_page.get_affiliation()

        action_by = ActionBy()
        # action_by.ActionID = action.ActionID
        action_by.RoleDescription = self.action_page.action_view.role_description_text_box.GetValue()
        action_by.AffiliationID = affiliation.AffiliationID
        action_by.AffiliationObj = affiliation

        # result = self.series_service.getResult(var=variable, meth=method, proc=proc_level, action=action, actionby=action_by)
        result = self.pgExisting.pnlExisting.olvSeriesList.GetSelectedObject().ResultObj

        if self.rbSave:
            result = self.record_service.save()
        elif self.rbSaveAsNew:
            result = self.record_service.save_as(variable=variable, method=method, proc_level=proc_level,
                                                action=action, action_by=action_by)
        elif self.rbSaveAsExisting:
            if self.overwrite:
                result = self.record_service.save_existing(result=result)
            elif self.append:
                #TODO send in just the result
                #def save_appending(self, var = None, method =None, qcl = None, overwrite = False):
                #TODO if i require that original or new is selected I can call once with overwrite = original
                if self.original:
                    result = self.record_service.save_appending(result=result, overwrite=False)
                elif self.new:
                    result = self.record_service.save_appending(result=result, overwrite=True)

        Publisher.sendMessage("refreshSeries")
        return True







