import wx
from wx.wizard import WizardPageSimple
from odmtools.view.WizardMethodView import WizardMethodView


class WizardMethodController(WizardPageSimple):
    def __init__(self, parent, series_service):
        WizardPageSimple.__init__(self, parent)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.method_view = WizardMethodView(self)
        main_sizer.Add(self.method_view, 1, wx.EXPAND | wx.RIGHT, -16)  # Sufficient to hide the scroll bar
        self.SetSizer(main_sizer)

        self.series_service = series_service
        table_columns = ["Descriptions", "Link", "ID"]
        self.method_view.existing_method_table.set_columns(table_columns)
        self.method_view.method_type_combo.AppendItems(["ABC"])
        self.__fetch_data()

    def __fetch_data(self):
        methods = self.series_service.get_all_methods()
        data = []
        for meth in methods:
            data.append([
                meth.description,
                meth.link,
                meth.id
            ])

        self.method_view.existing_method_table.set_table_content(data=data)
