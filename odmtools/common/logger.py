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
        self.formatString1 = '%(asctime)s (%(levelname)s) %(module)s:%(funcName)s(%(lineno)d) - %(message)s'
        self.formatString2 ='%(asctime)s - %(levelname)s - %(module)s - %(message)s'

    def setupLogger(self, loggerName, logFile, m='w', level=logging.INFO):
        l = logging.getLogger(loggerName)
        # formatter = logging.Formatter('%(asctime)s : %(message)s')
        formatter = logging.Formatter(self.formatString1)


        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(formatter)

        l.setLevel(level)
        #l.setLevel(20) #Set logger to 20 to hide debug statements
        l.addHandler(streamHandler)



        logPath = user_log_dir("ODMTools", "UCHIC")
        if not os.path.exists(logPath):
            os.makedirs(logPath, 0755)
        fileHandler = logging.FileHandler(os.path.join(logPath, logFile), mode=m)
        fileHandler.setFormatter(formatter)

        # l.setLevel(logging.ERROR)
        l.addHandler(fileHandler)


        # solves issues where logging would duplicate its logging message to the root logger
        # https://stackoverflow.com/questions/21127360/python-2-7-log-displayed-twice-when-logging-module-is-used-in-two-python-scri
        l.propagate = False

        return l

