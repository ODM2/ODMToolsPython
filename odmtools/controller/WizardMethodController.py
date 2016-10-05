import wx
from wx.wizard import WizardPageSimple
from odmtools.view.WizardMethodView import WizardMethodView


class WizardMethodController(WizardPageSimple):
    def __init__(self, parent, series):
        WizardPageSimple.__init__(self, parent)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.method_view = WizardMethodView(self)
        main_sizer.Add(self.method_view, 1, wx.EXPAND | wx.RIGHT, -16)  # Sufficient to hide the scroll bar
        self.SetSizer(main_sizer)

        self.series = series
        table_columns = ["Descriptions", "Link", "ID"]
        self.method_view.existing_method_table.set_columns(table_columns)
        self.method_view.method_type_combo.AppendItems(["ABC"])
