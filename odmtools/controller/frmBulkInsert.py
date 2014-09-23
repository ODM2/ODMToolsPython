"""
    Bulk Insert of points
"""
import datetime
import wx
import odmtools.view.clsBulkInsert as clsBulkInsert
import odmtools.controller.olvAddPoint as olv
import pandas as pd
import numpy as np

__author__ = 'Jacob'


class BulkInsert(clsBulkInsert.BulkInsert):
    def __init__(self, parent):
        clsBulkInsert.BulkInsert.__init__(self, parent)
        self.parent = parent


    def onUpload(self, event):
        """Reads csv into pandas object

        Parameters
        ----------
        filepath : string
            path to csv file
        """

        ## Obtain CSV filepath
        openFileDialog = wx.FileDialog(self, "Open CSV file", "", "", "CSV files (*.csv)|*.csv",
                                       wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        value = openFileDialog.ShowModal()

        if value == wx.ID_CANCEL:
            return

        filepath = openFileDialog.GetPath()

        try:
            data = pd.read_csv(filepath, dtype={'UTCOffset': np.int32}, converters={
                "DataValue": self.checkDataValue,
                "Date": self.checkDate,
                #"CensorCode": self.checkCensorCode,
            })
            pointList = []
            for i in data.columns[4:]:
                data[i] = data[i].astype(str)

            for count, row in data.iterrows():
                try:
                    values = row.tolist()
                    pointList.append(olv.Points(*values))
                    #p = olv.Points(*values)
                except Exception as e:
                    print "Inside: ", e
                    continue


            #self.parent.olv.AddObjects(data.to_dict())
        except Exception as e:
            print "Outside:", e
            return None

        self.parent.olv.AddObjects(pointList)

        self.Hide()

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

    def checkDataValue(self, item):
        try:
            value = int(item)
            if isinstance(value, int):
                return value
            value = float(item)
            if isinstance(value, float):
                return value
        except:
            return "NULL"

    def checkDate(self, item):
        try:
            format = '%Y-%m-%d'
            value = datetime
        except:
            pass
        return item

    def checkCensorCode(self, item):
        try:
            return str(item)
        except:
            return item


if __name__ == '__main__':
    app = wx.App(useBestVisual=True)
    m = BulkInsert(None)
    m.Show()
    app.MainLoop()
