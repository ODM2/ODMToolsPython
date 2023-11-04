__author__ = 'Stephanie'
import wx
from wx.adv import AboutBox, AboutDialogInfo
from wx.lib.wordwrap import wordwrap
from odmtools.meta import data

class frmAbout(wx.Dialog):
    def __init__(self, parent):
        self.parent = parent
        info = AboutDialogInfo()
        info.Name = data.app_name
        info.Version = data.version
        info.Copyright = data.copyright
        info.Description = wordwrap(data.description, 350, wx.ClientDC(parent))
        info.WebSite = data.website
        info.Developers = data.developers
        info.License = wordwrap(data.license, 500, wx.ClientDC(parent))
        # Then we call wx.AboutBox giving it that info object
        AboutBox(info)
        #self.ShowModal()