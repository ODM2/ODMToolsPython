import wx
import wx.grid
import logging
import itertools as iter

import pandas as pd
from odmtools.lib.ObjectListView import ColumnDefn, VirtualObjectListView, ObjectListView
from wx.lib.pubsub import pub as Publisher
import numpy as np
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
        # self.record_service = self.parent.Parent.getRecordService()
        self.myOlv = VirtualObjectListView(self, style=wx.LC_REPORT)

        self.myOlv.SetEmptyListMsg("No Series Selected for Editing")
        self.currentItem = None

        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_2.Add(self.myOlv, 1, wx.ALL | wx.EXPAND, 4)
        self.SetSizer(sizer_2)

        self.myOlv.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onItemSelected)
        self.myOlv.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.onItemSelected)

        self.EnableSorting()

        Publisher.subscribe(self.onChangeSelection, "changeTableSelection")
        Publisher.subscribe(self.onRefresh, "refreshTable")
        Publisher.subscribe(self.onDeselectAll, "deselectAllDataTable")

        self.ascending = False
        self.enableSelectDataTable = False

        self.Layout()



    # def toggleBindings(self):
    #     """ Activates/Deactivates Datatable specific bindings
    #
    #     :param activate:
    #     :return:
    #     """
    #
    #     if self.toggle():
    #         #logger.info("binding activated...")
    #         try:
    #             self.myOlv.Bind(wx.EVT_LIST_ITEM_FOCUSED, self.onItemSelected, id=self.myOlv.GetId())
    #             self.myOlv.Bind(wx.EVT_CHAR, self.onKeyPress, id=self.myOlv.GetId())
    #             self.myOlv.Bind(wx.EVT_LIST_KEY_DOWN, self.onKeyPress, id=self.myOlv.GetId())
    #         except:
    #             pass
    #     else:
    #         #logger.info("binding deactivated...")
    #         try:
    #             self.myOlv.Unbind(wx.EVT_LIST_ITEM_FOCUSED, self.onItemSelected, id=self.myOlv.GetId())
    #             self.myOlv.Unbind(wx.EVT_CHAR, self.onKeyPress, id=self.myOlv.GetId())
    #             self.myOlv.Unbind(wx.EVT_LIST_KEY_DOWN, self.onKeyPress, id=self.myOlv.GetId())
    #         except:
    #             pass

    def init(self, memDB):
        self.memDB = memDB

        columns = [ColumnDefn(x.strip(), align="left", valueGetter=i, minimumWidth=125, width=125,
                              stringConverter='%Y-%m-%d %H:%M:%S' if "date" in x.lower() else '%s')
                   for x, i in self.memDB.getEditColumns()]

        self.myOlv.useAlternateBackColors = True
        self.myOlv.oddRowsBackColor = wx.Colour(191, 217, 217)

        '''values = self.memDB.getDataValues()
        value_length = len(values)

        self.myOlvDataFrame = pd.DataFrame(values, columns=[x.title for x in columns])
        '''
        self.myOlv.SetColumns(columns)

        self.myOlvDataFrame = self.memDB.getDataValuesDF()
        sort_by_index = list(self.myOlvDataFrame.columns).index("LocalDateTime")
        self.myOlvDataFrame.sort(self.myOlvDataFrame.columns[sort_by_index], inplace=True)
        self.dataObjects = self.myOlvDataFrame.values.tolist()

        self.myOlv.SetObjectGetter(self.objectGetter)
        self.myOlv.SetItemCount(len(self.myOlvDataFrame))

    def EnableSorting(self):
        self.myOlv.Bind(wx.EVT_LIST_COL_CLICK, self.onColSelected)
        self.sortedColumnIndex = -1

        if not self.myOlv.smallImageList:
            self.myOlv.SetImageLists()
        if (not self.myOlv.smallImageList.HasName(ObjectListView.NAME_DOWN_IMAGE) and
                    self.myOlv.smallImageList.GetSize(0) == (16, 16)):
            self.myOlv.RegisterSortIndicators()

    def objectGetter(self, index):
        """
        A Virtual list has to have a callable installed that says which model object is shown
        at a given index
        """
        return self.dataObjects[index % len(self.dataObjects)]

    def onColSelected(self, evt):
        """
        Allows users to sort by clicking on columns
        """
        logger.debug("Column: %s" % evt.m_col)
        self.sortColumn(evt.m_col)

    def sortColumn(self, selected_column):
        oldSortColumnIndex = self.sortedColumnIndex
        self.sortedColumnIndex = selected_column
        ascending = self.myOlv.sortAscending
        if ascending:
            self.myOlvDataFrame.sort(self.myOlvDataFrame.columns[selected_column], inplace=True)
            self.myOlv.sortAscending = False
        elif not ascending:
            self.myOlvDataFrame.sort(self.myOlvDataFrame.columns[selected_column], ascending=False, inplace=True)
            self.myOlv.sortAscending = True

        self.myOlv._UpdateColumnSortIndicators(selected_column, oldSortColumnIndex)

        self.dataObjects = self.myOlvDataFrame.values.tolist()
        if self.myOlv.GetItemCount:
            itemFrom = self.myOlv.GetTopItem()
            itemTo   = self.myOlv.GetTopItem()+1 + self.myOlv.GetCountPerPage()
            itemTo   = min(itemTo, self.myOlv.GetItemCount()-1)
            self.myOlv.RefreshItems(itemFrom, itemTo)

    def onRefresh(self, e):
        self.myOlvDataFrame = self.memDB.getDataValuesDF()
        self.dataObjects = self.myOlvDataFrame.values.tolist()
        # self.myOlv.RefreshItems()

    def clear(self):
        self.memDB = None
        self.myOlv.DeleteAllItems()
        self.myOlvDataFrame = None
        self.dataObjects = None

    def onItemSelected(self, event):
        """

        Disable selecting of an item in the DataTable, only sorting is available
        """
        if not self.enableSelectDataTable:
            self.myOlv.SetItemState(event.m_itemIndex, 0, wx.LIST_STATE_SELECTED)

    def onDeselectAll(self):

        selected_item = self.myOlv.GetFirstSelected()
        while selected_item != -1:
            self.myOlv.SetItemState(selected_item, 0, wx.LIST_STATE_SELECTED)
            selected_item = self.myOlv.GetNextSelected(selected_item)


    def onChangeSelection(self,  datetime_list=[]):
        """
        Select values within
        """
        self.onDeselectAll()

        if isinstance(datetime_list, pd.DataFrame):
            try:
                self.enableSelectDataTable = True
                olv = self.myOlvDataFrame.set_index("LocalDateTime")
                filtered_dataframe = self.myOlvDataFrame[olv.index.isin(datetime_list.index)]
                results = np.where(self.myOlvDataFrame.index.isin(filtered_dataframe.index))

                for i in results[0]:
                    self.myOlv.SetItemState(i, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)
                self.myOlv.Focus(results[0][0])
                self.enableSelectDataTable = False
            except:
                pass

    def onKeyPress(self, evt):
        """Ignores Keypresses"""
        pass

    def stopEdit(self):
        self.clear()








