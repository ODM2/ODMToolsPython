
import wx
import logging

from common.logger import LoggerTool

tool = LoggerTool()
logger = tool.setupLogger(__name__, __name__ + '.log', 'w', logging.DEBUG)

class pnlSeriesSelectorTable(wx.Panel):
    pass


