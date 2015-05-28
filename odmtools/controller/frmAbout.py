__author__ = 'Stephanie'
import wx
from wx import AboutBox, AboutDialogInfo, ClientDC
from wx.lib.wordwrap import wordwrap
from odmtools.meta import data

class frmAbout(wx.Dialog):
    def __init__(self, parent):
        self.parent = parent
        info = AboutDialogInfo()
        info.Name = data.app_name
        info.Version = data.version
        info.Copyright = data.copyright
        info.Description = wordwrap(data.description, 350, ClientDC(parent))
        info.WebSite = data.website
        info.Developers = data.developers
        info.License = wordwrap(data.license, 500, ClientDC(parent))
        # Then we call wx.AboutBox giving it that info object
        AboutBox(info)
        #self.ShowModal()