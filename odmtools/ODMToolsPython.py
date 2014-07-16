#!/usr/bin/python2
import os
import sys

this_file = os.path.realpath(__file__)
directory = os.path.dirname(os.path.dirname(this_file))
sys.path.insert(0, directory)


#from guppy import hpy
#h = hpy()
    

import wx
from gui import frmODMToolsMain


def create(parent):
    return frmODMToolsMain.create(parent)

def runODM():
    app = wx.App(False)
    frame = create(None)
    frame.Show()

    #import wx.lib.inspection
    #wx.lib.inspection.InspectionTool().Show()
   
    #before = h.heap()
    #print "Before: ", before
    
    app.MainLoop()
    
    #after = h.heap()
    #leftover = after - before
    
    #import pdb
    #pdb.set_trace()
    
    #print "After: ", after
    #print "Leftovers: ", leftover
    

    '''
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
    '''

if __name__ == '__main__':
    #from guppy import hpy
   # h = hpy()
    app = wx.App(False)
    frame = create(None)
    frame.Show()

    #import wx.lib.inspection
    #wx.lib.inspection.InspectionTool().Show()

    app.MainLoop()
    #print "HEAPY!", h.heap()

    '''
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
    '''








