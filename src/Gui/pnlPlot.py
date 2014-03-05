#Boa:FramePanel:Panel1

import wx
from wx.lib.pubsub import pub as Publisher

try:
    from agw import flatnotebook as fnb
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.flatnotebook as fnb

import matplotlib
matplotlib.use('WXAgg')
import plotTimeSeries
import plotSummary
import plotHistogram
import plotBoxWhisker
import plotProbability
from clsPlotOptions import PlotOptions, OneSeriesPlotInfo, SeriesPlotInfo

[wxID_PANEL1, wxID_PAGEBOX, wxID_PAGEHIST, wxID_PAGEPROB,
wxID_PAGESUMMARY, wxID_PAGETIMESERIES, wxID_TABPLOTS
] = [wx.NewId() for _init_ctrls in range(7)]


class pnlPlot(fnb.FlatNotebook):

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

        self.pltBox = plotBoxWhisker.plotBox(id=wxID_PAGEBOX, name='pltBox',
                parent=self, pos=wx.Point(0, 0), size=wx.Size(605, 458),
                style=wx.TAB_TRAVERSAL)
        self.AddPage(self.pltBox, 'Box/Whisker')

        self.pltSum = plotSummary.plotSummary( id = wxID_PAGESUMMARY, name=u'pltSum',
              parent=self, pos=wx.Point(784, 256), size=wx.Size(437, 477),
              style=wx.TAB_TRAVERSAL)
        self.AddPage(self.pltSum, 'Summary')

        Publisher.subscribe(self.onDateChanged, ("onDateChanged"))
        Publisher.subscribe(self.OnPlotType, ("onPlotType"))
        Publisher.subscribe(self.OnShowLegend, ("OnShowLegend"))
        Publisher.subscribe(self.OnNumBins, ("OnNumBins"))
        Publisher.subscribe(self.OnRemovePlot, ("removePlot"))
        Publisher.subscribe(self.OnChangeSelection, ("changePlotSelection"))
        Publisher.subscribe(self.OnChangeSelectionDT, ("changePlotSelectionDT"))
        Publisher.subscribe(self.onUpdateValues, ("updateValues"))


        self.selectedSerieslist = []
        self._seriesPlotInfo= None
        self.editID = None


    def onUpdateValues(self, event):
        self.pltTS.updateValues()


    def OnChangeSelection(self, sellist):
      self.pltTS.changeSelection(sellist)

    def OnChangeSelectionDT(self, sellist):
      self.pltTS.changeSelectionDT(sellist)

    def OnRemovePlot(self, seriesID):

      # self.selectedSerieslist.remove(seriesID)
      self._seriesPlotInfo.Update(seriesID, False)
      self.pltTS.Plot(self._seriesPlotInfo)
      self.pltSum.Plot(self._seriesPlotInfo)
      self.pltBox.Plot(self._seriesPlotInfo)
      self.pltHist.Plot(self._seriesPlotInfo)
      self.pltProb.Plot(self._seriesPlotInfo)

    def OnNumBins(self , numBins):
      self.pltHist.ChangeNumOfBins(numBins)

    def onDateChanged(self, startDate, endDate):
      self.pltTS.onDateChanged(startDate, endDate)

    def OnPlotType(self, event, ptype):
      self.pltTS.OnPlotType(ptype)
      self.pltProb.OnPlotType(ptype)


    def OnShowLegend(self, event, isVisible):
      self.pltTS.OnShowLegend(isVisible)
      self.pltProb.OnShowLegend(isVisible)

    def stopEdit(self):
        self._seriesPlotInfo.StopEditSeries()
        self.editID = None
        self.pltTS.stopEdit()

    def addEditPlot(self, dataRep, seriesID, record_service):
        self.record_service = record_service
        if not self._seriesPlotInfo:
            options = PlotOptions("Both", 0, False, False, True)
            self._seriesPlotInfo= SeriesPlotInfo(dataRep, options )
        self.editID= seriesID
        self._seriesPlotInfo.SetEditSeries(self.editID)
        self.pltTS.setEdit(self.editID)

    def addPlot(self, dataRep, seriesID):

        if not self._seriesPlotInfo:
            options = PlotOptions("Both", 0, False, False, True)
            self._seriesPlotInfo= SeriesPlotInfo(dataRep, options )

        self._seriesPlotInfo.Update(seriesID, True)
        self.selectedSerieslist.append(seriesID)

        self.pltSum.Plot(self._seriesPlotInfo)
        self.pltHist.Plot(self._seriesPlotInfo)
        self.pltProb.Plot(self._seriesPlotInfo)
        self.pltBox.Plot(self._seriesPlotInfo)
        self.pltTS.Plot(self._seriesPlotInfo)

    #     self.PlotGraph()
    def selectPlot(self, value):
        self.SetSelection(value)

    def getActivePlotID(self):
        return self.GetSelection()

    def Close(self):
        self.pltTS.Close()

    def Clear(self):
        self.pltSum.Clear()
        self.pltHist.Clear()
        self.pltProb.Clear()
        self.pltBox.Clear()
        self.pltTS.Clear()
        self._seriesPlotInfo= None
##    def get_edit_metadata(self)




    def __init__(self, parent, id,  size, style, name, pos= None):
        self._init_ctrls(parent)
        self.parent = parent
