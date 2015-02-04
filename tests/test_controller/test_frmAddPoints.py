import wx

from odmtools.controller.frmAddPoints import AddPoints
from odmtools.controller.olvAddPoint import Points


__author__ = 'Jacob'


class TestAddPoints:
    def setup(self):
        self.app = wx.App()
        self.frame = AddPoints(None)
        self.olv = self.frame.olv
        assert self.olv
        assert len(self.olv.GetObjects()) == 0

    def tearDown(self):
        self.frame.Destroy()

    def test_onAddBtn(self):
        self.olv.AddObject(self.olv.sampleRow())
        assert len(self.olv.GetObjects()) == 1
        self.olv.AddObject(self.olv.sampleRow())
        assert len(self.olv.GetObjects()) == 2
        assert not len(self.olv.GetObjects()) == 3

        self.olv.SetObjects(None)
        assert not self.olv.GetObjects()

        size = 99999
        objects = self._buildObjects(size)
        self.olv.SetObjects(objects)
        assert len(self.olv.GetObjects()) == size

        '''
        Note:
        If you need this event to
        be processed synchronously use
        (self.GetEventhandler().ProcessEvent(event)) to fire the event instead
        that way it will get handled before the next part of your code is
        executed.

        So for example

        def FireEvent(self):
            evt = MyEvent(...)
            self.GetEventHandler().ProcessEvent(evt)
            self.updateDrawing()
        '''

        evt = wx.PyCommandEvent(wx.EVT_BUTTON.typeId, self.frame.addRowBtn.GetId())
        #wx.PostEvent(self.frame.addRowBtn, evt)
        self.frame.GetEventHandler().ProcessEvent(evt)
        assert self.olv.GetObjects()

    def test_onDeleteBtn(self):
        size = 10000
        values = [self.olv.sampleRow() for _ in range(size)]
        assert values and len(values) == size
        self.olv.AddObjects(values)
        assert len(self.olv.GetObjects()) == size

        selectedObjs = self.olv.GetObjects()
        assert selectedObjs
        if len(selectedObjs) > 1:
            length = len(selectedObjs)
            self.olv.RemoveObjects(selectedObjs)
            assert len(self.olv.GetObjects()) == 0
        else:
            assert False

        self.olv.AddObject(self.olv.sampleRow())
        selectedObjs = self.olv.GetObjects()
        if len(selectedObjs) > 1:
            assert False
        self.olv.RemoveObjects(selectedObjs)

        assert not self.olv.GetObjects()
        self.olv.AddObjects(self._buildObjects(size))
        assert len(self.olv.GetObjects()) == size
        evt = wx.PyCommandEvent(wx.EVT_BUTTON.typeId, self.frame.deleteRowBtn.GetId())
        self.frame.GetEventHandler().ProcessEvent(evt)

    def test_onClearAllBtn(self):
        assert not self.olv.GetObjects()
        size = 100000
        self.olv.SetObjects(self._buildObjects(size))
        assert len(self.olv.GetObjects()) == size
        self.frame._clearAll()
        assert not self.olv.GetObjects()

    def test_customRemove(self):
        self.olv.AddObject(self.olv.sampleRow())
        assert len(self.olv.GetObjects()) == 1

        objects = self.olv.GetObjects()
        self.frame.customRemove(objects)
        assert not self.olv.GetObjects()

        ## Test order remains the same after removing
        size = 10000
        objects = self._buildObjects(size)
        for i in objects:
            print i.dataValue
        assert len(objects) == size
        tests = [1, 5, 25, 100, 150, 300, 600, 55, 9000]

        for test in objects:
            if test.dataValue in tests:
                if not self.frame.customRemove(test):
                    assert False

        currentObjects = self.olv.GetObjects()
        for obj in currentObjects:
            if obj.dataValue not in objects:
                assert False

    def test_isCorrect(self):
        import pandas as pd
        self.col = ['DataValue', 'Date', 'Time', 'UTCOffSet', 'CensorCode', 'ValueAccuracy', 'OffSetValue',
            'OffSetType', 'QualifierCode', 'LabSampleCode']
        df = pd.DataFrame(columns=self.col)
        df.loc[0] = ['FLOAT|INT', 'YYYY-MM-DD', 'HH:MM:SS', 'INT', 'gt|nc|lt|nd|pnq', 'FLOAT', 'FLOAT',
                     'String', 'String', 'String']
        size = 500
        pointList = []

        for i in range(1, size):
            df.loc[i] = ['-9999', '2005-06-29', '14:20:15', '-7', 'nc', "1.2", "1", "NULL", "NULL", "NULL"]
            pointList.append(Points(*df.loc[i]))

        assert len(df) == size
        assert len(pointList) == size - 1

        isCorrect = True
        for p in pointList:
            returnValue = self.olv.isCorrect(p)
            if returnValue == "error":
                isCorrect = False
        assert isCorrect

        """Bad case"""
        df.loc[len(df)+1] = ['-9999', '2005-06-29', '--:20:15', '-7', 'BadExample', "1.2", "1", "NULL", "NULL", "NULL"]
        pointList.append(Points(*df.append(df.loc[len(df)])))
        assert len(df) == size + 1
        assert len(pointList) == size

        isCorrect = True
        for p in pointList:
            if not self.olv.isCorrect(p):
                isCorrect = False
        assert not isCorrect



    def _buildObjects(self, size):
        return [Points(dataValue=x) for x in range(size)]


    def test_onUploadBtn(self):
        pass

    def test_onFinishedBtn(self):
        pass






