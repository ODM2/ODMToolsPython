#Boa:Wizard:wizSave

import wx
import wx.wizard as wiz

# import * from WizardPanels
import pnlMethod
import pnlQCL
import pnlVariable
import pnlSummary
import pnlIntro

[wxID_PNLINTRO, wxID_PNLVARIABLE, wxID_PNLMETHOD, wxID_PNLQCL,
wxID_PNLSUMMARY, wxID_WIZSAVE,
] = [wx.NewId() for _init_ctrls in range(6)]




########################################################################
class QCLPage(wiz.WizardPageSimple):
    def __init__(self, parent, title, service_man):
        """Constructor"""
        wiz.WizardPageSimple.__init__(self, parent)

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = sizer
        self.SetSizer(sizer)

        title = wx.StaticText(self, -1, title)
        title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        sizer.Add(title, 10, wx.ALIGN_CENTRE|wx.ALL, 5)
        sizer.Add(wx.StaticLine(self, -1), 5, wx.EXPAND|wx.ALL, 5)
        self.panel=pnlQCL.pnlQCL(self, id=wxID_PNLINTRO, name=u'pnlQCL',
              pos=wx.Point(536, 285), size=wx.Size(439, 357),
              style=wx.TAB_TRAVERSAL, sm = service_man)
        self.sizer.Add(self.panel, 85, wx.ALL, 5)
        series_service  = service_man.get_series_service()
        self._init_data(series_service)

    def _init_data(self, series):
        qcl=series.get_all_qcls()
        for q in qcl:
            num_items = self.panel.lstQCL.GetItemCount()
            self.panel.lstQCL.InsertStringItem(num_items, str(q.code))
            self.panel.lstQCL.SetStringItem(num_items, 1, str(q.definition))
            self.panel.lstQCL.SetStringItem(num_items, 2, str(q.explanation))
            self.panel.lstQCL.SetStringItem(num_items, 3 , str(q.id))



########################################################################
class VariablePage(wiz.WizardPageSimple):
    def __init__(self, parent, title, service_man, var):
        """Constructor"""
        wiz.WizardPageSimple.__init__(self, parent)

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = sizer
        self.SetSizer(sizer)

        title = wx.StaticText(self, -1, title)
        title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        sizer.Add(title, 10, wx.ALIGN_CENTRE|wx.ALL, 5)
        sizer.Add(wx.StaticLine(self, -1), 5, wx.EXPAND|wx.ALL, 5)
        self.panel=pnlVariable.pnlVariable(self, id=wxID_PNLVARIABLE, name=u'pnlVariable',
              pos=wx.Point(536, 285), size=wx.Size(439, 357),
              style=wx.TAB_TRAVERSAL,sm = service_man, var = var)
        self.sizer.Add(self.panel, 85, wx.ALL, 5)
        series_service = service_man.get_series_service()
        self._init_data(series_service)

    def _init_data(self, series_service):
        vars=series_service.get_vars()
        for v in vars:
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

########################################################################
class MethodPage(wiz.WizardPageSimple):
    def __init__(self, parent, title,service_man):
        """Constructor"""
        wiz.WizardPageSimple.__init__(self, parent)

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = sizer
        self.SetSizer(sizer)

        title = wx.StaticText(self, -1, title)
        title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        sizer.Add(title, 10, wx.ALIGN_CENTRE|wx.ALL, 5)
        sizer.Add(wx.StaticLine(self, -1), 5, wx.EXPAND|wx.ALL, 5)
        self.panel=pnlMethod.pnlMethod(self, id=wxID_PNLMETHOD, name=u'pnlMethod',
              pos=wx.Point(536, 285), size=wx.Size(439, 357),
              style=wx.TAB_TRAVERSAL,sm = service_man)
        self.sizer.Add(self.panel, 85, wx.ALL, 5)
        series_service = service_man.get_series_service()
        self._init_data(series_service)

    def _init_data(self, series):
        meth=series.get_all_methods()
        for m in meth:
            num_items = self.panel.lstMethods.GetItemCount()
            self.panel.lstMethods.InsertStringItem(num_items, str(m.description))
            self.panel.lstMethods.SetStringItem(num_items, 1, str(m.link))
            self.panel.lstMethods.SetStringItem(num_items, 2, str(m.id))



