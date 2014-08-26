#!/usr/local/bin/python

# ## Loading up information ####
import logging

from odmtools.common.logger import LoggerTool


tool = LoggerTool()
logger = tool.setupLogger(__name__, __name__ + '.log', 'w', logging.DEBUG)
logger.debug("Welcome to ODMTools Python. Please wait as system loads")
###############################

#import os
#import sys

'''
this_file = os.path.realpath(__file__)
directory = os.path.dirname(os.path.dirname(this_file))
sys.path.insert(0, directory)
'''

import wx
from odmtools.gui import frmODMTools


def create(parent):
    return frmODMTools.create(parent)


def runODM():
    app = wx.App(False)
    frame = create(None)
    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    app = wx.App(False)
    frame = create(None)
    frame.Show()
    app.MainLoop()
