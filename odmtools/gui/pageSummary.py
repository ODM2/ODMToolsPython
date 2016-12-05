
#Boa:FramePanel:pnlSummary

import wx

[wxID_PNLSUMMARY, wxID_PNLSUMMARYTREESUMMARY,
] = [wx.NewId() for _init_ctrls in range(2)]

class pnlSummary(wx.Panel):
    def _init_coll_boxSizer1_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.treeSummary, 100, border=0, flag=wx.EXPAND)

    def _init_sizers(self):
        # generated method, don't edit
        self.boxSizer1 = wx.BoxSizer(orient=wx.VERTICAL)

        self._init_coll_boxSizer1_Items(self.boxSizer1)

        self.SetSizer(self.boxSizer1)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PNLSUMMARY, name=u'pnlSummary',
              parent=prnt, pos=wx.Point(565, 279), size=wx.Size(439, 357),
              style=wx.TAB_TRAVERSAL)
        self.SetClientSize(wx.Size(423, 319))

        self.treeSummary = MyTree(id=wxID_PNLSUMMARYTREESUMMARY,
               parent=self, pos=wx.Point(0, 0),
              size=wx.Size(423, 319), style=wx.TR_HAS_BUTTONS|wx.TR_HIDE_ROOT)

        self._init_sizers()

    def __init__(self, parent, id, size, style, name, ss, pos= (0,0)):
        self.series_service = ss
        self._init_ctrls(parent)


class MyTree(wx.TreeCtrl): # Who's tree is this? Who said it was theirs?
    def __init__(self, parent, id, pos, size, style):

         wx.TreeCtrl.__init__(self, parent, id, pos, size, style)
         self.root = self.AddRoot('Series')
         self.site = self.AppendItem(self.root, 'Site')
         self.v = self.AppendItem(self.root, 'Variable')
         self.m = self.AppendItem(self.root, 'Method')
         self.action = self.AppendItem(self.root, 'Action')
         self.processing_level = self.AppendItem(self.root, 'Processing Level')

         self.sc=self.AppendItem(self.site, 'Code: ')
         self.sn=self.AppendItem(self.site, 'Name: ')

         self.vc=self.AppendItem(self.v, 'Code: ')
         self.vn=self.AppendItem(self.v, 'Name: ')
         self.vu=self.AppendItem(self.v, 'Units: ')
         self.vsm=self.AppendItem(self.v, 'Sample Medium: ')
         self.vvt=self.AppendItem(self.v, 'Value Type: ')
         self.vts=self.AppendItem(self.v, 'Time Support: ')
         self.vtu=self.AppendItem(self.v, 'Time Units: ')
         self.vdt=self.AppendItem(self.v, 'Data Type: ')
         self.vgc=self.AppendItem(self.v, 'General Category: ')

         self.md=self.AppendItem(self.m, 'Description: ')

         # self.soc=self.AppendItem(self.action, 'Person: ')
         self.soo=self.AppendItem(self.action, 'Organization: ')
         self.sod=self.AppendItem(self.action, 'Description: ')

         self.qc=self.AppendItem(self.processing_level, 'Code: ')
         self.qd=self.AppendItem(self.processing_level, 'Definition: ')
         self.qe=self.AppendItem(self.processing_level, 'Explanation: ')

