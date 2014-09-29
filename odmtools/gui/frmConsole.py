"""
    ODMTools Console

"""
import wx
from wx.py.crust import CrustFrame, Crust
from wx.py.frame import Frame, ShellFrameMixin

__author__ = 'Jacob'
class ModifiedFrame(Frame):
    """Override standard PyCrust frame in order to remove exit and about page"""
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)

        self.Unbind(wx.EVT_MENU, id=wx.ID_ABOUT)

        ## Remove unneeded menu items ##
        def remove(id):
            mb = self.fileMenu.GetMenuBar()
            subMenuItem = mb.FindItemById(id)
            subMenu = subMenuItem.GetMenu()
            subMenu.RemoveItem(subMenuItem)
        '''try:
            remove(wx.ID_EXIT)
        except Exception as e :
            print e
            remove(253)'''
        remove(wx.ID_ABOUT)

class ODMConsole(ModifiedFrame, ShellFrameMixin):
    def __init__(self, *args, **kwargs):
        ModifiedFrame.__init__(self, title='ODMTools', pos=wx.DefaultPosition,
                               style=wx.NO_BORDER, shellName='PyCrust')
        ShellFrameMixin.__init__(self, config=None, dataDir=None)

        self.SetSize((400, 300))

        intro = ''
        if 'version' in kwargs:
            intro = 'ODMTools Python Console %s ' % kwargs['version']
        else:
            intro = 'ODMTools Python Console'
        self.SetStatusText(intro.replace('\n', ', '))


        kwargs['rootObject'] = None
        kwargs['rootLabel'] = None
        kwargs['rootIsNamespace'] = True
        kwargs['locals'] = None
        kwargs['InterpClass'] = None
        kwargs['startupScript'] = self.startupScript
        kwargs['execStartupScript'] = self.execStartupScript
        self.crust = Crust(self, intro=intro)
        self.shellName = self.crust.shell
        self.shell = self.crust.shell

        # Override the filling so that status messages go to the status bar.
        self.crust.filling.tree.setStatusText = self.SetStatusText

        # Override the shell so that status messages go to the status bar.
        self.shell.setStatusText = self.SetStatusText

        self.shell.SetFocus()
        self.LoadSettings()


    def OnClose(self, event):
        """Event handler for closing."""
        self.SaveSettings()
        self.crust.shell.destroy()
        self.Destroy()


    def OnAbout(self, event):
        """Display an About window."""
        title = 'About PyCrust'
        text = "Test!"
        dialog = wx.MessageDialog(self, text, title, wx.OK | wx.ICON_INFORMATION)
        dialog.ShowModal()
        dialog.Destroy()


    def ToggleTools(self):
        """Toggle the display of the filling and other tools"""
        return self.crust.ToggleTools()


    def ToolsShown(self):
        return self.crust.ToolsShown()


    def OnHelp(self, event):
        """Show a help dialog."""
        ShellFrameMixin.OnHelp(self, event)


    def LoadSettings(self):
        if self.config is not None:
            ShellFrameMixin.LoadSettings(self)
            Frame.LoadSettings(self, self.config)
            self.crust.LoadSettings(self.config)


    def SaveSettings(self, force=False):
        if self.config is not None:
            ShellFrameMixin.SaveSettings(self, force)
            if self.autoSaveSettings or force:
                Frame.SaveSettings(self, self.config)
                self.crust.SaveSettings(self.config)


    def DoSaveSettings(self):
        if self.config is not None:
            self.SaveSettings(force=True)
            self.config.Flush()

