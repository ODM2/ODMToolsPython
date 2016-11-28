import wx


class NewFlagValuesView(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title="Flag Values", style=wx.FRAME_FLOAT_ON_PARENT | wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)

        panel = wx.Panel(self)
        content_panel = wx.Panel(panel)
        bottom_panel = wx.Panel(panel)

        ##########################################
        # CONTENT PANEL
        ##########################################

        annotation_title = wx.StaticText(content_panel, label="Annotation")
        self.annotation_combo = wx.ComboBox(content_panel, style=wx.CB_READONLY )#| wx.CB_SORT)
        code_title = wx.StaticText(content_panel, label="Code")
        self.code_textbox = wx.TextCtrl(content_panel, size=(100, -1))
        text_title = wx.StaticText(content_panel, label="Text")
        self.text_textbox = wx.TextCtrl(content_panel)
        link_text = wx.StaticText(content_panel, label="Link")
        self.link_textbox = wx.TextCtrl(content_panel)

        content_panel_sizer = wx.BoxSizer(wx.VERTICAL)
        content_panel_sizer.Add(annotation_title, 0, wx.EXPAND | wx.ALL ^ wx.BOTTOM, 10)
        content_panel_sizer.Add(self.annotation_combo, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        content_panel_sizer.Add(code_title, 0, wx.EXPAND | wx.ALL ^ wx.BOTTOM, 10)
        content_panel_sizer.Add(self.code_textbox, 0, wx.LEFT | wx.RIGHT, 10)
        content_panel_sizer.Add(text_title, 0, wx.EXPAND | wx.ALL ^ wx.BOTTOM, 10)
        content_panel_sizer.Add(self.text_textbox , 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        content_panel_sizer.Add(link_text, 0, wx.EXPAND | wx.ALL ^ wx.BOTTOM, 10)
        content_panel_sizer.Add(self.link_textbox, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)

        content_panel.SetSizer(content_panel_sizer)

        ##########################################
        # BOTTOM PANEL
        ##########################################

        self.ok_button = wx.Button(bottom_panel, label="OK")
        self.cancel_button = wx.Button(bottom_panel, label="CANCEL")
        static_line = wx.StaticLine(bottom_panel)
        self.cancel_button.SetDefault()

        bottom_panel_sizer = wx.BoxSizer(wx.VERTICAL)
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer.AddSpacer((0, 0), 1, wx.EXPAND, 2)
        button_sizer.Add(self.ok_button, 0, wx.EXPAND | wx.ALL ^ wx.RIGHT, 5)
        button_sizer.Add(self.cancel_button, 0, wx.EXPAND | wx.ALL, 5)

        bottom_panel_sizer.Add(static_line, 0, wx.EXPAND)
        bottom_panel_sizer.Add(button_sizer, 0, wx.ALIGN_RIGHT)

        bottom_panel.SetSizer(bottom_panel_sizer)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(content_panel, 1, wx.EXPAND | wx.ALL, 0)
        main_sizer.Add(bottom_panel, 0, wx.EXPAND | wx.ALL, 0)

        panel.SetSizer(main_sizer)
        main_sizer.Fit(self)
        self.SetSize((400, 300))



