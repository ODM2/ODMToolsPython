import textwrap

import wx
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas
from matplotlib.font_manager import FontProperties

from mnuPlotToolbar import MyCustomToolbar as NavigationToolbar


class plotProb(wx.Panel):
    def _init_coll_boxSizer1_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        parent.AddWindow(self.toolbar, 0, wx.EXPAND)


    def _init_sizers(self):
        # generated method, don't edit
        self.boxSizer1 = wx.BoxSizer(orient=wx.VERTICAL)
        self._init_coll_boxSizer1_Items(self.boxSizer1)
        self.SetSizer(self.boxSizer1)


    def clear(self):
        self.plots.clear()

    def close(self):
        #self.plot.clf()
        self.plots.close('all')

    def _init_ctrls(self, prnt):
        #matplotlib.figure.Figure.__init__(self)
        wx.Panel.__init__(self, prnt, -1)

        self.figure = Figure()
        self.plots = self.figure.add_subplot(111)
        self.plots.axis([0, 1, 0, 1])  #
        self.plots.plot([], [])
        self.plots.set_title("No Data To Plot")
        self.islegendvisible = False


        self.canvas = FigCanvas(self, -1, self.figure)
        # Create the navigation toolbar, tied to the canvas
        self.toolbar = NavigationToolbar(self.canvas)
        self.toolbar.Realize()

        left = 0.125  # the left side of the subplots of the figure
        right = 0.9  # the right side of the subplots of the figure
        bottom = 0.51  # the bottom of the subplots of the figure
        top = 1.2  # the top of the subplots of the figure
        wspace = .8  # the amount of width reserved for blank space between subplots
        hspace = .8  # the amount of height reserved for white space between subplots
        self.figure.subplots_adjust(
            left=left, bottom=bottom, right=right, top=top, wspace=wspace, hspace=hspace
        )
        self.figure.tight_layout()


        #self.canvas.SetCursor(wx.StockCursor(wx.CURSOR_CROSS))
        #self.canvas.SetScrollbar(wx.HORIZONTAL, 0,5, 1000)
        self.setColor("WHITE")
        self.canvas.SetFont(wx.Font(20, wx.SWISS, wx.NORMAL, wx.NORMAL,
                                    False, u'Tahoma'))

        self.fontP = FontProperties()
        self.fontP.set_size('small')

        self.canvas.draw()

        self._init_sizers()


    def onPlotType(self, ptype):
        # self.timeSeries.clear()
        if ptype == "line":
            ls = '-'
            m = 'None'
        elif ptype == "point":
            ls = 'None'
            m = 's'
        else:
            ls = '-'
            m = 's'
        # print plt.setp(self.lines)
        # print(len(self.lines))
        self.format = ls + m
        for line in self.prob:
            plt.setp(line, linestyle=ls, marker=m)
        if self.islegendvisible:
            self.onShowLegend(self.islegendvisible)
        self.canvas.draw()

    def onShowLegend(self, isVisible):
        self.islegendvisible = isVisible
        if isVisible:
            leg = self.plots.legend(loc='best', ncol=2, fancybox=True, prop=self.fontP)
            leg.get_frame().set_alpha(.5)
            leg.draggable(state=True)

        else:
            self.plots.legend_ = None
        self.canvas.draw()


    def Plot(self, seriesPlotInfo):
        self.seriesPlotInfo = seriesPlotInfo
        self.updatePlot()


    def updatePlot(self):
        self.clear()
        count = self.seriesPlotInfo.count()
        self.prob = []
        self.plots = self.figure.add_subplot(111)
        for oneSeries in self.seriesPlotInfo.getAllSeries():

            self.plots.set_xlabel("Cumulative Frequency < Stated Value %")
            if count > 1:
                self.plots.set_ylabel("\n".join(textwrap.wrap(oneSeries.axisTitle, 50)))
                self.plots.set_title("")

            else:
                self.plots.set_ylabel("\n".join(textwrap.wrap(oneSeries.axisTitle, 50)))
                self.plots.set_title("\n".join(textwrap.wrap(oneSeries.siteName, 55)))

            if len(oneSeries.dataTable) >0:
                self.prob.append(
                    self.plots.plot(oneSeries.Probability.Xaxis, oneSeries.Probability.Yaxis, 'bs', color=oneSeries.color,
                                   label=oneSeries.plotTitle))

        self.setXaxis()

        '''if count > 1:
            plt.subplots_adjust(bottom=.1 + .1)
            self.plot.legend(loc='upper center', ncol=2, prop=self.fontP)
        else:
            plt.subplots_adjust(bottom=.1)
            self.plot.legend_ = None'''

        left = 0.125  # the left side of the subplots of the figure
        right = 0.9  # the right side of the subplots of the figure
        bottom = 0.51  # the bottom of the subplots of the figure
        top = 1.2  # the top of the subplots of the figure
        wspace = .8  # the amount of width reserved for blank space between subplots
        hspace = .8  # the amount of height reserved for white space between subplots
        self.figure.subplots_adjust(
            left=left, bottom=bottom, right=right, top=top, wspace=wspace, hspace=hspace
        )

        if len(self.prob)>0:
            self.figure.tight_layout()

        self.canvas.draw()


    def addPlot(self, cursor, series, Filter):
        # self.cursor = Values[0]
        self.cursor = cursor

        self.cursor.execute("SELECT DataValue FROM DataValues" + Filter)
        self.dataValues = [x[0] for x in self.cursor.fetchall()]
        self.Series = series
        self.plots.clear()
        length = len(self.dataValues)
        self.Yaxis = sorted(self.dataValues)
        self.Xaxis = []
        for it in range(0, length):
            curFreq = self.calcualteProbabilityFreq(it + 1, length)
            curX = self.calculateProbabilityXPosition(curFreq)
            self.Xaxis.append(curX)

        self.plots.clear()
        x = range(len(self.Xaxis))
        self.plots.set_xlabel("Cumulative Frequency < Stated Value %")
        self.plots.set_ylabel(
            "\n".join(textwrap.wrap(self.Series.variable_name + " (" + self.Series.variable_units_name + ")", 50)))
        self.plots.set_title("\n".join(textwrap.wrap(self.Series.site_name + " " + self.Series.variable_name, 55)))

        self.plots = self.figure.add_subplot(111)
        self.prob = self.plots.plot(self.Xaxis, self.Yaxis, 'bs')

        #self.figure.autofmt_xdate()
        self.setXaxis()
        self.canvas.draw()

    def setXaxis(self):

        self.plots.set_xticklabels(
            ["0.01", "0.02", "0.02", "1", "2", "5", "10", "20", "30", "40", "50", "60", "70", "80", "90", "95", "98",
             "99", "99.9", "99.98", "99.99"])
        self.plots.set_xticks(
            [-3.892, -3.5, -3.095, -2.323, -2.055, -1.645, -1.282, -0.842, -0.542, -0.254, 0, 0.254, 0.542, 0.842,
             1.282, 1.645, 2.055, 2.323, 3.095, 3.5, 3.892])
        self.plots.set_xbound(-4, 4)


    def setColor(self, color):
        """Set figure and canvas colours to be the same."""
        self.figure.set_facecolor(color)
        self.figure.set_edgecolor(color)
        self.canvas.SetBackgroundColour(color)

    def calculateProbabilityXPosition(self, freq):
        try:
            return round(4.91 * ((freq ** .14) - (1.00 - freq) ** .14), 3)
        except:
            print "An error occurred while calculating the X-Position for a point in the prob plot"
            pass

    def calcualteProbabilityFreq(self, rank, numRows):
        try:
            return round((rank - .0375) / (numRows + 1 - (2 * 0.375)), 3)
        except:
            print "An error occured while calculating the frequency for a point in the prob plot"
            pass


    def __init__(self, parent, id, pos, size, style, name):
        self._init_ctrls(parent)


