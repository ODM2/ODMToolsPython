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

        self.currentItem = 0

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
            ColumnDefn(x.strip(), align="left", valueGetter=i, width=-1) for x, i in self.memDB.getEditColumns())

        #####table Settings
        self.myOlv.useAlternateBackColors = True
        self.myOlv.oddRowsBackColor = "SlateGray"
        self.myOlv.AutoSizeColumns()


        # self.values = [list(x) for x in self.cursor.fetchall()]
        self.myOlv.SetObjects(self.memDB.getDataValuesforEdit())

    def onRefresh(self, e):
        self.myOlv.SetObjects(self.memDB.getDataValuesforEdit())
        self.myOlv.SelectObject(self.myOlv.GetObjectAt(0), deselectOthers=True, ensureVisible=True)


    def clear(self):
        self.memDB = None
        self.record_service = None
        self.myOlv.SetObjects(None)


    def onItemSelected(self, event):


        self.currentItem = event.GetEventObject().GetSelectedObjects()

        self.record_service.select_points(datetime_list=[x[3] for x in self.currentItem])

        #update plot
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
            Publisher.sendMessage(("changeSelection"), sellist=[], datetime_list=[x[3] for x in self.currentItem])

    def onChangeSelection(self, sellist=[], datetime_list=[]):
        objlist = []
        isfirstselected = False
        if len(sellist) > 0:
            for i in range(len(sellist)):
                if sellist[i]:
                    if not isfirstselected:
                        self.myOlv.SelectObject(self.myOlv.GetObjectAt(i), deselectOthers=True, ensureVisible=True)
                        isfirstselected = True
                    objlist.append(self.myOlv.GetObjectAt(i))
            self.myOlv.SelectObjects(objlist, deselectOthers=False)  #, ensureVisible =True

        else:
            #TODO Select by DateTime        #filter(by date),        #getfilteredobjects,        #removefilter,        #Select Objects

            self.DoSelectDateTime(self.myOlv, datetime_list)

            #for dateval in datetime_list:
            #    logger.debug("filter: %s" % dateval.strftime("%Y-%m-%d %H:%M:%S"))
            #    self.myOlv.SetFilter(DateSearch(self.myOlv, self.myOlv.columns[3:5], dateval))
            #    logger.debug("len: %d" % len(self.myOlv.GetFilteredObjects()))
                #logger.debug("filteredobject: %s" % self.myOlv.GetFilteredObjects())
                #if not isfirstselected:
                #    self.myOlv.SelectObject(self.myOlv.GetFilteredObjects()[0], deselectOthers=True, ensureVisible=True)
                #    isfirstselected = True
            #    objlist.append(self.myOlv.GetFilteredObjects()[0])
            #self.myOlv.SelectObjects(objlist, deselectOthers=False)





            #self.myOlv.SelectObject(self.myOlv.GetFilteredObjects(), deselectOthers=False)



        #self.myOlv.SelectObjects(objlist, deselectOthers=True)  #, ensureVisible =True

        self.myOlv.SetFocus()

    def DoSelectDateTime(self, olv, datetimes):

        logger.debug(datetimes)
        objs = [x for x in olv.modelObjects if x[3] in datetimes]
        olv.SelectObject(objs[0], deselectOthers=True, ensureVisible=True)
        logger.debug(objs)
        olv.SelectObjects(objs, deselectOthers=True)

    def stopEdit(self):
        self.clear()

    def getSelectedIDs(self, selobjects):
        idlist = [False] * self.memDB.getEditRowCount()
        for sel in selobjects:
            idlist[self.myOlv.GetIndexOf(sel)] = True

        return idlist


class DateSearch(object):
    """
    Return only model objects that match a given string. If columns is not empty,
    only those columns will be considered when searching for the string. Otherwise,
    all columns will be searched.

    Example::
        self.olv.SetFilter(Filter.TextSearch(self.olv, text="findthis"))
        self.olv.RepopulateList()
    """

    def __init__(self, objectListView, columns=(), date=None):
        """
        Create a filter that includes on modelObject that have 'self.text' somewhere in the given columns.
        """
        self.objectListView = objectListView
        self.columns = columns
        self.date = date

    def __call__(self, modelObjects):
        """
        Return the model objects that contain our text in one of the columns to consider
        """
        print "date: ", self.date

        if not self.date:
            #return modelObjects
            return None


        # In non-report views, we can only search the primary column
        if self.objectListView.InReportView():
            cols = self.columns or self.objectListView.columns
        else:
            cols = [self.objectListView.columns[0]]
            print "Cols: ", cols

        #textToFind = self.text.lower()

        def _containsDate(modelObject):
            for col in cols:
                print col.GetValue(modelObject)
                if self.date == col.GetValue(modelObject):
                    return True
            return False

        return [x for x in modelObjects if _containsDate(x)]

    def SetDate(self, date):
        """
        Set the text that this filter will match. Set this to None or "" to disable the filter.
        """
        self.date = date





