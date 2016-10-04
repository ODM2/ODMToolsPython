import wx


class WizardVariableView(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # Create components
        header_text = wx.StaticText(self, label="Variable")
        static_line = wx.StaticLine(self, size=(-1, 12))

        required_static_box_sizer = wx.StaticBoxSizer(box=wx.StaticBox(self, label="Required Fields"), orient=wx.VERTICAL)
        variable_code_text = wx.StaticText(self, label="Variable Code")
        self.variable_code_text_ctrl = wx.TextCtrl(self)
        variable_name_text = wx.StaticText(self, label="Variable Name")
        self.variable_name_combo = wx.ComboBox(self, choices=["---"], style=wx.CB_READONLY | wx.CB_SORT)
        variable_type_text = wx.StaticText(self, label="Variable Type")
        self.variable_type_combo = wx.ComboBox(self, choices=["---"], style=wx.CB_READONLY | wx.CB_SORT)
        no_data_value_text = wx.StaticText(self, label="No Data Value")
        self.no_data_value_text_ctrl = wx.TextCtrl(self, value="-9999")

        optional_static_box_sizer = wx.StaticBoxSizer(box=wx.StaticBox(self, label="Optional Fields"), orient=wx.VERTICAL)
        speciation_text = wx.StaticText(self, label="Speciation")
        self.speciation_combo = wx.ComboBox(self, choices=["---"], style=wx.CB_READONLY | wx.CB_SORT)
        definition_text = wx.StaticText(self, label="Definition")
        self.definition_text_ctrl = wx.TextCtrl(self, size=(-1, 75))

        # Style Components
        font = wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD)
        header_text.SetFont(font)
        self.variable_name_combo.SetSelection(0)
        self.speciation_combo.SetSelection(0)
        self.variable_type_combo.SetSelection(0)

        # Add components to sizer
        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        row_sizer.Add(variable_code_text, 0, wx.EXPAND)
        row_sizer.Add(self.variable_code_text_ctrl, 1, wx.EXPAND | wx.LEFT, 30)
        required_static_box_sizer.Add(row_sizer, 1, wx.EXPAND | wx.ALL, 5)

        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        row_sizer.Add(variable_name_text, 0, wx.EXPAND)
        row_sizer.Add(self.variable_name_combo, 1, wx.EXPAND | wx.LEFT, 27)
        required_static_box_sizer.Add(row_sizer, 1, wx.EXPAND | wx.ALL, 5)

        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        row_sizer.Add(variable_type_text, 0, wx.EXPAND)
        row_sizer.Add(self.variable_type_combo, 1, wx.EXPAND | wx.LEFT, 33)
        required_static_box_sizer.Add(row_sizer, 1, wx.EXPAND | wx.ALL, 5)

        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        row_sizer.Add(no_data_value_text, 0, wx.EXPAND)
        row_sizer.Add(self.no_data_value_text_ctrl, 1, wx.EXPAND | wx.LEFT, 29)
        required_static_box_sizer.Add(row_sizer, 1, wx.EXPAND | wx.ALL, 5)

        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        row_sizer.Add(speciation_text, 0, wx.EXPAND)
        row_sizer.Add(self.speciation_combo, 1, wx.EXPAND | wx.LEFT, 48)
        optional_static_box_sizer.Add(row_sizer, 0, wx.EXPAND | wx.ALL, 5)

        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        row_sizer.Add(definition_text, 0, wx.EXPAND)
        row_sizer.Add(self.definition_text_ctrl, 1, wx.EXPAND | wx.LEFT, 52)
        optional_static_box_sizer.Add(row_sizer, 1, wx.EXPAND | wx.ALL, 5)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(header_text, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        main_sizer.Add(static_line, 0, wx.EXPAND | wx.TOP, 5)
        main_sizer.Add(required_static_box_sizer, 0, wx.EXPAND | wx.TOP, 10)
        main_sizer.Add(optional_static_box_sizer, 0, wx.EXPAND | wx.TOP, 10)
        self.SetSizer(main_sizer)
