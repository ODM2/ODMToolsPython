from odmtools.controller.olvAddPoint import Points
from odmtools.controller.logicCellEdit import CellEdit

__author__ = 'Jacob'

class TestLogicCellEdit:
    def setup(self):
        pass

    def tearDown(self):
        pass

    def test_imgGetterDataValue(self):
        ## Test unicode, int, float,
        tests = [u'-9999', 10, 14.5, -9999, '']

        for test in tests:
            result = CellEdit().imgGetterDataValue(Points(dataValue=test))
            if result == "error":
                assert False


