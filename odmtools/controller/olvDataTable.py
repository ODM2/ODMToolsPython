import wx
import logging
# from odmtools.common.logger import LoggerTool
from odmtools.lib.ObjectListView import VirtualObjectListView, ObjectListView, ColumnDefn
import pandas as pd

# tool = LoggerTool()
# logger = tool.setupLogger(__name__, __name__ + '.log', 'w', logging.DEBUG)
logger =logging.getLogger('main')


__author__ = 'jmeline'


class OLVDataTable(VirtualObjectListView):
    def __init__(self, parent, **kwargs):
        VirtualObjectListView.__init__(self, parent, **kwargs)
        self.SetEmptyListMsg("No Series Selected for Editing")
        self.EnableSorting()
        self.sortedColumnIndex = -1
        self.currentItem = None
        self.dataframe = None

    def init(self, memDB):
        self.memDB = memDB
        columns = [ColumnDefn(x.strip(), align="left", valueGetter=i, minimumWidth=125, width=125,
                              stringConverter='%Y-%m-%d %H:%M:%S' if "date" in x.lower() else '%s')
                   for x, i in self.memDB.getEditColumns()]
        self.useAlternateBackColors = True
        self.oddRowsBackColor = wx.Colour(191, 217, 217)
        self.SetColumns(columns)
        self.dataframe = self.memDB.getDataValuesDF()
        sort_by_index = list(self.dataframe.columns).index("LocalDateTime")
        # self.dataframe.sort(self.dataframe.columns[sort_by_index], inplace=True) # sort() is depecrated
        self.dataframe.sort_values(self.dataframe.columns[sort_by_index], inplace=True)
        self.dataObjects = self.dataframe.values.tolist()

        self.SetObjectGetter(self.ObjectGetter)
        self.SetItemCount(len(self.dataframe))

    def EnableSorting(self):
        self.Bind(wx.EVT_LIST_COL_CLICK, self.onColSelected)
        if not self.smallImageList:
            self.SetImageLists()
        if (not self.smallImageList.HasName(ObjectListView.NAME_DOWN_IMAGE) and
                    self.smallImageList.GetSize(0) == (16, 16)):
            self.RegisterSortIndicators()

    def ObjectGetter(self, index):
        """
        A Virtual list has to have a callable installed that says which model object is shown
        at a given index
        """
        return self.dataObjects[index % len(self.dataObjects)]

    def onColSelected(self, evt):
        """
        Allows users to sort by clicking on columns
        """
        if isinstance(self.dataframe, pd.DataFrame):
           if self.dataframe.empty:
               return
        else:
            if not self.dataframe:
                return

        logger.debug("Column: %s" % evt.m_col)
        self.sortColumn(evt.m_col)

    def sortColumn(self, selected_column):
        oldSortColumnIndex = self.sortedColumnIndex
        self.sortedColumnIndex = selected_column
        ascending = self.sortAscending
        if ascending:
            self.dataframe.sort(self.dataframe.columns[selected_column], inplace=True)
            self.sortAscending = False
        elif not ascending:
            self.dataframe.sort(self.dataframe.columns[selected_column], ascending=False, inplace=True)
            self.sortAscending = True

        self._UpdateColumnSortIndicators(selected_column, oldSortColumnIndex)

        self.dataObjects = self.dataframe.values.tolist()
        if self.GetItemCount:
            itemFrom = self.GetTopItem()
            itemTo = self.GetTopItem() + 1 + self.GetCountPerPage()
            itemTo = min(itemTo, self.GetItemCount() - 1)
            self.RefreshItems(itemFrom, itemTo)

    def onItemSelected(self, event):
        """

        Disable selecting of an item in the DataTable, only sorting is available
        """
        if not self.enableSelectDataTable:
            self.SetItemState(event.m_itemIndex, 0, wx.LIST_STATE_SELECTED)

    def onDeselectAll(self):
        selected_item = self.GetFirstSelected()
        while selected_item != -1:
            self.SetItemState(selected_item, 0, wx.LIST_STATE_SELECTED)
            selected_item = self.GetNextSelected(selected_item)

    def _rowFormatter(self, listItem, object):
        """Handles the formatting of rows for object list view
        :param: wx.ListCtrl listitem
        :param: ModelObject object

        :rtype: None
        """
        objects = self.GetSelectedObjects()

        # if self.currentItem and object in self.currentItem:
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