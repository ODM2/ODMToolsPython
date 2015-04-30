'''
By Jacob Meline
    Creates a factory logging method to be used within any class
'''

__author__ = 'Jacob'

import logging
import os

from odmtools.lib.Appdirs.appdirs import user_log_dir



class LoggerTool():
    def __init__(self):
        self.formatString = '%(asctime)s - %(levelname)s - %(name)s.%(funcName)s() (%(lineno)d): %(message)s'
        self.formatString1 = '%(asctime)s (%(levelname)s) %(module)s:%(funcName)s.%(name)s(%(lineno)d) - %(message)s'

    def setupLogger(self, loggerName, logFile, m='w', level=logging.INFO):
        l = logging.getLogger(loggerName)
        # formatter = logging.Formatter('%(asctime)s : %(message)s')
        formatter = logging.Formatter(self.formatString)

        #logPath = os.path.abspath(os.path.dirname("../../"))
        #logPath = util.resource_path("ODMTools")
        logPath = user_log_dir("ODMTools", "UCHIC")

        #logPath = os.path.join(user_log_dir("ODMTools", "UCHIC"), "log")
        #print  logPath

        if not os.path.exists(logPath):
            os.makedirs(logPath, 0755)
        fileHandler = logging.FileHandler(os.path.join(logPath, logFile), mode=m)
        fileHandler.setFormatter(formatter)
        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(formatter)

        l.setLevel(level)
        #l.setLevel(20) #Set logger to 20 to hide debug statements
        l.addHandler(fileHandler)
        l.addHandler(streamHandler)

        # solves issues where logging would duplicate its logging message to the root logger
        # https://stackoverflow.com/questions/21127360/python-2-7-log-displayed-twice-when-logging-module-is-used-in-two-python-scri
        l.propagate = False

        return l

