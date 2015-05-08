import wx
import os
from odmtools.controller.frmBulkInsert import BulkInsert

class TestBulkInsert:
    def setup(self):
        self.app = wx.App()
        self.BulkInsert = BulkInsert(None)
        self.CSVPath = os.path.join('test_controller', 'testFiles', 'test.csv')

    def teardown(self):
        pass

    def test_obtainFilePath(self):
        assert self.BulkInsert
        assert self.CSVPath

    def test_readDataFromCSV(self):
        assert self.BulkInsert
        assert self.CSVPath
        result = self.BulkInsert.readDataFromCSV(self.CSVPath)
        if not isinstance(result, bool):
            assert not result.empty
        else:
            assert result
        assert len(result) == 1

    def test_loadIntoDataFrame(self):
        assert self.BulkInsert
        assert self.CSVPath
        result = self.BulkInsert.readDataFromCSV(self.CSVPath)
        assert not result.empty

    def test_onUpload(self):
        assert self.BulkInsert
        assert isinstance(self.BulkInsert.col, list)
        assert self.CSVPath






