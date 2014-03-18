#Boa:FramePanel:Panel1

import wx
from wx.lib.pubsub import pub as Publisher

try:
    from agw import flatnotebook as fnb
except ImportError:  # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.flatnotebook as fnb

import matplotlib

matplotlib.use('WXAgg')
import plotTimeSeries
import plotSummary
import plotHistogram
import plotBoxWhisker
import plotProbability
from clsPlotOptions import PlotOptions, SeriesPlotInfo

[wxID_PANEL1, wxID_PAGEBOX, wxID_PAGEHIST, wxID_PAGEPROB,
 wxID_PAGESUMMARY, wxID_PAGETIMESERIES, wxID_TABPLOTS
] = [wx.NewId() for _init_ctrls in range(7)]


class pnlPlot(fnb.FlatNotebook):
    def __init__(self, parent, id, size, style, name, pos=None):
        self._init_ctrls(parent)
        self.parent = parent

    def _init_ctrls(self, parent):
        fnb.FlatNotebook.__init__(self, id=wxID_TABPLOTS, name=u'tabPlots',
                                  parent=parent, pos=wx.Point(0, 0), size=wx.Size(491, 288),
                                  agwStyle=fnb.FNB_NODRAG | fnb.FNB_HIDE_TABS)
        # style |= fnb.FNB_HIDE_TABS
        # self.book.SetAGWWindowStyleFlag(style)

        self.pltTS = plotTimeSeries.plotTimeSeries(id=wxID_PAGETIMESERIES, name='pltTS',
                                                   parent=self, pos=wx.Point(0, 0), size=wx.Size(605, 458),
                                                   style=wx.TAB_TRAVERSAL)
        self.AddPage(self.pltTS, 'TimeSeries')

        self.pltProb = plotProbability.plotProb(id=wxID_PAGEPROB, name='pltProb',
                                                parent=self, pos=wx.Point(0, 0), size=wx.Size(605, 458),
                                                style=wx.TAB_TRAVERSAL)
        self.AddPage(self.pltProb, 'Probablity')

        self.pltHist = plotHistogram.plotHist(id=wxID_PAGEHIST, name='pltHist',
                                              parent=self, pos=wx.Point(0, 0), size=wx.Size(605, 458),
                                              style=wx.TAB_TRAVERSAL)
        self.AddPage(self.pltHist, 'Histogram')

        self.pltBox = plotBoxWhisker.PlotBox(id=wxID_PAGEBOX, name='pltBox',
                                             parent=self, pos=wx.Point(0, 0), size=wx.Size(605, 458),
                                             style=wx.TAB_TRAVERSAL)
        self.AddPage(self.pltBox, 'Box/Whisker')

        self.pltSum = plotSummary.plotSummary(id=wxID_PAGESUMMARY, name=u'pltSum',
                                              parent=self, pos=wx.Point(784, 256), size=wx.Size(437, 477),
                                              style=wx.TAB_TRAVERSAL)
        self.AddPage(self.pltSum, 'Summary')

        Publisher.subscribe(self.onDateChanged, ("onDateChanged"))
        Publisher.subscribe(self.onPlotType, ("onPlotType"))
        Publisher.subscribe(self.onShowLegend, ("onShowLegend"))
        Publisher.subscribe(self.onNumBins, ("onNumBins"))
        Publisher.subscribe(self.onRemovePlot, ("removePlot"))
        Publisher.subscribe(self.onChangeSelection, ("changePlotSelection"))
        Publisher.subscribe(self.onChangeSelectionDT, ("changePlotSelectionDT"))
        Publisher.subscribe(self.onUpdateValues, ("updateValues"))

        self.selectedSerieslist = []
        self._seriesPlotInfo = None
        self.editID = None


    def onUpdateValues(self, event):
        self.pltTS.updateValues()


    def onChangeSelection(self, sellist):
        self.pltTS.changeSelection(sellist)

    def onChangeSelectionDT(self, sellist):
        self.pltTS.changeSelectionDT(sellist)

    def onRemovePlot(self, seriesID):

        # self.selectedSerieslist.remove(seriesID)
        self._seriesPlotInfo.update(seriesID, False)
        self.pltTS.Plot(self._seriesPlotInfo)
        self.pltSum.Plot(self._seriesPlotInfo)
        self.pltBox.Plot(self._seriesPlotInfo)
        self.pltHist.Plot(self._seriesPlotInfo)
        self.pltProb.Plot(self._seriesPlotInfo)

    def onNumBins(self, numBins):
        self.pltHist.changeNumOfBins(numBins)

    def onDateChanged(self, startDate, endDate):
        self.pltTS.onDateChanged(startDate, endDate)

    def onPlotType(self, event, ptype):
        self.pltTS.onPlotType(ptype)
        self.pltProb.onPlotType(ptype)


    def onShowLegend(self, event, isVisible):
        self.pltTS.onShowLegend(isVisible)
        self.pltProb.onShowLegend(isVisible)

    def stopEdit(self):
        self._seriesPlotInfo.stopEditSeries()
        self.editID = None
        self.pltTS.stopEdit()

    def addEditPlot(self, memDB, seriesID, record_service):
        self.record_service = record_service
        if not self._seriesPlotInfo:
            options = PlotOptions("Both", 0, False, False, True)
            self._seriesPlotInfo = SeriesPlotInfo(memDB, options)
        self.editID = seriesID
        self._seriesPlotInfo.setEditSeries(self.editID)
        self.pltTS.setEdit(self.editID)

    def addPlot(self, memDB, seriesID):

        if not self._seriesPlotInfo:
            options = PlotOptions("Both", 0, False, False, True)
            self._seriesPlotInfo = SeriesPlotInfo(memDB, options)

        self._seriesPlotInfo.update(seriesID, True)
        self.selectedSerieslist.append(seriesID)

        self.pltSum.Plot(self._seriesPlotInfo)
        self.pltProb.Plot(self._seriesPlotInfo)
        self.pltBox.Plot(self._seriesPlotInfo)
        self.pltHist.Plot(self._seriesPlotInfo)

        self.pltTS.Plot(self._seriesPlotInfo)

    #     self.PlotGraph()
    def selectPlot(self, value):
        #select the corresponding page of the notebook
        self.SetSelection(value)

    def getActivePlotID(self):
        return self.GetSelection()

    def close(self):
        self.pltTS.close()

    def clear(self):
        self.pltSum.clear()
        self.pltHist.clear()
        self.pltProb.clear()
        self.pltBox.clear()
        self.pltTS.clear()

        # Set title of TimeSeries to default
        self.pltTS.timeSeries.set_title("No Data To Plot")

        self._seriesPlotInfo = None

    ##    def get_edit_metadata(self)





