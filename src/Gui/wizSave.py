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


def CreateBitmap(xpm):
    bmp = wx.Image(xpm, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
    return bmp


########################################################################
class QCLPage(wiz.WizardPageSimple):
    def __init__(self, parent, title):
        """Constructor"""
        wiz.WizardPageSimple.__init__(self, parent)
 
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = sizer
        self.SetSizer(sizer)
 
        title = wx.StaticText(self, -1, title)
        title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        sizer.Add(title, 10, wx.ALIGN_CENTRE|wx.ALL, 5)
        sizer.Add(wx.StaticLine(self, -1), 5, wx.EXPAND|wx.ALL, 5)
        self.sizer.Add(pnlQCL.pnlQCL(self, id=wxID_PNLINTRO, name=u'pnlQCL',
              pos=wx.Point(536, 285), size=wx.Size(439, 357),
              style=wx.TAB_TRAVERSAL), 85, wx.ALL, 5)


########################################################################
class VariablePage(wiz.WizardPageSimple):
    def __init__(self, parent, title):
        """Constructor"""
        wiz.WizardPageSimple.__init__(self, parent)
 
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = sizer
        self.SetSizer(sizer)
 
        title = wx.StaticText(self, -1, title)
        title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        sizer.Add(title, 10, wx.ALIGN_CENTRE|wx.ALL, 5)
        sizer.Add(wx.StaticLine(self, -1), 5, wx.EXPAND|wx.ALL, 5)
        self.sizer.Add(pnlVariable.pnlVariable(self, id=wxID_PNLVARIABLE, name=u'pnlVariable',
              pos=wx.Point(536, 285), size=wx.Size(439, 357),
              style=wx.TAB_TRAVERSAL), 85, wx.ALL, 5)

########################################################################
class MethodPage(wiz.WizardPageSimple):
    def __init__(self, parent, title):
        """Constructor"""
        wiz.WizardPageSimple.__init__(self, parent)
 
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = sizer
        self.SetSizer(sizer)
 
        title = wx.StaticText(self, -1, title)
        title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        sizer.Add(title, 10, wx.ALIGN_CENTRE|wx.ALL, 5)
        sizer.Add(wx.StaticLine(self, -1), 5, wx.EXPAND|wx.ALL, 5)
        self.sizer.Add(pnlMethod.pnlMethod(self, id=wxID_PNLMETHOD, name=u'pnlMethod',
              pos=wx.Point(536, 285), size=wx.Size(439, 357),
              style=wx.TAB_TRAVERSAL), 85, wx.ALL, 5)
              
              
########################################################################
class SummaryPage(wiz.WizardPageSimple):
    def __init__(self, parent, title):
        """Constructor"""
        wiz.WizardPageSimple.__init__(self, parent)
 
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = sizer
        self.SetSizer(sizer)
 
        title = wx.StaticText(self, -1, title)
        title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        sizer.Add(title, 10, wx.ALIGN_CENTRE|wx.ALL, 5)
        sizer.Add(wx.StaticLine(self, -1), 5, wx.EXPAND|wx.ALL, 5)
        self.sizer.Add(pnlSummary.pnlSummary(self, id=wxID_PNLSUMMARY, name=u'pnlSummary',
              pos=wx.Point(536, 285), size=wx.Size(439, 357),
              style=wx.TAB_TRAVERSAL), 85, wx.ALL, 5)
              
              
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
        """If the checkbox is set then return the next page's next page"""
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
    return wizSave(parent)



class wizSave(wx.wizard.Wizard):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wiz.Wizard.__init__(self, bitmap=CreateBitmap("images\\wizardsave.png"), id=wxID_WIZSAVE,
              parent=prnt, pos=wx.Point(748, 331), title=u'Save...')
        self.SetToolTipString(u'Save Wizard')
        self.SetName(u'wizSave')
        
        
        

    def __init__(self, parent):
        self._init_ctrls(parent)
        
        page1 = IntroPage(self, "Intro")
        
        page2 = MethodPage(self, "Method")
        page3 = QCLPage(self, "Quality Control Level")
        page4 = VariablePage(self, "Variable")
        page5 = SummaryPage(self, "Summary")
 
        self.FitToPage(page1)
##        page5.sizer.Add(wx.StaticText(page5, -1, "\nThis is the last page."))
 
        # Set the initial order of the pages
        page1.SetNext(page2)
        
        page2.SetPrev(page1)
        page2.SetNext(page3)
        
        page3.SetPrev(page2)
        page3.SetNext(page4)
        
        page4.SetPrev(page3)
        page4.SetNext(page5)
        
        page5.SetPrev(page4)
 
##        fin_btn = self.FindWindowById(wx.ID_FINISH)
##        fin_btn.SetLabel("Save Series")
 
    
        self.GetPageAreaSizer().Add(page1)
        self.RunWizard(page1)
        self.Destroy()


if __name__ == '__main__':
    app = wx.App(False)
    frame = create(None)
    frame.Show()

    app.MainLoop()
