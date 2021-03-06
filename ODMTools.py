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
from odmtools.common.taskServer import TaskServerMP
from odmtools.common.logger import LoggerTool
from multiprocessing import cpu_count, freeze_support
from odmtools.odmdata import MemoryDatabase

import pyodbc
import pymysql
#import psycopg2


tool = LoggerTool()
logger = tool.setupLogger('main',  'odmtools.log', 'a', logging.INFO)
wx.Log.SetLogLevel(0)


import sys
import os
# Module multiprocessing is organized differently in Python 3.4+
try:
    # Python 3.4+
    if sys.platform.startswith('win'):
        import multiprocessing.popen_spawn_win32 as forking
    else:
        import multiprocessing.popen_fork as forking
except ImportError:
    import multiprocessing.forking as forking

if sys.platform.startswith('win'):
    # First define a modified version of Popen.
    class _Popen(forking.Popen):
        def __init__(self, *args, **kw):
            if hasattr(sys, 'frozen'):
                # We have to set original _MEIPASS2 value from sys._MEIPASS
                # to get --onefile mode working.
                os.putenv('_MEIPASS2', sys._MEIPASS)
            try:
                super(_Popen, self).__init__(*args, **kw)
            finally:
                if hasattr(sys, 'frozen'):
                    # On some platforms (e.g. AIX) 'os.unsetenv()' is not
                    # available. In those cases we cannot delete the variable
                    # but only set it to the empty string. The bootloader
                    # can handle this case.
                    if hasattr(os, 'unsetenv'):
                        os.unsetenv('_MEIPASS2')
                    else:
                        os.putenv('_MEIPASS2', '')

    # Second override 'Popen' class with our modified version.
    forking.Popen = _Popen




class MyApp(wx.App):
    """
    A Simple App class, modified to hold the processes and task queues
    """

    def __init__(self, redirect=True, filename=None, useBestVisual=False, clearSigInt=True, taskserver=None, memdb = None):
        """
        Initialise the App.
        """
        self.taskserver = taskserver
        self.memdb = memdb
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
        kwargs['memdb']= self.memdb
        self.frame = frmODMToolsMain(**kwargs)
        self.frame.Show(True)
        app= self.frame
        return True

def runODM():
    app = wx.App(False)
    #frame = create(None)
    #frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    logger.info("Welcome to ODMTools Python. Please wait as system loads")
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
    memdb = MemoryDatabase()

    # Build app with taskserver included
    app = MyApp(False, taskserver=tsmp, memdb = memdb)
    app.MainLoop()

