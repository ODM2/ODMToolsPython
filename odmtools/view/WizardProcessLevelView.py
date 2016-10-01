import wx


class WizardProcessLevelView(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # Create components
        header_text = wx.StaticText(self, label="Processing Level")
        static_line = wx.StaticLine(self, size=(-1, 12))
        required_static_box_sizer = wx.StaticBoxSizer(box=wx.StaticBox(self, label="Required Fields"), orient=wx.VERTICAL)
        level_code = wx.StaticText(self, label="Processing Level Code")
        self.level_code_text_ctrl = wx.TextCtrl(self)
        optional_static_box_sizer = wx.StaticBoxSizer(box=wx.StaticBox(self, label="Optional Fields"), orient=wx.VERTICAL)
        definition_text = wx.StaticText(self, label="Definition")
        self.definition_text_ctrl = wx.TextCtrl(self, size=(-1, 75))
        explanation_text = wx.StaticText(self, label="Explanation")
        self.explanation_text_ctrl = wx.TextCtrl(self, size=(-1, 75))

        # Style components
        font = wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD)
        header_text.SetFont(font)

        # Add components to sizer
        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        row_sizer.Add(level_code, 0, wx.EXPAND)
        row_sizer.Add(self.level_code_text_ctrl, 1, wx.EXPAND | wx.LEFT, 30)
        required_static_box_sizer.Add(row_sizer, 1, wx.EXPAND | wx.ALL, 5)

        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        row_sizer.Add(definition_text, 0, wx.EXPAND)
        row_sizer.Add(self.definition_text_ctrl, 1, wx.EXPAND | wx.LEFT, 95)
        optional_static_box_sizer.Add(row_sizer, 1, wx.EXPAND | wx.ALL, 5)

        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        row_sizer.Add(explanation_text, 0, wx.EXPAND)
        row_sizer.Add(self.explanation_text_ctrl, 1, wx.EXPAND | wx.LEFT, 85)
        optional_static_box_sizer.Add(row_sizer, 1, wx.EXPAND | wx.ALL, 5)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(header_text, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        main_sizer.Add(static_line, 0, wx.EXPAND | wx.TOP, 5)
        main_sizer.Add(required_static_box_sizer, 0, wx.EXPAND | wx.TOP, 10)
        main_sizer.Add(optional_static_box_sizer, 0, wx.EXPAND | wx.TOP, 10)
        self.SetSizer(main_sizer)
