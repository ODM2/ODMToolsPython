import wx
from wx.wizard import WizardPageSimple
from odmtools.view.WizardMethodView import WizardMethodView
from odm2api.ODM2.models import Methods as Method


class WizardMethodController(WizardPageSimple):
    def __init__(self, parent, series_service, current_method=None):
        WizardPageSimple.__init__(self, parent)

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.method_view = WizardMethodView(self)
        main_sizer.Add(self.method_view, 1, wx.EXPAND | wx.RIGHT, -16)  # Sufficient to hide the scroll bar
        self.SetSizer(main_sizer)

        self.series_service = series_service
        table_columns = ["ID", "Descriptions", "Link", "Code", "Type"]
        self.cv_types = []
        self.method_view.existing_method_table.set_columns(table_columns)

        self.on_auto_radio(None)

        self.all_methods = []
        self.current_method_in_series = current_method  # Not the same as the selected method in the table
        self.__populate_table()
        self.select_current_method()
        self.method_view.method_type_combo.AppendItems(self.cv_types)
        self.on_existing_method_radio(None)

        self.method_view.auto_method_radio.Bind(wx.EVT_RADIOBUTTON, self.on_auto_radio)
        self.method_view.existing_method_radio.Bind(wx.EVT_RADIOBUTTON, self.on_existing_method_radio)
        self.method_view.create_method_radio.Bind(wx.EVT_RADIOBUTTON, self.on_create_method_radio)

    def select_current_method(self):
        if self.current_method_in_series is None:
            return

        if self.current_method_in_series not in self.all_methods:
            return  # the current method is not in the table

        index = self.all_methods.index(self.current_method_in_series)
        self.method_view.existing_method_table.Focus(index)
        self.method_view.existing_method_table.Select(index)

    def on_auto_radio(self, event):
        self.method_view.existing_method_table.Disable()
        self.enable_create_method_section(False)

    def on_existing_method_radio(self, event):
        self.method_view.existing_method_table.Enable()
        self.enable_create_method_section(False)

    def enable_create_method_section(self, active):
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
        self.enable_create_method_section(True)

    def __populate_table(self):
        self.all_methods = self.series_service.get_all_methods()
        data = []
        for meth in self.all_methods:
            data.append([
                meth.MethodID, meth.MethodDescription,
                meth.MethodLink, meth.MethodCode,
                meth.MethodTypeCV
            ])

            if meth.MethodTypeCV not in self.cv_types:
                self.cv_types.append(meth.MethodTypeCV)

        self.method_view.existing_method_table.set_table_content(data=data)

    def getMethod(self):
        if self.method_view.auto_method_radio.GetValue():
            return self.__auto_generate_a_method()

        if self.method_view.existing_method_radio.GetValue():
            return self.__select_existing_method()

        if self.method_view.create_method_radio.GetValue():
            return self.__create_new_method()

        return None

    def __auto_generate_a_method(self):
        code = "odmtools"
        method = self.series_service.get_method_by_code(method_code=code)
        if method is None:
            method = Method()
            method.MethodCode = code
            method.MethodDescription = "Values derived from ODM Tools Python"
        return method

    def __select_existing_method(self):
        index = self.method_view.existing_method_table.GetFirstSelected()
        return self.all_methods[index]

    def __create_new_method(self):
        code = self.method_view.method_code_text_ctrl.GetValue()
        name = self.method_view.method_name_text_ctrl.GetValue()
        typeCV = self.method_view.method_type_combo.GetValue()
        # organization = self.method_view.organization_combo.GetValue()
        link = self.method_view.method_link_text_ctrl.GetValue()
        description = self.method_view.description_text_ctrl.GetValue()

        method = Method()
        method.MethodCode = code
        method.MethodName = name
        method.MethodTypeCV = typeCV
        method.MethodLink = link
        method.MethodDescription = description

        return method
