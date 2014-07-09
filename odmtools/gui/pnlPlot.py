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
from clsPlotOptions import SeriesPlotInfo

import logging
from odmtools.common.logger import LoggerTool

tool = LoggerTool()
logger = tool.setupLogger(__name__, __name__ + '.log', 'w', logging.DEBUG)

[wxID_PANEL1, wxID_PAGEBOX, wxID_PAGEHIST, wxID_PAGEPROB,
 wxID_PAGESUMMARY, wxID_PAGETIMESERIES, wxID_TABPLOTS
] = [wx.NewId() for _init_ctrls in range(7)]


class pnlPlot(fnb.FlatNotebook):
    def __init__(self, parent, id, size, style, name, pos=None):
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

        self.selectedSerieslist = []
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
        Publisher.subscribe(self.onChangeSelection, "changeSelection")
        Publisher.subscribe(self.onUpdateValues, "updateValues")
        Publisher.subscribe(self.clear, "clearPlot")

    def onUpdateValues(self, event):
        self.pltTS.updateValues()

    def onChangeSelection(self, sellist, datetime_list):
        self.pltTS.changePlotSelection(sellist, datetime_list)

    def onRemovePlot(self, seriesID):

        # self.selectedSerieslist.remove(seriesID)
        #tempseries= self._seriesPlotInfo.getSeries(seriesID)
        self._seriesPlotInfo.update(seriesID, False)
        self.redrawPlots()
        #self.clear()

    def onNumBins(self, numBins):
        self.pltHist.changeNumOfBins(numBins)

    def onDateChanged(self, startDate, endDate):
        self._seriesPlotInfo.updateDateRange(startDate, endDate)
        self.redrawPlots()
        # self.pltTS.onDateChanged(startDate, endDate)


        #   def onDateChanged(self, startDate, endDate):
        #       self.pltTS.onDateChanged(startDate, endDate)

    # Reset the date to the full date
    def onDateFull(self):
        self._seriesPlotInfo.updateDateRange()
        self.redrawPlots()

    def onPlotType(self, event, ptype):
        self.pltTS.onPlotType(ptype)
        self.pltProb.onPlotType(ptype)

    def onShowLegend(self, event, isVisible):
        self.pltTS.onShowLegend(isVisible)
        self.pltProb.onShowLegend(isVisible)
        self.legendVisible = isVisible

    def stopEdit(self):
        self._seriesPlotInfo.stopEditSeries()
        self.editID = None
        self.pltTS.stopEdit()
        self.redrawPlots()


    def addEditPlot(self, memDB, seriesID, record_service):
        self.record_service = record_service
        if not self._seriesPlotInfo:
            self._seriesPlotInfo = SeriesPlotInfo(memDB)

        self.editID = seriesID
        self._seriesPlotInfo.setEditSeries(self.editID)
        self.pltTS.setEdit(self.editID)
        self.redrawPlots()

    def addPlot(self, memDB, seriesID):

        import resource

        if not self._seriesPlotInfo:
            self._seriesPlotInfo = SeriesPlotInfo(memDB)

        self._seriesPlotInfo.update(seriesID, True)

        ## 2014-07-09 10:46:45,569 - DEBUG - gui.pnlPlot.addPlot() (156): Memory usage: 161288 (kb)
        self.selectedSerieslist.append(seriesID)
        




        ## 2014-07-09 10:46:51,253 - DEBUG - gui.pnlPlot.addPlot() (160): Memory usage: 182816 (kb)
        self.redrawPlots()


    def redrawPlots(self):
        import resource
        from odmtools.common.timer import Timer
        logger.debug("Memory usage: %s (kb)" % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss )
        with Timer() as t:
            self.pltSum.Plot(self._seriesPlotInfo)
        logger.info("self.pltSum took %s sec" % t.interval)

        logger.debug("Memory usage: %s (kb)" % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss )
        with Timer() as t:
            self.pltProb.Plot(self._seriesPlotInfo)
        logger.info("self.pltSum took %.03f sec" % t.interval)
        
        logger.debug("Memory usage: %s (kb)" % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss )
        with Timer() as t:
            self.pltBox.Plot(self._seriesPlotInfo)
        logger.info("self.pltBox took %.03f sec" % t.interval)    
        
        logger.debug("Memory usage: %s (kb)" % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss )
        with Timer() as t:
            self.pltHist.Plot(self._seriesPlotInfo)
        logger.info("self.pltHist took %.03f sec" % t.interval)    
        
        logger.debug("Memory usage: %s (kb)" % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss )
        with Timer() as t:
            self.pltTS.Plot(self._seriesPlotInfo)
        logger.info("self.pltTs took %.03f sec" % t.interval)    
        
        logger.debug("Memory usage: %s (kb)" % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss )
        self.onShowLegend(event=None, isVisible=self.legendVisible)
        
        logger.debug("Memory usage: %s (kb)" % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss )
        maxStart, maxEnd, currStart, currEnd = self._seriesPlotInfo.getDates()
        
        logger.debug("Memory usage: %s (kb)" % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss )
        Publisher.sendMessage("resetdate", startDate=maxStart, endDate=maxEnd, currStart= currStart, currEnd=currEnd)
        logger.debug("Memory usage: %s (kb)" % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss )
        logger.debug("\n")

        '''
        2014-07-09 10:53:04,628 - DEBUG - gui.pnlPlot.redrawPlots() (166): Memory usage: 111720 (kb)
        2014-07-09 10:53:07,827 - DEBUG - gui.pnlPlot.redrawPlots() (168): Memory usage: 129832 (kb)
        2014-07-09 10:53:08,041 - DEBUG - gui.pnlPlot.redrawPlots() (170): Memory usage: 131416 (kb)
        2014-07-09 10:53:08,399 - DEBUG - gui.pnlPlot.redrawPlots() (172): Memory usage: 133104 (kb)
        2014-07-09 10:53:08,704 - DEBUG - gui.pnlPlot.redrawPlots() (174): Memory usage: 134800 (kb)
        2014-07-09 10:53:08,947 - DEBUG - gui.pnlPlot.redrawPlots() (176): Memory usage: 138368 (kb)
        2014-07-09 10:53:09,188 - DEBUG - gui.pnlPlot.redrawPlots() (178): Memory usage: 138368 (kb)
        2014-07-09 10:53:09,189 - DEBUG - gui.pnlPlot.redrawPlots() (180): Memory usage: 138368 (kb)
        2014-07-09 10:53:09,190 - DEBUG - gui.pnlPlot.redrawPlots() (182): Memory usage: 138368 (kb)
        2014-07-09 10:53:09,191 - DEBUG - gui.pnlPlot.redrawPlots() (183): 

        2014-07-09 10:53:09,305 - DEBUG - gui.pnlPlot.redrawPlots() (166): Memory usage: 138368 (kb)
        2014-07-09 10:53:10,207 - DEBUG - gui.pnlPlot.redrawPlots() (168): Memory usage: 138368 (kb)
        2014-07-09 10:53:10,413 - DEBUG - gui.pnlPlot.redrawPlots() (170): Memory usage: 138368 (kb)
        2014-07-09 10:53:10,767 - DEBUG - gui.pnlPlot.redrawPlots() (172): Memory usage: 138588 (kb)
        2014-07-09 10:53:11,061 - DEBUG - gui.pnlPlot.redrawPlots() (174): Memory usage: 139016 (kb)
        2014-07-09 10:53:11,344 - DEBUG - gui.pnlPlot.redrawPlots() (176): Memory usage: 140140 (kb)
        2014-07-09 10:53:11,571 - DEBUG - gui.pnlPlot.redrawPlots() (178): Memory usage: 140188 (kb)
        2014-07-09 10:53:11,572 - DEBUG - gui.pnlPlot.redrawPlots() (180): Memory usage: 140188 (kb)
        2014-07-09 10:53:11,573 - DEBUG - gui.pnlPlot.redrawPlots() (182): Memory usage: 140188 (kb)
        2014-07-09 10:53:11,574 - DEBUG - gui.pnlPlot.redrawPlots() (183): 
        '''

    #     self.PlotGraph()
    def selectPlot(self, value):
        #select the corresponding page of the notebook
        self.SetSelection(value)

    def getActivePlotID(self):
        return self.GetSelection()

    def close(self):
        self.pltTS.close()

    def clear(self):
        #self.pltTS.init_plot()
        if self.pltSum:
            self.pltSum.clear()

        if self.pltHist:
            self.pltHist.clear()
            #self.pltHist.close()

        if self.pltProb:
            self.pltProb.clear()
            #self.pltProb.close()

        if self.pltBox:
            self.pltBox.clear()
            #self.pltBox.close()

        if self.pltTS:
            self.pltTS.clear()
            self.pltTS.close()

            # Set title of TimeSeries to default
            self.pltTS.timeSeries.set_title("No Data To Plot")

        self._seriesPlotInfo = None