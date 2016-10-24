import wx
from wx.wizard import WizardPageSimple
from odmtools.view.WizardMethodView import WizardMethodView
from odm2api.ODM2.models import Methods as Method


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
        self.on_auto_radio(None)

        self.method_view.auto_method_radio.Bind(wx.EVT_RADIOBUTTON, self.on_auto_radio)
        self.method_view.existing_method_radio.Bind(wx.EVT_RADIOBUTTON, self.on_existing_method_radio)
        self.method_view.create_method_radio.Bind(wx.EVT_RADIOBUTTON, self.on_create_method_radio)

        self.__fetch_data()

    def on_auto_radio(self, event):
        self.method_view.existing_method_table.Enable(False)
        self.__set_create_method_section_(False)

    def on_existing_method_radio(self, event):
        self.method_view.existing_method_table.Enable()
        self.__set_create_method_section_(False)

    def __set_create_method_section_(self, active):
        if not isinstance(active, bool):
            raise Exception("active must be type bool")

        self.method_view.method_code_text_ctrl.Enable(active)
        self.method_view.method_name_text_ctrl.Enable(active)
        self.method_view.method_type_combo.Enable(active)
        self.method_view.organization_combo.Enable(active)
        self.method_view.method_link_text_ctrl.Enable(active)
        self.method_view.description_text_ctrl.Enable(active)

    def on_create_method_radio(self, event):
        self.method_view.existing_method_table.Disable()
        self.__set_create_method_section_(True)

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

    def getMethod(self):
        m = Method()
        if self.method_view.auto_method_radio.GetValue():
            description = "Values derived from ODM Tools Python"
            m = self.series_service.get_method_by_code(description)
            if m is None:
                m = Method()
                m.description = description
        elif self.method_view.existing_method_radio.GetValue():
            index = self.method_view.existing_method_table.GetFirstSelected()
            desc = self.method_view.existing_method_table.GetItem(index, 0).GetText()

            m = self.series_service.get_method_by_code(desc)
        elif self.method_view.create_method_radio.GetValue():
            m.description = self.method_view.description_text_ctrl.GetValue()


        return m
