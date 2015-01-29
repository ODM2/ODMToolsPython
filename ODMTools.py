#!/usr/local/bin/python

"""

ODMTools is a python application for managing observational data using the Observations Data Model.
ODMTools allows you to query, visualize, and edit data stored in an Observations Data Model (ODM) database.
ODMTools was originally developed as part of the CUAHSI Hydrologic Information System.

Repository is located on www.github.com/UCHIC/ODMToolsPython

"""

import wx
import logging
from odmtools.gui.frmODMTools import frmODMToolsMain
from common.taskServer import TaskServerMP
from odmtools.common.logger import LoggerTool
from multiprocessing import cpu_count, freeze_support

tool = LoggerTool()
logger = tool.setupLogger(__name__, __name__ + '.log', 'w', logging.DEBUG)
wx.Log.SetLogLevel(0)

class MyApp(wx.App):
    """
    A Simple App class, modified to hold the processes and task queues
    """

    def __init__(self, redirect=True, filename=None, useBestVisual=False, clearSigInt=True, taskserver=None):
        """
        Initialise the App.
        """
        self.taskserver = taskserver
        wx.App.__init__(self, redirect, filename, useBestVisual, clearSigInt)

    def OnInit(self):
        """
        Initialize an App with a Frame
        """
        title = u'ODMTools'

        kwargs = {}
        kwargs['parent'] = None
        kwargs['name'] = title
        kwargs['style'] = wx.DEFAULT_FRAME_STYLE
        kwargs['title'] = title

        # multiprocessing task server
        kwargs['taskServer'] = self.taskserver
        self.frame = frmODMToolsMain(**kwargs)
        self.frame.Show(True)
        return True

def runODM():
    app = wx.App(False)
    #frame = create(None)
    #frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    logger.debug("Welcome to ODMTools Python. Please wait as system loads")
    # https://docs.python.org/2/library/multiprocessing.html#miscellaneous

    # Add support for when a program which uses multiprocessing has been frozen to produce a Windows executable.
    # (Has been tested with py2exe, PyInstaller and cx_Freeze.)
    # One needs to call this function straight after the if __name__ == '__main__' line of the main module.

    # If the freeze_support() line is omitted then trying to run the frozen executable will raise RuntimeError.
    # If the module is being run normally by the Python interpreter then freeze_support() has no effect.
    freeze_support()

    # Determine the number of CPU's available
    numproc = cpu_count()

    # Initialize TaskServer.
    # This class starts the processes before starting wxpython and is needed
    tsmp = TaskServerMP(numproc=numproc)

    # Build app with taskserver included
    app = MyApp(False, taskserver=tsmp)
    app.MainLoop()

