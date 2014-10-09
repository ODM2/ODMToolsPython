import wx

from odmtools.controller.frmAddPoints import AddPoints


__author__ = 'Jacob'


class TestAddPoints:
    def setup(self):
        self.app = wx.App()
        self.frame = AddPoints(None)
        self.olv = self.frame.olv
        assert self.olv
        assert len(self.olv.GetObjects()) == 0

    def tearDown(self):
        print "Closing down frame"
        self.frame.Destroy()

    def test_onAddBtn(self):
        self.olv.AddObject(self.olv.sampleRow())
        assert len(self.olv.GetObjects()) == 1
        self.olv.AddObject(self.olv.sampleRow())
        assert len(self.olv.GetObjects()) == 2
        assert not len(self.olv.GetObjects()) == 3

        self.olv.SetObjects(None)
        assert not self.olv.GetObjects()



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



    def test_onClearAllBtn(self):
        self.olv.SetObjects(None)
        assert not self.olv.GetObjects()



    def test_onUploadBtn(self):
        pass

    def test_onFinishedBtn(self):
        pass






