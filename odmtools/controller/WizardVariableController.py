import wx
from odmtools.view.WizardVariableView import WizardVariableView
from wx.wizard import WizardPageSimple


class WizardVariableController(WizardPageSimple):
    def __init__(self, parent, service_manager):
        WizardPageSimple.__init__(self, parent)

        self.service_manager = service_manager
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.variable_view = WizardVariableView(self)
        main_sizer.Add(self.variable_view, 1, wx.EXPAND | wx.RIGHT, -16)
        self.SetSizer(main_sizer)

        table_columns = ["Code", "Name", "Speciation", "Units",
                         "Sample Medium", "Value Type", "IsRegular", "Time Support",
                         "Time Units", "DataType", "Genaral Category", "NoDataValue"]
        self.variable_view.variable_table.set_columns(table_columns)

        self.__fetch_data()

    def __fetch_data(self):
        cv_service = self.service_manager.get_cv_service()
        name_list = [x.term for x in cv_service.get_variable_name_cvs()]
        var_unit = [x.name for x in cv_service.get_units_names()]
        spec_list = [x.term for x in cv_service.get_speciation_cvs()]

        self.variable_view.variable_name_combo.AppendItems(name_list)
        self.variable_view.speciation_combo.AppendItems(spec_list)
        self.variable_view.variable_type_combo.AppendItems(var_unit)
