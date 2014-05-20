#Boa:FramePanel:pnlDataTable

import logging

import wx
import wx.grid
from ObjectListView import ColumnDefn, FastObjectListView
from wx.lib.pubsub import pub as Publisher

from common.logger import LoggerTool

tool = LoggerTool()
logger = tool.setupLogger(__name__, __name__ + '.log', 'w', logging.DEBUG)

[wxID_PNLDATATABLE, wxID_PNLDATATABLEDATAGRID,
] = [wx.NewId() for _init_ctrls in range(2)]


class pnlDataTable(wx.Panel):
    def __init__(self, parent, id, size, style, name, pos=None):
        self._init_ctrls(parent)

    # selectedpoints = []
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PNLDATATABLE, name=u'pnlDataTable',
                          parent=prnt, size=wx.Size(677, 449),
                          style=wx.TAB_TRAVERSAL)
        self.parent = prnt
        self.record_service = self.parent.Parent.getRecordService()
        self.myOlv = FastObjectListView(self, -1, style=wx.LC_REPORT)  #Virtual

        # self.myOlv.SetObjectGetter(self.fetchFromDatabase)
        self.myOlv.SetEmptyListMsg("No Series Selected for Editing")
        self.myOlv.handleStandardKeys = True
        self.myOlv.rowFormatter = self._rowFormatter

        self.currentItem = None

        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_2.Add(self.myOlv, 1, wx.ALL | wx.EXPAND, 4)
        self.SetSizer(sizer_2)

        self.myOlv.Bind(wx.EVT_LIST_ITEM_FOCUSED, self.onItemSelected)
        self.myOlv.Bind(wx.EVT_CHAR, self.onKeyPress)

        Publisher.subscribe(self.onChangeSelection, ("changeTableSelection"))
        Publisher.subscribe(self.onRefresh, ("refreshTable"))

        self.Layout()


    def init(self, memDB, record_service):
        self.memDB = memDB
        self.record_service = record_service
        self.myOlv.SetColumns(
            ColumnDefn(x.strip(), align="left", valueGetter=i, minimumWidth=100, width=-1)
            for x, i in self.memDB.getEditColumns()
        )

        #####table Settings
        self.myOlv.useAlternateBackColors = True
        self.myOlv.oddRowsBackColor = "SlateGray"
        self.myOlv.AutoSizeColumns()

        # self.values = [list(x) for x in self.cursor.fetchall()]
        self.myOlv.SetObjects(self.memDB.getDataValuesforEdit())

    def onRefresh(self, e):
        self.myOlv.SetObjects(self.memDB.getDataValuesforEdit())

    def clear(self):
        self.memDB = None
        self.record_service = None
        self.myOlv.SetObjects(None)

    def onItemSelected(self, event):
        """Capture the currently selected Object to be used for editing

        :param event: wx.EVT_LIST_ITEM_FOCUSED type
        """

        self.currentItem = event.GetEventObject().GetSelectedObjects()
        self.myOlv.RefreshObjects(self.currentItem)
        #logger.debug("selectedObjects %s" % self.currentItem)

        self.record_service.select_points(datetime_list=[x[3] for x in self.currentItem])
        #update plot
        Publisher.sendMessage(("changeSelection"), sellist=[], datetime_list=[x[3] for x in self.currentItem])

    def onKeyPress(self, event):
        """Checks for when user inputs Ctrl+A"""
        keycode = event.GetKeyCode()
        logger.debug("keycode %s" % keycode)
        if keycode == 1:
            #logger.debug("OnKeyPress! Ctrl+A was pressed")
            self.myOlv.SelectAll()
            self.currentItem = self.myOlv.GetSelectedObjects()
            logger.debug("itemtype %s" % type(self.currentItem))

            if len(self.currentItem) > 0: pass
            #print "self.currentItem: ", self.currentItem
            #print "len: ", len(self.currentItem)

            #selectedids = self.getSelectedIDs(self.myOlv.GetSelectedObjects())
            self.record_service.select_points(datetime_list=[x[3] for x in self.currentItem])
            Publisher.sendMessage(("changeSelection"), sellist=[], datetime_list=[x[3] for x in self.currentItem])

    def onChangeSelection(self, sellist=[], datetime_list=[]):
        objlist = []
        #self.myOlv.SelectObject(None, deselectOthers=True)
        if len(sellist) > 0:
            for i in range(len(sellist)):
                if sellist[i]:
                    objlist.append(self.myOlv.GetObjectAt(i))
        else:
            #logger.debug(datetime_list)
            objlist = [x for x in self.myOlv.modelObjects if x[3] in datetime_list]

        if len(objlist) > 0:
            self.myOlv.SelectObject(objlist[0], deselectOthers=True, ensureVisible=True)
        #logger.debug(objs)
        self.myOlv.SelectObjects(objlist, deselectOthers=True)

    def stopEdit(self):
        self.clear()

    def getSelectedIDs(self, selobjects):
        idlist = [False] * self.memDB.getEditRowCount()
        for sel in selobjects:
            idlist[self.myOlv.GetIndexOf(sel)] = True
        return idlist

    def _rowFormatter(self, listItem, object):
        """Handles the formatting of rows for object list view
        :param: wx.ListCtrl listitem
        :param: ModelObject object

        :rtype: None
        """

        if self.currentItem and object in self.currentItem:

            #print self.currentItem
            #listItem.SetTextColour(wx.Colour(25, 25, 112))
            # font type: wx.DEFAULT, wx.DECORATIVE, wx.ROMAN, wx.SCRIPT, wx.SWISS, wx.MODERN
            # slant: wx.NORMAL, wx.SLANT or wx.ITALIC
            # weight: wx.NORMAL, wx.LIGHT or wx.BOLD
            #font1 = wx.Font(10, wx.SWISS, wx.ITALIC, wx.NORMAL)
            # use additional fonts this way ...
            #font1 = wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL, False, u'Comic Sans MS')
            listItem.SetFont(
                wx.Font(9, wx.DECORATIVE, wx.ITALIC, wx.BOLD, face=u'Lucida Console'))
        else:
            listItem.SetTextColour(wx.Colour())
            listItem.SetFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.NORMAL, False, u'Tahoma'))







