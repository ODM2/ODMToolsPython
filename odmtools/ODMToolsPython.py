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

    from collections import defaultdict
    from gc import get_objects

    before = defaultdict(int)
    after = defaultdict(int)
    for i in get_objects():
        before[type(i)] += 1

    leaked_things = [[x] for x in range(10)]
    for i in get_objects():
        after[type(i)] += 1

    print "Results!!!!"
    print [(k, after[k] - before[k]) for k in after if after[k] - before[k]]









