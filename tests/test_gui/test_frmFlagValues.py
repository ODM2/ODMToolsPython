
__author__ = 'jmeline'

import wx
from odmtools.gui.frmFlagValues import frmFlagValues

class TestFrmFlagValues:
    def setup(self):
        self.app = wx.App()
        self.frame = frmFlagValues(None)

