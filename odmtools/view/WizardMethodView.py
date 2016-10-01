import wx


class WizardMethodView(wx.Panel):  # Rename this to page method view
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # Create components
        header_text = wx.StaticText(self, label="Method")
        static_line = wx.StaticLine(self, size=(-1, 12))

        required_static_box_sizer = wx.StaticBoxSizer(box=wx.StaticBox(self, label="Required Fields"), orient=wx.VERTICAL)
        method_code_text = wx.StaticText(self, label="Method Code")
        self.method_code_text_ctrl = wx.TextCtrl(self)
        method_name_text = wx.StaticText(self, label="Method Name")
        self.method_name_text_ctrl = wx.TextCtrl(self)
        method_type_text = wx.StaticText(self, label="Method Type")
        self.method_type_combo = wx.ComboBox(self)

        optional_static_box_sizer = wx.StaticBoxSizer(box=wx.StaticBox(self, label="Optional Fields"), orient=wx.VERTICAL)
        organization_text = wx.StaticText(self, label="Organization")
        self.organization_text_ctrl = wx.TextCtrl(self)
        method_link_text = wx.StaticText(self, label="Method Link")
        self.method_link_text_ctrl = wx.TextCtrl(self)
        description_text = wx.StaticText(self, label="Description")
        self.description_text_ctrl = wx.TextCtrl(self, size=(-1, 75))

        # Style Components
        font = wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD)
        header_text.SetFont(font)

        # Add components to sizer
        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        row_sizer.Add(method_code_text, 0, wx.EXPAND)
        row_sizer.Add(self.method_code_text_ctrl, 1, wx.EXPAND | wx.LEFT, 24)
        required_static_box_sizer.Add(row_sizer, 0, wx.EXPAND | wx.ALL, 5)

        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        row_sizer.Add(method_name_text, 0, wx.EXPAND)
        row_sizer.Add(self.method_name_text_ctrl, 1, wx.EXPAND | wx.LEFT, 20)
        required_static_box_sizer.Add(row_sizer, 0, wx.EXPAND | wx.ALL, 5)

        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        row_sizer.Add(method_type_text, 0, wx.EXPAND)
        row_sizer.Add(self.method_type_combo, 1, wx.EXPAND | wx.LEFT, 26)
        required_static_box_sizer.Add(row_sizer, 0, wx.EXPAND | wx.ALL, 5)

        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        row_sizer.Add(organization_text, 0, wx.EXPAND)
        row_sizer.Add(self.organization_text_ctrl, 1, wx.EXPAND | wx.LEFT, 27)
        optional_static_box_sizer.Add(row_sizer, 0, wx.EXPAND | wx.ALL, 5)

        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        row_sizer.Add(method_link_text, 0, wx.EXPAND)
        row_sizer.Add(self.method_link_text_ctrl, 1, wx.EXPAND | wx.LEFT, 27)
        optional_static_box_sizer.Add(row_sizer, 0, wx.EXPAND | wx.ALL, 5)

        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        row_sizer.Add(description_text, 0, wx.EXPAND)
        row_sizer.Add(self.description_text_ctrl, 1, wx.EXPAND | wx.LEFT, 34)
        optional_static_box_sizer.Add(row_sizer, 0, wx.EXPAND | wx.ALL, 5)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(header_text, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        main_sizer.Add(static_line, 0, wx.EXPAND | wx.TOP, 5)
        main_sizer.Add(required_static_box_sizer, 0, wx.EXPAND | wx.TOP, 10)
        main_sizer.Add(optional_static_box_sizer, 0, wx.EXPAND | wx.TOP, 10)
        self.SetSizer(main_sizer)