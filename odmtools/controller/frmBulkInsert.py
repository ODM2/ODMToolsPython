"""
    Bulk Insert of points
"""
import wx
import odmtools.view.clsBulkInsert as clsBulkInsert
import odmtools.controller.olvAddPoint as olv
import pandas as pd
from pandas.parser import CParserError
import csv
import StringIO

__author__ = 'Jacob'


class BulkInsert(clsBulkInsert.BulkInsert):
    def __init__(self, parent):
        clsBulkInsert.BulkInsert.__init__(self, parent)
        self.parent = parent

        self.col = ['DataValue', 'Date', 'Time', 'UTCOffSet', 'CensorCode', 'ValueAccuracy', 'OffSetValue',
               'OffSetType', 'QualifierCode', 'LabSampleCode']

    def obtainFilePath(self):
        ## Obtain CSV filepath

        openFileDialog = wx.FileDialog(self, "Open CSV file", "", "", "CSV files (*.csv)|*.csv",
                                   wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        value = openFileDialog.ShowModal()

        if value == wx.ID_CANCEL:
            return None
        filepath = openFileDialog.GetPath()

        return filepath

    def readDataFromCSV(self, filepath):
        
        csv_data = StringIO.StringIO()
        
        try:
            with open(filepath, 'rb') as f:
                reader = csv.reader(f)
                for row in reader:
                    csv_data.write(str(row).strip('[]').replace("'", "") + '\n')
        except csv.Error as e:
            with open (filepath, 'rU') as f:
                reader = csv.reader(f)
                for row in reader:
                    csv_data.write(str(row).strip('[]').replace("'", "") + '\n')
        
        csv_data.seek(0)
        
        try:
            #data = pd.read_csv(filepath, skiprows=[1], engine='c', lineterminator='\n')
            data = pd.read_csv(csv_data, skiprows=[1], engine='c', converters={0: str.strip,
                                1: str.strip,
                                2: str.strip,
                                3: str.strip,
                                4: str.strip,
                                5: str.strip,
                                6: str.strip,
                                7: str.strip,
                                8: str.strip,
                                9: str.strip})
        except CParserError as e:

            msg = wx.MessageDialog(None, "There was an issue trying to parse your file. "
                                         "Please compare your csv with the template version as the file"
                                         " you provided "
                                         "doesn't work: %s" % e, 'Issue with csv', wx.OK | wx.ICON_WARNING |
                                   wx.OK_DEFAULT)
            value = msg.ShowModal()
            return False
        
        ## Change 'nan' to 'NULL' for consistency
        data.fillna(" NULL", inplace=True)

        for i in data.columns[3:]:
            data[i] = data[i].astype(str)
        return data

    def loadIntoDataFrame(self, data):
        pointList = []
        keepGoing = True
        dlg = wx.ProgressDialog("Upload Progress", "Uploading %s values" % len(data), maximum=len(data),
                    parent=self,
                    style=0 | wx.PD_APP_MODAL | wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME |
                          wx.PD_ESTIMATED_TIME | wx.PD_REMAINING_TIME | wx.PD_AUTO_HIDE)

        for count, row in data.iterrows():
            if not keepGoing:
                break
            try:
                values = row.tolist()
                pointList.append(olv.Points(*values))
                (keepGoing, _) = dlg.Update(count, "%s/%s Objects Uploaded" % (count, len(data)))

            except TypeError as e:
                dlg.Destroy()
                msg = wx.MessageDialog(None, "There was an issue trying to parse your file. "
                                             "Please check to see if there could be more columns or"
                                             " values than"
                                             " the program expects",
                                       'Issue with csv', wx.OK | wx.ICON_WARNING | wx.OK_DEFAULT)
                value = msg.ShowModal()
                return False

        dlg.Destroy()
        return pointList
    def onUpload(self, event):
        """Reads csv into pandas object

        Parameters
        ----------
        filepath : string
            path to csv file
        """

        filepath = self.obtainFilePath()

        if not filepath:
            return False
        
        data = self.readDataFromCSV(filepath)
        
        if data.empty:
            return False

        pointList = self.loadIntoDataFrame(data)

        if not pointList:
            return False

        self.parent.olv.AddObjects(pointList)
        del pointList
        self.EndModal(0) # Denver
        #self.Hide()
        self.parent.Raise()
        event.Skip()

    def onTemplate(self, event):
        """
                DataValues: Floats or -9999 (No data value)
                Date: --+ String
                        |-- Later to be combined into one
                Time: --+ String

                UTFOffSet: -12 - 12
                CensorCode: 'gt|nc|lt|nd|pnq'
                ValueAccuracy: Float
                OffsetValue: Float
                OffsetType: String
                QualifierCode: String

        :param event:
        :return:
        """
        saveFileDialog = wx.FileDialog(self, "Save Bulk Insert Template", "", "", "CSV files (*.csv)|*.csv", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        value = saveFileDialog.ShowModal()
        if value == wx.ID_CANCEL:
            return
        filepath = saveFileDialog.GetPath()
        df = pd.DataFrame(columns=self.col)
        df.loc[0] = ['FLOAT|INT', 'YYYY-MM-DD', 'HH:MM:SS', 'INT', 'gt|nc|lt|nd|pnq', 'FLOAT', 'FLOAT',
                     'String', 'String', 'String']
        df.loc[1] = ['-9999', '2005-06-29', '14:20:15', '-7', 'nc', "1.2", "1", "NULL", "NULL", "NULL"]
        df.to_csv(filepath, index=False)

        self.EndModal(0) # Denver
        #self.Hide()
        self.parent.Raise()

    def onClose(self, event):
        self.EndModal(0) # Denver
        #self.Hide()
        self.parent.Raise()

if __name__ == '__main__':
    app = wx.App(useBestVisual=True)
    m = BulkInsert(None)
    m.Show()
    app.MainLoop()