########################################################################
class SummaryPage(wiz.WizardPageSimple):
    def __init__(self, parent, title, service_man):
        """Constructor"""
        wiz.WizardPageSimple.__init__(self, parent)
        self.parent= parent
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = sizer
        self.SetSizer(sizer)

        title = wx.StaticText(self, -1, title)
        title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        sizer.Add(title, 10, wx.ALIGN_CENTRE|wx.ALL, 5)
        sizer.Add(wx.StaticLine(self, -1), 5, wx.EXPAND|wx.ALL, 5)
        self.panel =pnlSummary.pnlSummary(self, id=wxID_PNLSUMMARY, name=u'pnlSummary',
              pos=wx.Point(536, 285), size=wx.Size(439, 357),
              style=wx.TAB_TRAVERSAL, sm = service_man)
        self.sizer.Add(self.panel, 85, wx.ALL, 5)


    def fill_summary(self):
        Site, Variable, Method, Source, QCL=self.parent.get_metadata()

##        self.panel.treeSummary.SetItemText(self.panel.treeSummary.qc, "Code: "+ str(QCL.code))


        self.panel.treeSummary.SetItemText(self.panel.treeSummary.sc, 'Code: '+ str(Site.code))
        self.panel.treeSummary.SetItemText(self.panel.treeSummary.sn, 'Name: '+ str(Site.name))

        self.panel.treeSummary.SetItemText(self.panel.treeSummary.vc, 'Code: '+ str(Variable.code))
        self.panel.treeSummary.SetItemText(self.panel.treeSummary.vn, 'Name: '+ str(Variable.name))
        self.panel.treeSummary.SetItemText(self.panel.treeSummary.vu, 'Units: '+ str(Variable.variable_unit.name))
        self.panel.treeSummary.SetItemText(self.panel.treeSummary.vsm, 'Sample Medium: '+ str(Variable.sample_medium))
        self.panel.treeSummary.SetItemText(self.panel.treeSummary.vvt, 'Value Type: '+ str(Variable.value_type))
        self.panel.treeSummary.SetItemText(self.panel.treeSummary.vts, 'Time Support: '+ str(Variable.time_support))
        self.panel.treeSummary.SetItemText(self.panel.treeSummary.vtu, 'Time Units: '+ str(Variable.time_unit.name))
        self.panel.treeSummary.SetItemText(self.panel.treeSummary.vdt, 'Data Type: '+ str(Variable.data_type))
        self.panel.treeSummary.SetItemText(self.panel.treeSummary.vgc, 'General Category: '+ str(Variable.general_category))

        self.panel.treeSummary.SetItemText(self.panel.treeSummary.md, 'Description: '+ str(Method.description))

        self.panel.treeSummary.SetItemText(self.panel.treeSummary.soo, 'Organization: '+ str(Source.organization))
        self.panel.treeSummary.SetItemText(self.panel.treeSummary.sod, 'Description: '+ str(Source.description))
        self.panel.treeSummary.SetItemText(self.panel.treeSummary.soc, 'Citation: '+ str(Source.citation))

        self.panel.treeSummary.SetItemText(self.panel.treeSummary.qc, 'Code: '+ str(QCL.code))
        self.panel.treeSummary.SetItemText(self.panel.treeSummary.qd, 'Definition: '+ str(QCL.definition))
        self.panel.treeSummary.SetItemText(self.panel.treeSummary.qe, 'Explanation: '+ str(QCL.explanation))

        self.panel.treeSummary.ExpandAll()



########################################################################
class IntroPage(wiz.PyWizardPage):
    def __init__(self, parent, title):
        """Constructor"""
        wiz.PyWizardPage.__init__(self, parent)
        self.next = self.prev = None
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = sizer
        self.SetSizer(sizer)

        title = wx.StaticText(self, -1, title)
        title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        sizer.Add(title, 10, wx.ALIGN_CENTRE|wx.ALL, 5)
        sizer.Add(wx.StaticLine(self, -1), 5, wx.EXPAND|wx.ALL, 5)
        self.pnlIntroduction=pnlIntro.pnlIntro(self, id=wxID_PNLINTRO, name=u'pnlIntro',
              pos=wx.Point(536, 285), size=wx.Size(439, 357), style=wx.TAB_TRAVERSAL)
        self.sizer.Add(self.pnlIntroduction, 85, wx.ALL, 5)

    def SetNext(self, next):
        self.next = next

    def SetPrev(self, prev):
        self.prev = prev

    def GetNext(self):
        """If the checkbox is set then return the next page's next page otherwise return the very last page"""
        if self.pnlIntroduction.rbSave.GetValue():
            self.next.GetNext().GetNext().GetNext().SetPrev(self)
            return self.next.GetNext().GetNext().GetNext()
        else:
            # print self.next
            self.next.GetNext().SetPrev(self.next)
            return self.next

    def GetPrev(self):
        return self.prev


