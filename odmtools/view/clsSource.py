# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc


###########################################################################
## Class dlgCreateSource
###########################################################################

class clsSource(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                           size=wx.Size(493, 418), style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        sizerMain = wx.BoxSizer(wx.VERTICAL)

        sizerOrganization = wx.FlexGridSizer(0, 2, 0, 0)
        sizerOrganization.AddGrowableCol(1)
        sizerOrganization.AddGrowableRow(1)
        sizerOrganization.SetFlexibleDirection(wx.BOTH)
        sizerOrganization.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.lblOrg = wx.StaticText(self, wx.ID_ANY, u"Organization", wx.DefaultPosition, wx.DefaultSize,
                                    wx.ALIGN_RIGHT)
        self.lblOrg.Wrap(-1)
        sizerOrganization.Add(self.lblOrg, 0, wx.ALIGN_RIGHT | wx.ALL, 5)

        self.txtOrg = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        sizerOrganization.Add(self.txtOrg, 1, wx.ALL | wx.EXPAND, 5)

        self.lblDescrip = wx.StaticText(self, wx.ID_ANY, u"Description", wx.DefaultPosition, wx.DefaultSize,
                                        wx.ALIGN_RIGHT)
        self.lblDescrip.Wrap(-1)
        sizerOrganization.Add(self.lblDescrip, 0, wx.ALIGN_RIGHT | wx.ALL, 5)

        self.txtDescrip = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                      wx.TE_MULTILINE)
        sizerOrganization.Add(self.txtDescrip, 0, wx.ALL | wx.EXPAND, 5)

        self.lblLink = wx.StaticText(self, wx.ID_ANY, u"Link", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT)
        self.lblLink.Wrap(-1)
        sizerOrganization.Add(self.lblLink, 0, wx.ALIGN_RIGHT | wx.ALL, 5)

        self.txtLink = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        sizerOrganization.Add(self.txtLink, 0, wx.ALL | wx.EXPAND, 5)

        sizerMain.Add(sizerOrganization, 1, wx.EXPAND, 5)

        sizerContact = wx.FlexGridSizer(0, 4, 0, 0)
        sizerContact.AddGrowableCol(1)
        sizerContact.SetFlexibleDirection(wx.BOTH)
        sizerContact.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.lblName = wx.StaticText(self, wx.ID_ANY, u" Name", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT)
        self.lblName.Wrap(-1)
        sizerContact.Add(self.lblName, 0, wx.ALIGN_RIGHT | wx.ALL, 5)

        self.txtName = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        sizerContact.Add(self.txtName, 1, wx.ALL | wx.EXPAND, 5)

        self.lblPhone = wx.StaticText(self, wx.ID_ANY, u"Phone", wx.DefaultPosition, wx.DefaultSize, 0)
        self.lblPhone.Wrap(-1)
        sizerContact.Add(self.lblPhone, 0, wx.ALIGN_RIGHT | wx.ALL, 5)

        self.txtPhone = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        sizerContact.Add(self.txtPhone, 0, wx.ALL, 5)

        sizerMain.Add(sizerContact, 1, wx.EXPAND, 5)

        sizerAddress = wx.FlexGridSizer(0, 2, 0, 0)
        sizerAddress.AddGrowableCol(1)
        sizerAddress.SetFlexibleDirection(wx.BOTH)
        sizerAddress.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.lblEmail = wx.StaticText(self, wx.ID_ANY, u"            Email", wx.DefaultPosition, wx.DefaultSize, 0)
        self.lblEmail.Wrap(-1)
        sizerAddress.Add(self.lblEmail, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_RIGHT | wx.ALL, 5)

        self.txtEmail = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        sizerAddress.Add(self.txtEmail, 0, wx.ALL | wx.EXPAND, 5)

        self.lblAddress = wx.StaticText(self, wx.ID_ANY, u"Address", wx.DefaultPosition, wx.DefaultSize, 0)
        self.lblAddress.Wrap(-1)
        sizerAddress.Add(self.lblAddress, 0, wx.ALIGN_RIGHT | wx.ALL, 5)

        self.txtAddress = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        sizerAddress.Add(self.txtAddress, 0, wx.ALL | wx.EXPAND, 5)

        sizerMain.Add(sizerAddress, 1, wx.EXPAND, 5)

        sizerDetails = wx.FlexGridSizer(1, 6, 0, 0)
        sizerDetails.AddGrowableCol(1)
        sizerDetails.SetFlexibleDirection(wx.BOTH)
        sizerDetails.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.lblCity = wx.StaticText(self, wx.ID_ANY, u"City", wx.DefaultPosition, wx.DefaultSize, 0)
        self.lblCity.Wrap(-1)
        sizerDetails.Add(self.lblCity, 0, wx.ALIGN_RIGHT | wx.ALL, 5)

        self.txtCity = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        sizerDetails.Add(self.txtCity, 1, wx.ALL | wx.EXPAND, 5)

        self.lblState = wx.StaticText(self, wx.ID_ANY, u"State", wx.DefaultPosition, wx.DefaultSize, 0)
        self.lblState.Wrap(-1)
        sizerDetails.Add(self.lblState, 0, wx.ALIGN_RIGHT | wx.ALL, 5)

        self.txtState = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.txtState.SetMaxLength(2
                                   )
        sizerDetails.Add(self.txtState, 0, wx.ALL, 5)

        self.lblZip = wx.StaticText(self, wx.ID_ANY, u"ZipCode", wx.DefaultPosition, wx.DefaultSize, 0)
        self.lblZip.Wrap(-1)
        sizerDetails.Add(self.lblZip, 0, wx.ALIGN_RIGHT | wx.ALL, 5)

        self.txtZip = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.txtZip.SetMaxLength(10)
        sizerDetails.Add(self.txtZip, 0, wx.ALL, 5)

        sizerMain.Add(sizerDetails, 1, wx.EXPAND, 5)

        sizerCitation = wx.FlexGridSizer(0, 2, 0, 0)
        sizerCitation.AddGrowableCol(1)
        sizerCitation.SetFlexibleDirection(wx.BOTH)
        sizerCitation.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.lblCitation = wx.StaticText(self, wx.ID_ANY, u"          Citation", wx.DefaultPosition, wx.DefaultSize, 0)
        self.lblCitation.Wrap(-1)
        sizerCitation.Add(self.lblCitation, 0, wx.ALIGN_RIGHT | wx.ALL, 5)

        self.txtCitation = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        sizerCitation.Add(self.txtCitation, 0, wx.ALL | wx.EXPAND, 5)

        self.lblMetadata = wx.StaticText(self, wx.ID_ANY, u"Metadata", wx.DefaultPosition, wx.DefaultSize, 0)
        self.lblMetadata.Wrap(-1)
        sizerCitation.Add(self.lblMetadata, 0, wx.ALIGN_RIGHT | wx.ALL, 5)

        chMetaChoices = []
        self.chMeta = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, chMetaChoices, 0)
        self.chMeta.SetSelection(0)
        sizerCitation.Add(self.chMeta, 0, wx.ALL | wx.EXPAND, 5)

        sizerMain.Add(sizerCitation, 1, wx.EXPAND, 5)

        sizerButtons = wx.FlexGridSizer(0, 3, 0, 0)
        sizerButtons.AddGrowableCol(0)
        sizerButtons.SetFlexibleDirection(wx.BOTH)
        sizerButtons.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.pnlFiller = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        sizerButtons.Add(self.pnlFiller, 1, wx.EXPAND | wx.ALL, 5)

        self.btnOk = wx.Button(self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0)
        sizerButtons.Add(self.btnOk, 0, wx.ALL, 5)

        self.btnCancel = wx.Button(self, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0)
        sizerButtons.Add(self.btnCancel, 0, wx.ALL, 5)

        sizerMain.Add(sizerButtons, 1, wx.EXPAND, 5)

        self.SetSizer(sizerMain)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.btnOk.Bind(wx.EVT_BUTTON, self.onOkClick)
        self.btnCancel.Bind(wx.EVT_BUTTON, self.onCancelClick)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def onOkClick(self, event):
        event.Skip()

    def onCancelClick(self, event):
        event.Skip()


