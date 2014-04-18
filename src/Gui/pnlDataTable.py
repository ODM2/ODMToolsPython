#Boa:FramePanel:pnlDataTable

import logging

import wx
import wx.grid
from ObjectListView import ColumnDefn, FastObjectListView, Filter
from wx.lib.pubsub import pub as Publisher

from common.logger import LoggerTool

tool = LoggerTool()
logger = tool.setupLogger(__name__, __name__ + '.log', 'w', logging.DEBUG)

[wxID_PNLDATATABLE, wxID_PNLDATATABLEDATAGRID,
] = [wx.NewId() for _init_ctrls in range(2)]


class pnlDataTable(wx.Panel):
    def __init__(self, parent, id,  size, style, name, pos=None):
        self._init_ctrls(parent)

    # selectedpoints = []
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PNLDATATABLE, name=u'pnlDataTable',
              parent=prnt,  size=wx.Size(677, 449),
              style=wx.TAB_TRAVERSAL)
        self.parent= prnt
        self.record_service= self.parent.Parent.getRecordService()
        self.myOlv = FastObjectListView(self, -1, style=wx.LC_REPORT) #Virtual

        # self.myOlv.SetObjectGetter(self.fetchFromDatabase)
        self.myOlv.SetEmptyListMsg("No Series Selected for Editing")
        self.myOlv.handleStandardKeys =True

        self.currentItem = 0

        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_2.Add(self.myOlv, 1, wx.ALL|wx.EXPAND, 4)
        self.SetSizer(sizer_2)

        self.myOlv.Bind(wx.EVT_LIST_ITEM_FOCUSED, self.onItemSelected )
        self.myOlv.Bind(wx.EVT_CHAR, self.onKeyPress)

        Publisher.subscribe(self.onChangeSelection, ("changeTableSelection"))
        Publisher.subscribe(self.onRefresh, ("refreshTable"))

        self.Layout()


    def init(self, memDB, record_service):
        self.memDB = memDB
        self.record_service = record_service
        self.myOlv.SetColumns(ColumnDefn(x.strip(), align="left", valueGetter=i, width=-1) for x, i in self.memDB.getEditColumns())

        #####table Settings
        self.myOlv.useAlternateBackColors = True
        self.myOlv.oddRowsBackColor = "SlateGray"
        self.myOlv.AutoSizeColumns()


        # self.values = [list(x) for x in self.cursor.fetchall()]
        self.myOlv.SetObjects(self.memDB.getDataValuesforEdit())

    def onRefresh(self, e):
        self.myOlv.SetObjects(self.memDB.getDataValuesforEdit())
        self.myOlv.SelectObject(self.myOlv.GetObjectAt(0), deselectOthers=True, ensureVisible =True)


    def clear(self):
        self.memDB= None
        self.record_service = None
        self.myOlv.SetObjects(None)


    def onItemSelected(self, event):
        # print "in onItemSelected"
        # if  not (event.m_itemIndex in self.selectedpoints):
        #     self.selectedpoints.Add(event.m_itemIndex)

        self.currentItem = event.GetEventObject().GetSelectedObjects()
        #logger.debug("OnItemSelected: %s\n" % (self.currentItem))
        #logger.debug("size %d" % len(self.currentItem))
        #for i in self.currentItem:
            #logger.debug("index: %s" % (i[3]))

        #logger.debug("dates %s" % [x[3] for x in self.currentItem])
        self.record_service.select_points(datetime_list=[x[3] for x in self.currentItem])
        #update plot
        #selectedids = self.getSelectedIDs(self.myOlv.GetSelectedObjects())
        Publisher.sendMessage(("changeSelection"), sellist=[], datetime_list=[x[3] for x in self.currentItem])

    def onKeyPress(self, event):
        # check for Ctrl+A
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
            Publisher.sendMessage(("changeSelection"), sellist= [], datetime_list=[x[3] for x in self.currentItem] )


    def onChangeSelection(self, sellist=[], datetime_list= []):
        objlist=[]
        isfirstselected = False
        if len(sellist)>0:
            for i in range(len(sellist)):
                if sellist[i]:
                    if not isfirstselected:
                        self.myOlv.SelectObject(self.myOlv.GetObjectAt(i), deselectOthers=True, ensureVisible =True)
                        isfirstselected=True
                    objlist.append(self.myOlv.GetObjectAt(i))
            self.myOlv.SelectObjects(objlist, deselectOthers=False)  #, ensureVisible =True
            self.record_service.select_points_tf(sellist)
        else:
            #TODO Select by DateTime        #filter(by date),        #getfilteredobjects,        #removefilter,        #Select Objects
            for dateval in datetime_list:
                #logger.debug("filter: %s" % dateval.strftime("%Y-%m-%d %H:%M:%S"))
                self.myOlv.SetFilter(Filter.TextSearch(self.myOlv, text=dateval.strftime("%Y-%m-%d %H:%M:%S")))
                #logger.debug("filteredobject: %s" % self.myOlv.GetFilteredObjects())
                if not isfirstselected:
                    self.myOlv.SelectObject(self.myOlv.GetFilteredObjects()[0], deselectOthers=True, ensureVisible =True)
                    isfirstselected =True
                objlist.append(self.myOlv.GetFilteredObjects()[0])
            self.myOlv.SelectObjects(objlist, deselectOthers=False)
            self.record_service.select_points(datetime_list=datetime_list)
                #self.myOlv.SelectObject(self.myOlv.GetFilteredObjects(), deselectOthers=False)



        #self.myOlv.SelectObjects(objlist, deselectOthers=True)  #, ensureVisible =True

        self.myOlv.SetFocus()

    def stopEdit(self):
        self.clear()

    def getSelectedIDs(self, selobjects):
        idlist=[False] * self.memDB.getEditRowCount()
        for sel in selobjects:
            idlist[self.myOlv.GetIndexOf(sel)]=True

        return idlist