########################################################################

class TitledPage(wiz.WizardPageSimple):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent, title):
        """Constructor"""
        wiz.WizardPageSimple.__init__(self, parent)

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = sizer
        self.SetSizer(sizer)

        title = wx.StaticText(self, -1, title)
        title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        sizer.Add(title, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND|wx.ALL, 5)


########################################################################



def create(parent):
    return wizSave(parent, serviceMan)



class wizSave(wx.wizard.Wizard):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wiz.Wizard.__init__(self, id=wxID_WIZSAVE,
              parent=prnt, title=u'Save...')
        self.SetToolTipString(u'Save Wizard')
        self.SetName(u'wizSave')
##self.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED,  self.onPlotSelection, id=wxID_RIBBONPLOTTIMESERIES)
        self.Bind(wx.wizard.EVT_WIZARD_PAGE_CHANGED, self.on_page_changing)
        self.Bind(wx.wizard.EVT_WIZARD_FINISHED, self.on_wizard_finished)

    def get_metadata(self):


        if self.is_changing_series:
            method = self.page2.panel.getMethod()
            qcl = self.page3.panel.getQCL()
            variable = self.page4.panel.getVariable()
        else:
            method = self.currSeries.method
            qcl = self.currSeries.quality_control_level
            variable =self.currSeries.variable
        site = self.currSeries.site
        source = self.currSeries.source
        return site, variable, method, source, qcl

    def __init__(self, parent, service_man, record_service):
        self._init_ctrls(parent)
        self.series_service = service_man.get_series_service()
        self.record_service = record_service
        self.is_changing_series = False
        self.currSeries = record_service.get_series()

        self.page1 = IntroPage(self, "Intro")

        self.page2 = MethodPage(self, "Method", service_man)
        self.page3 = QCLPage(self, "Quality Control Level", service_man)
        self.page4 = VariablePage(self, "Variable", service_man, self.currSeries.variable)
        self.page5 = SummaryPage(self, "Summary", service_man)

        self.FitToPage(self.page1)
##        page5.sizer.Add(wx.StaticText(page5, -1, "\nThis is the last page."))

        # Set the initial order of the pages
        self.page1.SetNext(self.page2)

        self.page2.SetPrev(self.page1)
        self.page2.SetNext(self.page3)

        self.page3.SetPrev(self.page2)
        self.page3.SetNext(self.page4)

        self.page4.SetPrev(self.page3)
        self.page4.SetNext(self.page5)

        self.page5.SetPrev(self.page4)

##        fin_btn = self.FindWindowById(wx.ID_FINISH)
##        fin_btn.SetLabel("Save Series")


        self.GetPageAreaSizer().Add(self.page1)
        self.RunWizard(self.page1)
        self.Destroy()

    def on_page_changing(self, event):
        if event.Page == self.page5:
            self.page5.fill_summary()
        elif event.Page==self.page1:
            self.is_changing_series = False
        else:
            self.is_changing_series = True


    def on_wizard_finished(self, event):
        Site, Variable, Method, Source, QCL= self.get_metadata()
        #if qcl exits use its its

        if self.series_service.qcl_exists(QCL):
            if QCL==self.currSeries.quality_control_level:
                QCL=None
            else:
                QCL = self.record_service.get_qcl(QCL)
        else:
            QCL=self.record_service.create_qcl(QCL.code, QCL.definition, QCL.explanation)

        #if variable exists use its id
        if self.series_service.variable_exists(Variable):
            if Variable==self.currSeries.variable:
                Variable= None
            else:
                Variable = self.record_service.get_variable(Variable)
        else:
            Variable=self.record_service.create_variable(Variable)
        #if method exists use its id
        if self.series_service.method_exists(Method):
            if Method==self.currSeries.method:
                Method=None
            else:
                Method = self.record_service.get_method(Method)
        else:
            Method=self.record_service.create_method(Method)

        self.record_service.save(Variable, Method, QCL)
        #t actual object from session. if it doesnt exist in the database use the created one.
##        event.Skip()



