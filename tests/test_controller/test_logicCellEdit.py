# coding=utf-8
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

    def test_imgGetterTime(self):
        tests = [u'00:00:00', u'0:0:0', u'23:00:00', u'12:00:12', "00:00:00"]

        for test in tests:
            print test
            result = CellEdit(self.parent, self.serviceManager, self.recordService)\
                .imgGetterTime(Points(time=test))
            if result == "error":
                assert False
            else:
                assert True

        failTests = [u'Hello', u'a2:s3:s4', u'00:oo:00', u'♣☺☻♥', u'00:♦:00', u'26:05:50',
                     u'12:90:00', u'12:40:80', u'-0:-3:-1']

        for test in failTests:
            result = CellEdit(self.parent, self.serviceManager, self.recordService)\
                .imgGetterTime(Points(time=test))
            if result == "error":
                assert True
            else:
                assert False

    def test_imgGetterDate(self):
        tests = [u'1973-12-15', u'2016-2-29', u'2016-02-29']

        for test in tests:
            result = CellEdit(self.parent, self.serviceManager, self.recordService)\
                .imgGetterDate(Points(date=test))
            if result == "error":
                print test
                assert False
            else:
                assert True

        failTests = [u'1999-90-9', u'12/12/2012']

        for test in failTests:
            result = CellEdit(self.parent, self.serviceManager, self.recordService)\
                .imgGetterTime(Points(time=test))
            if result == "error":
                assert True
            else:
                assert False


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









