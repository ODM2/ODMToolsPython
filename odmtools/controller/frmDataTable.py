from wx.lib.pubsub import pub as Publisher
from odmtools.view.clsDataTable import DataTable
import pandas as pd
import numpy as np

import wx
__author__ = 'jmeline'


class FrmDataTable(DataTable):
    def __init__(self, parent, **kwargs):
        self.parent = parent
        self.memDB = None
        DataTable.__init__(self, parent, **kwargs)

    def init_publishers(self):
        Publisher.subscribe(self.onChangeSelection, "changeTableSelection")
        Publisher.subscribe(self.onRefresh, "refreshTable")
        Publisher.subscribe(self.olvDataTable.onDeselectAll, "deselectAllDataTable")

    def init(self, memDB):
        self.olvDataTable.init(memDB)

    def onItemSelected(self, event):
        pass

    def onRefresh(self, e):
        self.olvDataTable.dataframe = self.memDB.getDataValuesDF()
        self.dataObjects = self.olvDataTable.dataframe.values.tolist()
        # self.myOlv.RefreshItems()

    def onChangeSelection(self,  datetime_list=None):
        """
        Select values within
        """
        self.olvDataTable.onDeselectAll()

        if isinstance(datetime_list, pd.DataFrame):
            try:
                self.enableSelectDataTable = True
                olv = self.olvDataTable.dataframe.set_index("LocalDateTime")
                filtered_dataframe = self.olvDataTable.dataframe[olv.index.isin(datetime_list.index)]
                results = np.where(self.olvDataTable.dataframe.index.isin(filtered_dataframe.index))

                for i in results[0]:
                    self.olvDataTable.SetItemState(i, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)
                self.olvDataTable.Focus(results[0][0])
                self.enableSelectDataTable = False
            except:
                pass
    def clear(self):
        self.memDB = None
        self.olvDataTable.DeleteAllItems()
        self.olvDataTable.dataframe = None
        self.dataObjects = None

    def stopEdit(self):
        self.clear()


if __name__ == "__main__":
    app = wx.App()
    frame = wx.Frame(None)
    panel = FrmDataTable(frame)
    frame.Show()
    app.MainLoop()
