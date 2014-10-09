from odmtools.controller.olvAddPoint import Points
from odmtools.controller.logicCellEdit import CellEdit

__author__ = 'Jacob'

class TestLogicCellEdit:
    def setup(self):
        self.parent = None
        self.serviceManager = None
        self.recordService = None

    def tearDown(self):
        pass

    def test_imgGetterDataValue(self):
        ## Test unicode, int, float,
        tests = [u'-9999', 10, 14.5, -9999]


        for test in tests:
            result = CellEdit(self.parent, self.serviceManager, self.recordService)\
                .imgGetterDataValue(Points(dataValue=test))
            if result == "error":
                assert False
            else:
                assert True

    def test_imgGetterUTCOffSet(self):
        ## Test int
        tests = range(-12, 12)

        for test in tests:
            result = CellEdit(self.parent, self.serviceManager, self.recordService)\
                .imgGetterUTCOFFset(Points(utcOffSet=str(test)))
            if result == "error":
                assert False
            else:
                assert True

    def test_imgGetterValueAccuracy(self):
        ## Test float, NULL, int
        import numpy as np
        tests = np.arange(-100, 100, 0.1).tolist() + ["NULL"] + range(-100, 100)

        for test in tests:
            result = CellEdit(self.parent, self.serviceManager, self.recordService)\
                .imgGetterValueAcc(Points(valueAccuracy=str(test)))
            if result == "error":
                assert False
            else:
                assert True

    def test_imgGetterOffsetValue(self):
        ## Test int, float, NULL
        import numpy as np
        tests = np.arange(-100, 100, 0.1).tolist() + ["NULL"] + range(-100, 100)

        for test in tests:
            result = CellEdit(self.parent, self.serviceManager, self.recordService)\
                .imgGetterOffSetValue(Points(offSetValue=str(test)))
            if result == "error":
                assert False
            else:
                assert True









