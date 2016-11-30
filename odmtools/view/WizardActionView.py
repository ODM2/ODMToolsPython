import wx
from odmtools.view.CustomListCtrl import CustomListCtrl
import wx.lib.scrolledpanel


class WizardActionView(wx.lib.scrolledpanel.ScrolledPanel):
    def __init__(self, parent):
        wx.lib.scrolledpanel.ScrolledPanel.__init__(self, parent)

        # Header
        header_text = wx.StaticText(self, label="Action")
        static_line = wx.StaticLine(self, size=(-1, 12))

        font = wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD)
        header_text.SetFont(font)

        # REQUIRED FIELDS
        required_static_box_sizer = wx.StaticBoxSizer(box=wx.StaticBox(self, label="Required Fields"), orient=wx.VERTICAL)
        affiliations_text = wx.StaticText(self, label="Affiliations")
        self.affiliations_table = CustomListCtrl(self)

        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        row_sizer.Add(affiliations_text, 0, wx.EXPAND)
        required_static_box_sizer.Add(row_sizer, 0, wx.EXPAND | wx.ALL, 5)

        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        row_sizer.Add(self.affiliations_table, 1, wx.EXPAND)
        required_static_box_sizer.Add(row_sizer, 0, wx.EXPAND | wx.ALL, 5)

        # OPTIONAL FIELDS
        optional_static_box_sizer = wx.StaticBoxSizer(box=wx.StaticBox(self, label="Optional Fields"), orient=wx.VERTICAL)
        action_file_link_text = wx.StaticText(self, label="Action File Link")
        action_file_link_text_box = wx.TextCtrl(self)
        description_text = wx.StaticText(self, label="Description")
        description_text_box = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        role_description_text = wx.StaticText(self, label="Role Description")
        role_description_text_box = wx.TextCtrl(self, style=wx.TE_MULTILINE)

        flex_grid_sizer = wx.FlexGridSizer(rows=3, cols=2, vgap=9, hgap=25)

        flex_grid_sizer.AddMany([(action_file_link_text), (action_file_link_text_box, 1, wx.EXPAND),
                                 (description_text), (description_text_box, 1, wx.EXPAND),
                                 (role_description_text), (role_description_text_box, 1, wx.EXPAND)
                                 ])

        flex_grid_sizer.AddGrowableRow(1, 1)
        flex_grid_sizer.AddGrowableCol(1, 1)

        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        row_sizer.Add(flex_grid_sizer, 1, wx.EXPAND)
        optional_static_box_sizer.Add(row_sizer, 0, wx.EXPAND | wx.ALL, 5)

        master_sizer = wx.BoxSizer(wx.VERTICAL)
        master_sizer.Add(header_text, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        master_sizer.Add(static_line, 0, wx.EXPAND | wx.TOP, 5)
        master_sizer.Add(required_static_box_sizer, 0, wx.EXPAND | wx.TOP, 5)
        master_sizer.Add(optional_static_box_sizer, 0, wx.EXPAND | wx.TOP, 5)

        self.SetSizer(master_sizer)
        # master_sizer.Fit(self)
