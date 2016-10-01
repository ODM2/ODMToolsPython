import wx
from odmtools.view.WizardVariableView import WizardVariableView
from wx.wizard import WizardPageSimple


class WizardVariableController(WizardPageSimple):
    def __init__(self, parent):
        WizardPageSimple.__init__(self, parent)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.variable_view = WizardVariableView(self)
        main_sizer.Add(self.variable_view, 1, wx.EXPAND | wx.ALL, 0)
        self.SetSizer(main_sizer)