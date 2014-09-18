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

        sb = self.frame.sb
        assert sb
        text = sb.GetStatusText()
        assert not text
        string = "Added a row"
        sb.SetStatusText(string)
        text = sb.GetStatusText()
        assert text == string

    def test_onDeleteBtn(self):
        size = 10000
        values = [self.olv.sampleRow() for _ in range(size)]
        assert values and len(values) == size
        self.olv.AddObjects(values)
        assert len(self.olv.GetObjects()) == size
        sb = self.frame.sb
        assert sb
        assert not sb.GetStatusText()

        selectedObjs = self.olv.GetObjects()
        assert selectedObjs
        if len(selectedObjs) > 1:
            length = len(selectedObjs)
            self.olv.RemoveObjects(selectedObjs)
            assert len(self.olv.GetObjects()) == 0
            string = "Removed %s items" % length
            sb.SetStatusText(string)
            assert sb.GetStatusText() == string
        else:
            assert False

        self.olv.AddObject(self.olv.sampleRow())
        selectedObjs = self.olv.GetObjects()
        if len(selectedObjs) > 1:
            assert False
        self.olv.RemoveObjects(selectedObjs)
        sb.SetStatusText("")
        assert sb.GetStatusText() == ""
        string = "Removing %s" % selectedObjs
        sb.SetStatusText(string)
        assert sb.GetStatusText() == string


    def test_onClearAllBtn(self):
        self.olv.SetObjects(None)
        assert not self.olv.GetObjects()



    def test_onUploadBtn(self):
        pass

    def test_onFinishedBtn(self):
        pass






