'''
By Jacob Meline
    Creates a factory logging method to be used within any class
'''

__author__ = 'Jacob'

import logging


class LoggerTool():
    def __init__(self):
        self.formatString = '%(asctime)s - %(levelname)s - %(name)s.%(funcName)s() (%(lineno)d): %(message)s'
        self.formatString1 = '%(asctime)s (%(levelname)s) %(module)s:%(funcName)s.%(name)s(%(lineno)d) - %(message)s'

    def setupLogger(self, loggerName, logFile, m='w', level=logging.INFO):
        l = logging.getLogger(loggerName)
        #formatter = logging.Formatter('%(asctime)s : %(message)s')
        formatter = logging.Formatter(self.formatString)

        fileHandler = logging.FileHandler(logFile, mode=m)
        fileHandler.setFormatter(formatter)
        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(formatter)

        l.setLevel(level)
        l.addHandler(fileHandler)
        l.addHandler(streamHandler)

        return l

