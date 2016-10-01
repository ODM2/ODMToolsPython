import wx
from odmtools.view.WizardProcessLevelView import WizardProcessLevelView
from wx.wizard import WizardPageSimple


class WizardProcessLevelController(WizardPageSimple):
    def __init__(self, parent):
        WizardPageSimple.__init__(self, parent)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.method_view = WizardProcessLevelView(self)
        main_sizer.Add(self.method_view, 1, wx.EXPAND | wx.ALL, 0)
        self.SetSizer(main_sizer)