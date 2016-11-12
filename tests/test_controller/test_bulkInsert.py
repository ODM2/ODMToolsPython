import wx
import os
from odmtools.controller.frmBulkInsert import BulkInsertController

class TestBulkInsert:
    def setup(self):
        self.app = wx.App()
        self.BulkInsert = BulkInsertController(None)
        path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.CSVPath = os.path.join(path, 'example_files', 'exampleBulkInsert.csv')
        self.CSVPath2 =os.path.join(path, 'example_files', 'exampleBulkInsert_win.csv')
        self.CSVPath3 =os.path.join(path, 'example_files', 'CSVUploadTemplate_Mac.csv')
        self.template_paths = [self.CSVPath, self.CSVPath2, self.CSVPath3]
    def teardown(self):
        pass

    def test_obtainFilePath(self):
        assert self.BulkInsert
        assert self.CSVPath

    def test_readDataFromCSV(self):
        assert self.BulkInsert
        assert self.CSVPath
        for i in self.template_paths:
            example = self.BulkInsert.readDataFromCSV(i)
            if not isinstance(example, bool):
                assert not example.empty
            else:
                assert example
            # assert len(example) == 1

        # test reading 

    def test_loadIntoDataFrame(self):
        assert self.BulkInsert
        assert self.CSVPath
        result = self.BulkInsert.readDataFromCSV(self.CSVPath)
        assert not result.empty

    def test_onUpload(self):
        assert self.BulkInsert
        assert isinstance(self.BulkInsert.columns, list)
        assert self.CSVPath






