import wx
import wx.grid
import logging
import itertools as iter
<<<<<<< HEAD
import pandas as pd
from odmtools.lib.ObjectListView import ColumnDefn, FastObjectListView, VirtualObjectListView
from wx.lib.pubsub import pub as Publisher
import numpy as np
import timeit
=======
from odmtools.lib.oldOlv import ColumnDefn, FastObjectListView
from wx.lib.pubsub import pub as Publisher
#import datetime
>>>>>>> 4788d9903a4f70315eacb6cb6b036e7d75f330e8

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

        #self.myOlv.Bind(wx.EVT_LIST_ITEM_FOCUSED, self.onItemSelected)
        self.myOlv.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onItemSelected)
        self.myOlv.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.onItemSelected)
        # for wxMSW
        self.Bind(wx.EVT_COMMAND_RIGHT_CLICK, self.OnRightClick)

        # for wxGTK
        self.Bind(wx.EVT_RIGHT_UP, self.OnRightClick)
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnRightClick)

        #self.myOlv.Bind(wx.EVT_CHAR, self.onKeyPress)
        #self.myOlv.Bind(wx.EVT_LIST_KEY_DOWN, self.onKeyPress)
        Publisher.subscribe(self.onChangeSelection, ("changeTableSelection"))
        Publisher.subscribe(self.onRefresh, ("refreshTable"))

        self.ascending = False
        self.enableSelectDataTable = False

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

        columns = [ColumnDefn(x.strip(), align="left", valueGetter=i, minimumWidth=125, width=-1,
                              stringConverter='%Y-%m-%d %H:%M:%S' if "date" in x.lower() else '%s')
                   for x, i in self.memDB.getEditColumns()]

        self.myOlv.useAlternateBackColors = True
        self.myOlv.oddRowsBackColor = wx.Colour(191, 217, 217)

        values = self.memDB.getDataValuesforEdit()
        value_length = len(values)

        self.myOlvDataFrame = pd.DataFrame(values, columns=[x.title for x in columns])
        self.myOlv.SetColumns(columns)

        self.dataObjects = self.myOlvDataFrame.values.tolist()

        self.myOlv.SetObjectGetter(self.objectGetter)
        self.myOlv.SetItemCount(value_length)


    def objectGetter(self, index):
        """
        A Virtual list has to have a callable installed that says which model object is shown
        at a given index
        """
        return self.dataObjects[index % len(self.dataObjects)]

    def OnRightClick(self, event):
        """
        Allow users to sort based off of column
        """
        try:
            selected_column = self.GetOLVColClicked(event=None)
            if self.ascending:
                self.myOlvDataFrame.sort(self.myOlvDataFrame.columns[selected_column], inplace=True)
                self.ascending = False
            elif not self.ascending:
                self.myOlvDataFrame.sort(self.myOlvDataFrame.columns[selected_column], ascending=False, inplace=True)
                self.ascending = True
            self.dataObjects = self.myOlvDataFrame.values.tolist()
            if self.myOlv.GetItemCount:
                itemFrom = self.myOlv.GetTopItem()
                itemTo   = self.myOlv.GetTopItem()+1 + self.myOlv.GetCountPerPage()
                itemTo   = min(itemTo, self.myOlv.GetItemCount()-1)
                self.myOlv.RefreshItems(itemFrom, itemTo)
        except Exception as e:
            print e

    def GetOLVColClicked(self, event):

        # DevPlayer@gmail.com  2011-01 Jan-13
        # For use with a 3rd party module named ObjectListView
        # used with wxPython.

        """
        GetColClicked( event ) -> int Column number of mouse click.

        Get ObjectListView() column the user single-left-clicked the mouse in.

        You can use the column number to set the modelObject's attributes
        without removing, re-adding, resorting the items in the OVL.

        This event handler is often bound to the event handler of the
        wx.EVT_LIST_ITEM_SELECTED event. Other events may be needed for
        the column's labels - the labels visually naming a column.

        This assumes the OLV.LayoutDirection() is LTR.
        """

        # ----------------------------------------------------------
        # Get the mouse position. Determine which column the user
        # clicked in.
        # This could probably all be done in some list hit test event.
        # Not all OS platforms set all events m_...atributes. This is a
        # work around.

        # Get point user clicked, here in screen coordinates.
        # Then convert the point to OVL control coordinates.

        spt = wx.GetMousePosition()
        fpt = self.myOlv.ScreenToClient(spt)  # USE THIS ONE
        x, y = fpt

        # Get all column widths, individually, of the OLV control .
        # Then compare if the mouse clicked in that column.

        # Make this a per-click calculation as column widths can
        # change often by the user and dynamically by different
        # lengths of data strings in rows.

        last_col = 0
        col_selected = None
        for col in range(self.myOlv.GetColumnCount()):

            # Get this OLV column's width in pixels.

            col_width = self.myOlv.GetColumnWidth(col)

            # Calculate the left and right vertical pixel positions
            # of this current column.

            left_pxl_col = last_col
            right_pxl_col = last_col + col_width - 1

            # Compare mouse click point in control coordinates,
            # (verse screen coordinates) to left and right coordinate of
            # each column consecutively until found.

            if left_pxl_col <= x <= right_pxl_col:
                # Mouse was clicked in the current column "col"; done

                col_selected = col
                break

            col_selected = None
            # prep for next calculation of next column

            last_col = last_col + col_width

        return col_selected

    def onRefresh(self, e):
        pass

    def clear(self):
        self.memDB = None
        self.record_service = None
        self.myOlv.DeleteAllItems()
        self.myOlvDataFrame = None

    def onItemSelected(self, event):
        """

        Disable selecting of an item in the DataTable, only sorting is available
        """
        if not self.enableSelectDataTable:
            self.myOlv.SetItemState(event.m_itemIndex, 0, wx.LIST_STATE_SELECTED)



    def onChangeSelection(self,  datetime_list=[]):
        """
        Select values within
        """
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







