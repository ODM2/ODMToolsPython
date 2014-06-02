from Gui import frmODMToolsMain
import wx


def create(parent):
    return frmODMToolsMain.create(parent)

if __name__ == '__main__':
    app = wx.App(False)
    frame = create(None)
    frame.Show()

    #import wx.lib.inspection
    #wx.lib.inspection.InspectionTool().Show()

    app.MainLoop()









