import wx
import wx.grid
import logging
import itertools as iter
import pandas as pd
from odmtools.lib.ObjectListView import ColumnDefn, FastObjectListView, VirtualObjectListView
from wx.lib.pubsub import pub as Publisher

import timeit

from odmtools.common.logger import LoggerTool


tool = LoggerTool()
logger = tool.setupLogger(__name__, __name__ + '.log', 'w', logging.DEBUG)

[wxID_PNLDATATABLE, wxID_PNLDATATABLEDATAGRID,
] = [wx.NewId() for _init_ctrls in range(2)]


class pnlDataTable(wx.Panel):

    toggle = iter.cycle([0, 1]).next

    def __init__(self, parent):
        self.parent = parent
        self._init_ctrls()

    def _init_ctrls(self):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PNLDATATABLE, name=u'pnlDataTable',
                          parent=self.parent, size=wx.Size(677, 449),
                          style=wx.TAB_TRAVERSAL)
        self.record_service = self.parent.Parent.getRecordService()
        # self.myOlv = FastObjectListView(self, -1, style=wx.LC_REPORT)
        ## Trying out virtualObjectListView
        self.myOlv = VirtualObjectListView(self, -1, style=wx.LC_REPORT)

        self.myOlv.SetEmptyListMsg("No Series Selected for Editing")
        self.currentItem = None

        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_2.Add(self.myOlv, 1, wx.ALL | wx.EXPAND, 4)
        self.SetSizer(sizer_2)

        self.myOlv.Bind(wx.EVT_LIST_ITEM_FOCUSED, self.onItemSelected)

        #self.myOlv.Bind(wx.EVT_CHAR, self.onKeyPress)
        #self.myOlv.Bind(wx.EVT_LIST_KEY_DOWN, self.onKeyPress)
        Publisher.subscribe(self.onChangeSelection, ("changeTableSelection"))
        Publisher.subscribe(self.onRefresh, ("refreshTable"))

        self.Layout()

    def toggleBindings(self):
        """ Activates/Deactivates Datatable specific bindings

        :param activate:
        :return:
        """

        if self.toggle():
            #logger.info("binding activated...")
            try:
                self.myOlv.Bind(wx.EVT_LIST_ITEM_FOCUSED, self.onItemSelected, id=self.myOlv.GetId())
                self.myOlv.Bind(wx.EVT_CHAR, self.onKeyPress, id=self.myOlv.GetId())
                self.myOlv.Bind(wx.EVT_LIST_KEY_DOWN, self.onKeyPress, id=self.myOlv.GetId())
            except:
                pass
        else:
            #logger.info("binding deactivated...")
            try:
                self.myOlv.Unbind(wx.EVT_LIST_ITEM_FOCUSED, self.onItemSelected, id=self.myOlv.GetId())
                self.myOlv.Unbind(wx.EVT_CHAR, self.onKeyPress, id=self.myOlv.GetId())
                self.myOlv.Unbind(wx.EVT_LIST_KEY_DOWN, self.onKeyPress, id=self.myOlv.GetId())
            except:
                pass

    def init(self, memDB, record_service):
        self.memDB = memDB
        self.record_service = record_service

        columns = [ColumnDefn(x.strip(), align="left", valueGetter=i, minimumWidth=100, width=-1,
                              stringConverter= '%Y-%m-%d %H:%M:%S' if "date" in x.lower() else '%s')
                   for x, i in self.memDB.getEditColumns()]


        self.myOlv.useAlternateBackColors = True
        self.myOlv.oddRowsBackColor = wx.Colour(191, 217, 217)

        values = self.memDB.getDataValues()
        value_length = len(values)

        self.myOlv.SetObjectGetter(self.objectGetter)
        self.myOlv.SetItemCount(value_length)

        self.myOlvDataFrame = pd.DataFrame(values, columns=[x.title for x in columns])
        self.myOlv.SetColumns(columns)
        self.dataObjects = self.myOlvDataFrame.values.tolist()

    def objectGetter(self, index):
        """
        A Virtual list has to have a callable installed that says which model object is shown
        at a given index
        """
        return self.dataObjects[index % len(self.dataObjects)]

    def onRefresh(self, e):
        #self.myOlv.SetObjects(self.memDB.getDataValuesforEdit())
        pass

    def clear(self):
        self.memDB = None
        self.record_service = None
        #self.myOlv.SetObjects(None)


    def onItemSelected(self, event):
        """Capture the currently selected Object to be used for editing

        :param event: wx.EVT_LIST_ITEM_FOCUSED type
        """
        #self.currentItem = event.GetEventObject().GetSelectedObjects()
        try:
            self.currentItem = pd.Series(self.myOlv.GetSelectedObjects())
            logger.debug("selectedObjects %s" % len(self.currentItem))

            self.record_service.select_points(datetime_list=[x[3] for x in self.currentItem])
            #update plot
            Publisher.sendMessage(("changePlotSelection"),  datetime_list=[x[3] for x in self.currentItem])
        except:
            pass


    def onChangeSelection(self,  datetime_list=[]):
        if isinstance(datetime_list, pd.DataFrame):
            start_time = timeit.default_timer()
            olv = self.myOlvDataFrame.set_index("LocalDateTime")
            filtered_dataframe = self.myOlvDataFrame[olv.index.isin(datetime_list.index)]
            values = filtered_dataframe.values.tolist()
            elapsed_time = timeit.default_timer() - start_time
            logger.debug("Change table took: %s seconds" % elapsed_time)

            ## Convert np timestamp to useable datetime.datetime format
            ## Improvements can be made. But this is faster than before.
            ##  Need to figure out how to convert pandas columns to datetime without loops.

            start_time = timeit.default_timer()
            for i in values:
                i[3] = i[3].to_pydatetime()
                i[5] = i[5].to_pydatetime()
            elapsed_time = timeit.default_timer() - start_time
            logger.debug("Change table took: %s seconds to correct the datatypes" % elapsed_time)


            if len(values) > 0:
                self.myOlv.SelectObject(values[0], deselectOthers=True, ensureVisible=True)
            start_time = timeit.default_timer()
            self.myOlv.SelectObjects(values, deselectOthers=True)
            elapsed_time = timeit.default_timer() - start_time
            logger.debug("Change table took: %s seconds to select in objectlistview" % elapsed_time)



    def onKeyPress(self, evt):
        """Ignores Keypresses"""
        pass

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
        objects = self.myOlv.GetSelectedObjects()

        #if self.currentItem and object in self.currentItem:
        if objects and object in objects:

            # font type: wx.DEFAULT, wx.DECORATIVE, wx.ROMAN, wx.SCRIPT, wx.SWISS, wx.MODERN
            # slant: wx.NORMAL, wx.SLANT or wx.ITALIC
            # weight: wx.NORMAL, wx.LIGHT or wx.BOLD
            #font1 = wx.Font(10, wx.SWISS, wx.ITALIC, wx.NORMAL)
            # use additional fonts this way ...
            #font1 = wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL, False, u'Comic Sans MS')
            listItem.SetFont(
                wx.Font(9, wx.DECORATIVE, wx.ITALIC, wx.BOLD))
        else:
            listItem.SetFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.NORMAL, False, u'Tahoma'))







