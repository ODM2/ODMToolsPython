#Boa:FramePanel:pnlSummary

import wx

[wxID_PNLSUMMARY] = [wx.NewId() for _init_ctrls in range(1)]

class pnlSummary(wx.Panel):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PNLSUMMARY, name=u'pnlSummary',
              parent=prnt, pos=wx.Point(536, 285), size=wx.Size(439, 357),
              style=wx.TAB_TRAVERSAL)
        self.SetClientSize(wx.Size(423, 319))

    def __init__(self, parent, id, pos, size, style, name):
        self._init_ctrls(parent)
