import wx
from odmtools.view.WizardVariableView import WizardVariableView
from wx.wizard import WizardPageSimple
from odm2api.ODM2.models import Variables as Variable


class WizardVariableController(WizardPageSimple):
    def __init__(self, parent, service_manager, current_variable):
        WizardPageSimple.__init__(self, parent)

        self.service_manager = service_manager
        self.current_variable = current_variable
        self.all_variables = []

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.variable_view = WizardVariableView(self)
        main_sizer.Add(self.variable_view, 1, wx.EXPAND | wx.RIGHT, -16)
        self.SetSizer(main_sizer)

        table_columns = ["Code", "Name", "Speciation", "DataType", "NoDataValue", "ID"]
        self.variable_view.variable_table.set_columns(table_columns)
        self.on_current_radio(None)

        self.__fetch_data()
        self.select_current_variable()

        self.variable_view.current_variable_radio.Bind(wx.EVT_RADIOBUTTON, self.on_current_radio)
        self.variable_view.existing_variable_radio.Bind(wx.EVT_RADIOBUTTON, self.on_existing_radio)
        self.variable_view.create_variable_radio.Bind(wx.EVT_RADIOBUTTON, self.on_create_radio)

    def select_current_variable(self):
        if self.current_variable is None:
            return

        index = -1
        for i in range(len(self.all_variables)):
            if self.all_variables[i].VariableID == self.current_variable.VariableID:
                index = i
                break

        if index >= 0:
            self.variable_view.variable_table.Select(index)

    def on_current_radio(self, event):
        self.variable_view.variable_table.Enable(False)
        self.__enable_create_variable_section(False)

        if event:
            event.Skip()

    def on_create_radio(self, event):
        self.variable_view.variable_table.Enable(False)
        self.__enable_create_variable_section(True)

        if event:
            event.Skip()

    def on_existing_radio(self, event):
        self.variable_view.variable_table.Enable(True)
        self.__enable_create_variable_section(False)
        self.variable_view.variable_table.SetFocus()

        if event:
            event.Skip()

    def __enable_create_variable_section(self, active):
        if not isinstance(active, bool):
            raise Exception("active must be type bool")

        self.variable_view.variable_code_text_ctrl.Enable(active)
        self.variable_view.variable_name_combo.Enable(active)
        self.variable_view.variable_type_combo.Enable(active)
        self.variable_view.no_data_value_text_ctrl.Enable(active)
        self.variable_view.speciation_combo.Enable(active)
        self.variable_view.definition_text_ctrl.Enable(active)

    def __fetch_data(self):
        self.__populate_variable_table()

        series_service = self.service_manager.get_series_service()
        name_list = [x.Term for x in series_service.get_variable_name_cvs()]
        var_unit = [x.UnitsName for x in series_service.get_units()]
        spec_list = [x.Term for x in series_service.get_speciation_cvs()]

        self.variable_view.variable_name_combo.AppendItems(name_list)
        self.variable_view.speciation_combo.AppendItems(spec_list)
        self.variable_view.variable_type_combo.AppendItems(var_unit)

    def __populate_variable_table(self):
        series_serivce = self.service_manager.get_series_service()
        self.all_variables = series_serivce.get_all_variables()
        data = []
        for var in self.all_variables:
            data.append([var.VariableCode,
                         var.VariableNameCV,
                         var.SpeciationCV,
                         var.VariableTypeCV,
                         var.NoDataValue,
                         var.VariableID])

        self.variable_view.variable_table.set_table_content(data=data)

    def get_variable(self):
        if self.variable_view.current_variable_radio.GetValue():
            return self.current_variable

        if self.variable_view.existing_variable_radio.GetValue():
            return self.__select_existing_variable()

        if self.variable_view.create_variable_radio.GetValue():
            return self.__create_new_variable()

        return None

    def __select_existing_variable(self):
        index = self.variable_view.variable_table.GetFirstSelected()
        return self.all_variables[index]

    def __create_new_variable(self):
        v = Variable()
        v.code = self.variable_view.variable_code_text_ctrl.GetValue() if self.variable_view.variable_code_text_ctrl.GetValue() <> "" else None
        v.name = self.variable_view.variable_name_combo.GetValue() if self.variable_view.variable_name_combo.GetValue() <> "" else None
        v.speciation = self.variable_view.speciation_combo.GetValue() if self.variable_view.speciation_combo.GetValue() <> "" else None
        v.variable_unit = self.service_manager.get_series_service()
        v.no_data_value = self.variable_view.no_data_value_text_ctrl.GetValue() if self.variable_view.no_data_value_text_ctrl.GetValue() <> "" else None

        return v





