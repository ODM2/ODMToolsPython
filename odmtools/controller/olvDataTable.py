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
        self.annotations = None
        self.annotations_grouped = {}

    def init(self, memDB):
        self.memDB = memDB

        self.useAlternateBackColors = True
        self.oddRowsBackColor = wx.Colour(191, 217, 217)

        self.dataframe = self.memDB.getDataValuesDF()
        self.annotations = self.memDB.get_annotations()

        sort_by_index = self.dataframe.columns.tolist().index("valuedatetime")
        self.dataframe.sort_values(self.dataframe.columns[sort_by_index], inplace=True)

        self.annotations_grouped = self.__group_annotations()
        self.dataObjects = self.__merge_dataframe_with_annotations()

        col = self.memDB.get_columns_with_annotations()

        columns = \
            [ColumnDefn(x.strip(), align="left", valueGetter=i, minimumWidth=125, width=125,
                        stringConverter='%Y-%m-%d %H:%M:%S' if "valuedatetime" == x.lower() else '%s')
             for x, i in col]

        self.SetColumns(columns)


        self.SetObjectGetter(self.ObjectGetter)
        self.SetItemCount(len(self.dataObjects))

    def __merge_dataframe_with_annotations(self):
        data_list = self.dataframe.values.tolist()
        data = data_list

        for key, value in self.annotations_grouped.iteritems():
            for i in range(0, len(data_list)):
                if key in data[i]:
                    data[i].append(value)
                    break

        return data

    def __group_annotations(self):
        """
        Ideally, this method should only be called once. Use self.grouped_annotations after calling this method
        :return:
        """
        anno_list = self.annotations.values.tolist()

        anno = {}
        for i in range(0, len(anno_list)):
            value_id = anno_list[i][1]
            annotation_code = anno_list[i][-1]
            if value_id in anno:
                anno[value_id].append(annotation_code)
            else:
                anno[value_id] = [annotation_code]

        return anno

    def EnableSorting(self):
        self.Bind(wx.EVT_LIST_COL_CLICK, self.on_column_selected)
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

    def on_column_selected(self, event):
        """
        Allows users to sort by clicking on columns
        """
        if not isinstance(self.dataframe, pd.DataFrame):
            return

        if self.dataframe.empty:
            return

        if not len(self.dataObjects):
            return

        self.sortColumn(event.Column)

    def sortColumn(self, selected_column):
        oldSortColumnIndex = self.sortedColumnIndex
        self.sortedColumnIndex = selected_column

        self.sortAscending = not self.sortAscending
        self.dataframe.sort_values(self.dataframe.columns[selected_column], ascending=self.sortAscending, inplace=True)

        self._UpdateColumnSortIndicators(selected_column, oldSortColumnIndex)

        # self.dataObjects = self.dataframe.values.tolist()
        self.dataObjects = self.__merge_dataframe_with_annotations()

        if self.GetItemCount():
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