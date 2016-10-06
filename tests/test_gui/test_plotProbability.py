import wx
import numpy as np
from tests.test_util import build_db, add_series, add_bulk_data_values
from odmtools.odmdata import MemoryDatabase
from odmtools.odmservices import SeriesService
from odmtools.gui import plotProbability
from odmtools.gui.pnlPlot import wxID_PAGEPROB


__author__ = 'jmeline'

# hide the iCCP warnings for the tests
wx.Log.SetLogLevel(0)

class TestPlotProbability:
    def setup(self):
        self.app = wx.App()
        self.frame = wx.Frame(None)
        self.pltProb = plotProbability.plotProb(id=wxID_PAGEPROB, name='pltProb',
                                                parent=self.frame, pos=wx.Point(0, 0), size=wx.Size(605, 458),
                                                style=wx.TAB_TRAVERSAL)


        self.connection_string = "sqlite:///:memory:"
        self.series_service = SeriesService(connection_string=self.connection_string, debug=False)
        self.session = self.series_service._session_factory.get_session()
        engine = self.series_service._session_factory.engine
        build_db(engine)

        self.memory_db = MemoryDatabase()

        self.memory_db.set_series_service(self.series_service)
        self.series = add_series(self.session)
        print "Series: ", self.series
        self.memory_db.initEditValues(self.series.id)
        # add_bulk_data_values(self.session, self.series_service)


    def test_onPlotType(self):
        assert self.app
        assert self.frame
        assert self.pltProb

        # add some values to the probability plot

        valid_values = ['line', 'both', 'point', 'test']

        try:
            for i in valid_values:
                self.pltProb.onPlotType(ptype=i)
        except Exception as e:
            print e
            assert False








