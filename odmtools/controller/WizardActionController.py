import wx
from odmtools.view.WizardActionView import WizardActionView
from wx.wizard import WizardPageSimple
from odm2api.ODM2.models import Affiliations


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
        self.populate_affiliations_table()

    def populate_affiliations_table(self):
        """
        self.affiliations must be a list affiliations
        :return:
        """
        if not isinstance(self.affiliations, list):
            return
        if not len(self.affiliations) and not isinstance(self.affiliations[0], Affiliations):
            return

        data = []
        for affiliation in self.affiliations:
            data.append([
                affiliation.PersonObj.PersonFirstName + " " + affiliation.PersonObj.PersonLastName,
                affiliation.OrganizationObj.OrganizationName
            ])

        columns = ["Person", "Organization"]
        self.action_view.affiliations_table.set_columns(columns)
        self.action_view.affiliations_table.set_table_content(data)

    def get_action(self):
        index = self.action_view.affiliations_table.GetFirstSelected()
        return self.affiliations[index]


if __name__ == '__main__':
    app = wx.App(False)
    controller = WizardActionController(None, None)
    controller.Show()
    app.MainLoop()