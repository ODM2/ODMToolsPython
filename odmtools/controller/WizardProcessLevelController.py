import wx
from odmtools.view.WizardProcessLevelView import WizardProcessLevelView
from wx.wizard import WizardPageSimple


class WizardProcessLevelController(WizardPageSimple):
    def __init__(self, parent):
        WizardPageSimple.__init__(self, parent)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.processing_level_view = WizardProcessLevelView(self)
        main_sizer.Add(self.processing_level_view, 1, wx.EXPAND | wx.RIGHT, -16)
        self.SetSizer(main_sizer)

        table_columns = ["Code", "Definition", "Explanation"]
        self.processing_level_view.existing_process_table.set_columns(table_columns)