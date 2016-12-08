import wx
from odmtools.view.CustomCollapsiblePanel import CustomCollapsiblePanel
from wx.lib.scrolledpanel import ScrolledPanel


class NewFlagValuesView(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title="Flag Values", style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)

        panel = wx.Panel(self)
        content_panel = ScrolledPanel(panel)
        bottom_panel = wx.Panel(panel)

        ##########################################
        # CONTENT PANEL
        ##########################################
        content_panel.SetupScrolling()

        annotation_title = wx.StaticText(content_panel, label="Annotation")
        self.collapsible_panel = CustomCollapsiblePanel(content_panel, title="Panel 1", expand=0, use_combo=True, combo_trigger_item="New Annontation")
        self.annotation_combo = self.collapsible_panel.interactive_item

        code_title = wx.StaticText(self.collapsible_panel, label="Code")
        self.code_textbox = wx.TextCtrl(self.collapsible_panel, size=(100, -1))
        text_title = wx.StaticText(self.collapsible_panel, label="Text")
        self.text_textbox = wx.TextCtrl(self.collapsible_panel)
        link_text = wx.StaticText(self.collapsible_panel, label="Link")
        self.link_textbox = wx.TextCtrl(self.collapsible_panel)

        sizer = wx.BoxSizer(wx.VERTICAL)
        content_panel_sizer = wx.BoxSizer(wx.VERTICAL)
        content_panel_sizer.Add(code_title, 0, wx.EXPAND | wx.ALL ^ wx.BOTTOM, 10)
        content_panel_sizer.Add(self.code_textbox, 0, wx.LEFT | wx.RIGHT, 10)
        content_panel_sizer.Add(text_title, 0, wx.EXPAND | wx.ALL ^ wx.BOTTOM, 10)
        content_panel_sizer.Add(self.text_textbox , 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        content_panel_sizer.Add(link_text, 0, wx.EXPAND | wx.ALL ^ wx.BOTTOM, 10)
        content_panel_sizer.Add(self.link_textbox, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)

        self.collapsible_panel.finish_layout()

        sizer.Add(annotation_title, 0, wx.EXPAND | wx.ALL ^ wx.BOTTOM, 10)
        sizer.Add(self.collapsible_panel, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        content_panel.SetSizer(sizer)

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
        self.SetSize((400, 150))



