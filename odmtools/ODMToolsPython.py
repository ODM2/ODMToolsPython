#!/usr/bin/python
import os
import sys

this_file = os.path.realpath(__file__)
directory = os.path.dirname(os.path.dirname(this_file))
sys.path.insert(0, directory)


import wx
from gui import frmODMToolsMain


def create(parent):
    return frmODMToolsMain.create(parent)

if __name__ == '__main__':
    app = wx.App(False)
    frame = create(None)
    frame.Show()

    #import wx.lib.inspection
    #wx.lib.inspection.InspectionTool().Show()

    app.MainLoop()









