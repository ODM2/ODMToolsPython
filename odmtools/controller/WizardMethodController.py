import wx
from wx.wizard import WizardPageSimple
from odmtools.view.WizardMethodView import WizardMethodView


class WizardMethodController(WizardPageSimple):
    def __init__(self, parent, series):
        WizardPageSimple.__init__(self, parent)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.method_view = WizardMethodView(self)
        main_sizer.Add(self.method_view, 1, wx.EXPAND | wx.ALL, 0)
        self.SetSizer(main_sizer)

        self.series = series

        self.method_view.method_type_combo.AppendItems(["ABC"])
