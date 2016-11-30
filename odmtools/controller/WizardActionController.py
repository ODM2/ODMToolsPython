import wx
from odmtools.view.WizardActionView import WizardActionView
from wx.wizard import WizardPageSimple


class WizardActionController(WizardPageSimple):
    def __init__(self, parent, affiliations):
        WizardPageSimple.__init__(self, parent)
        self.action_view = WizardActionView(self)
        self.affiliations = affiliations

        master_sizer = wx.BoxSizer(wx.VERTICAL)
        master_sizer.Add(self.action_view, 1, wx.EXPAND | wx.RIGHT, 0)
        self.SetSizer(master_sizer)

        if self.affiliations is None:
            return
        # Populate table with the affiliations


if __name__ == '__main__':
    app = wx.App(False)
    controller = WizardActionController(None, None)
    controller.Show()
    app.MainLoop()