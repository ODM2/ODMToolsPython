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
from odmtools.controller.logicPlotOptions import SeriesPlotInfo

import logging
from odmtools.common.logger import LoggerTool

tool = LoggerTool()
logger = tool.setupLogger(__name__, __name__ + '.log', 'w', logging.DEBUG)

[wxID_PANEL1, wxID_PAGEBOX, wxID_PAGEHIST, wxID_PAGEPROB,
 wxID_PAGESUMMARY, wxID_PAGETIMESERIES, wxID_TABPLOTS
] = [wx.NewId() for _init_ctrls in range(7)]


class pnlPlot(fnb.FlatNotebook):
    def __init__(self, parent, taskserver):
        self.taskserver = taskserver
        self._init_ctrls(parent)
        self.initPubSub()
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


        self._seriesPlotInfo = None
        self.editID = None
        self.legendVisible = False

    def initPubSub(self):
        Publisher.subscribe(self.onDateChanged, "onDateChanged")
        Publisher.subscribe(self.onDateFull, "onDateFull")
        Publisher.subscribe(self.onPlotType, "onPlotType")
        Publisher.subscribe(self.onShowLegend, "onShowLegend")
        Publisher.subscribe(self.onNumBins, "onNumBins")
        Publisher.subscribe(self.onRemovePlot, "removePlot")
        Publisher.subscribe(self.onChangeSelection, "changePlotSelection")
        Publisher.subscribe(self.onUpdateValues, "updateValues")
        Publisher.subscribe(self.clear, "clearPlot")

    def onUpdateValues(self, event):
        self.pltTS.updateValues()

    def onChangeSelection(self, datetime_list):
        self.pltTS.changePlotSelection( datetime_list)

    def onNumBins(self, numBins):
        self.pltHist.changeNumOfBins(numBins)

    def onDateChanged(self, startDate, endDate):
        self._seriesPlotInfo.updateDateRange(startDate, endDate)
        self.redrawPlots()

    def onDateFull(self):
        self._seriesPlotInfo.updateDateRange()
        self.redrawPlots()

    # Reset the date to the full date
    def onPlotType(self, event, ptype):
        self.pltTS.onPlotType(ptype)
        self.pltProb.onPlotType(ptype)

    def onShowLegend(self, event, isVisible):
        try:
            self.pltTS.onShowLegend(isVisible)
            self.pltProb.onShowLegend(isVisible)
            self.legendVisible = isVisible
        except AttributeError:
            pass

    def stopEdit(self):
        self._seriesPlotInfo.stopEditSeries()
        self.editID = None
        self.pltTS.stopEdit()
        self.redrawPlots()

    def addEditPlot(self, memDB, seriesID, record_service):
        self.record_service = record_service

        if not self._seriesPlotInfo:
            self._seriesPlotInfo = SeriesPlotInfo(memDB, self.taskserver)


        self.editID = seriesID
        self._seriesPlotInfo.setEditSeries(self.editID)
        self.pltTS.setEdit(self.editID)
        self.redrawPlots()

    def addPlot(self, memDB, seriesID):

        """
        Creates the plot
        """
        logger.debug("Adding plot")

        Publisher.sendMessage("EnablePlotButton", plot=self.getActivePlotID(), isActive=True)

        if not self._seriesPlotInfo:
            self._seriesPlotInfo = SeriesPlotInfo(memDB, self.taskserver)

        self._seriesPlotInfo.update(seriesID, True)

        logger.debug("Redrawing plots")
        self.redrawPlots()

    def onRemovePlot(self, seriesID):
        self._seriesPlotInfo.update(seriesID, False)
        self.redrawPlots()

    def redrawPlots(self):

        logger.debug("Plot Summary")
        self.pltSum.Plot(self._seriesPlotInfo)

        logger.debug("Plot Probability")
        self.pltProb.Plot(self._seriesPlotInfo)

        logger.debug("Plot Boxwhisker")
        self.pltBox.Plot(self._seriesPlotInfo)

        logger.debug("Plot Histogram")
        self.pltHist.Plot(self._seriesPlotInfo)

        logger.debug("Plot Timeseries")
        self.pltTS.Plot(self._seriesPlotInfo)

        self.onShowLegend(event=None, isVisible=self.legendVisible)
        maxStart, maxEnd, currStart, currEnd = self._seriesPlotInfo.getDates()
        Publisher.sendMessage("resetdate", startDate=maxStart, endDate=maxEnd, currStart=currStart, currEnd=currEnd)


    def selectPlot(self, value):
        self.SetSelection(value)

    def getActivePlotID(self):
        return self.GetSelection()

    def close(self):
        self.pltTS.close()

    def clear(self):
        """

        :return:
        """
        if self._seriesPlotInfo:
            for seriesID in self._seriesPlotInfo.getSeriesIDs():
                self._seriesPlotInfo.update(seriesID, False)
            self.redrawPlots()

