"""
    Bulk Insert of points
"""
import wx
import odmtools.view.clsBulkInsert as clsBulkInsert
import pandas as pd

__author__ = 'Jacob'


class BulkInsert(clsBulkInsert.BulkInsert):
    def __init__(self, parent):
        clsBulkInsert.BulkInsert.__init__(self, parent)


    def onUpload(self, event):
        """Reads csv into pandas object

        Parameters
        ----------
        filepath : string
            path to csv file
        skip : int
            indicates the skip amount to begin reading
        """

        ## Obtain CSV filepath
        openFileDialog = wx.FileDialog(self, "Open CSV file", "", "", "CSV files (*.csv)|*.csv",
                                       wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        value = openFileDialog.ShowModal()

        if value == wx.ID_CANCEL:
            return

        filepath = openFileDialog.GetPath()

        try:
            data = pd.read_csv(filepath, index_col=0)
            return data.sort()
        except:
            return None



        #print "On Upload!"
        # filepath = wx.FileDialog()
        #if not filepath:
        #    raise RuntimeError("FilePath cannot be null")

        #logger.debug("filepath: %s" % filepath)
        #logger.debug("sep: %s" % sep)
        #logger.debug("skiprows: %s" % skip)

        event.Skip()
    def onTemplate(self, event):
        #print "On template!"
        event.Skip()
    def onClose(self, event):
        self.Hide()
        event.Skip()


if __name__ == '__main__':
    app = wx.App(useBestVisual=True)
    m = BulkInsert(None)
    m.Show()
    app.MainLoop()
