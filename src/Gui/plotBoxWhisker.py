import textwrap

import wx
from wx.lib.pubsub import pub as Publisher
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas
import matplotlib.pyplot as plt

from mnuPlotToolbar import MyCustomToolbar as NavigationToolbar


class PlotBox(wx.Panel):
    def _init_coll_boxSizer1_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        parent.AddWindow(self.toolbar, 0, wx.EXPAND)


    def _init_sizers(self):
        # generated method, don't edit
        self.boxSizer1 = wx.BoxSizer(orient=wx.VERTICAL)
        self._init_coll_boxSizer1_Items(self.boxSizer1)
        self.SetSizer(self.boxSizer1)


    def _init_ctrls(self, prnt):
        #matplotlib.figure.Figure.__init__(self)
        wx.Panel.__init__(self, prnt, -1)

        Publisher.subscribe(self.monthly, ("box.Monthly"))
        Publisher.subscribe(self.yearly, ("box.Yearly"))
        Publisher.subscribe(self.seasonaly, ("box.Seasonal"))
        Publisher.subscribe(self.overall, ("box.Overall"))

        self.figure = matplotlib.figure.Figure()
        self.plot = self.figure.add_subplot(111)
        self.plot.axis([0, 1, 0, 1])  #
        self.plot.set_title("No Data To Plot")

        self.canvas = FigCanvas(self, -1, self.figure)
        # Create the navigation toolbar, tied to the canvas
        self.toolbar = NavigationToolbar(self.canvas, True)
        self.toolbar.Realize()


        #self.canvas.SetCursor(wx.StockCursor(wx.CURSOR_CROSS))
        #self.canvas.SetScrollbar(wx.HORIZONTAL, 0,5, 1000)
        self.setColor("WHITE")
        self.canvas.SetFont(wx.Font(20, wx.SWISS, wx.NORMAL, wx.NORMAL,
                                    False, u'Tahoma'))
        self.canvas.draw()
        self._init_sizers()

    def clear(self):
        self.figure.clear()

    def gridSize(self, cells):
        rows = 1
        cols = 1
        while rows * cols < cells:
            if rows == cols:
                cols = cols + 1
            else:
                rows = rows + 1
        return rows, cols

    def textSize(self, cells):
        wrap = 50
        wrap = wrap - (cells * 3)
        text = 20 - cells
        return wrap, text

    def Plot(self, seriesPlotInfo):
        self.seriesPlotInfo = seriesPlotInfo
        self.updatePlot()

    def updatePlot(self):
        self.clear()
        count = self.seriesPlotInfo.count()
        rows, cols = self.gridSize(count)
        self.plots = []
        i = 1
        for oneSeries in self.seriesPlotInfo.getSeriesInfo():
            self.plots.append(self.figure.add_subplot(repr(rows) + repr(cols) + repr(i)))

            wrap, text = self.textSize(count)
            self.plots[i - 1].set_xlabel("\n".join(textwrap.wrap(oneSeries.BoxWhisker.currinterval.title, wrap)))
            self.plots[i - 1].set_ylabel(
                "\n".join(textwrap.wrap(oneSeries.variableName + " (" + oneSeries.variableUnits + ")", wrap)))
            self.plots[i - 1].set_title(
                "\n".join(textwrap.wrap(oneSeries.siteName + " " + oneSeries.variableName, wrap)))

            self.canvas.SetFont(wx.Font(text, wx.SWISS, wx.NORMAL, wx.NORMAL,
                                        False, u'Tahoma'))

            med = oneSeries.BoxWhisker.currinterval.medians
            cl = oneSeries.BoxWhisker.currinterval.confint
            mean = oneSeries.BoxWhisker.currinterval.means
            ci = oneSeries.BoxWhisker.currinterval.conflimit
            bp = self.plots[i - 1].boxplot(oneSeries.BoxWhisker.currinterval.data, sym="-s", notch=True,
                                           bootstrap=5000, conf_intervals=cl)


            # Plot Mean and its confidence interval
            for x in range(len(mean)):
                self.plots[i - 1].vlines(x + 1, ci[x][0], ci[x][1], color='r', linestyle="solid")
            self.plots[i - 1].scatter([range(1, len(mean) + 1)], mean, marker='o', c='r', s=10)


            # Plot Median
            self.plots[i - 1].scatter([range(1, len(med) + 1)], med, marker='s', c="k", s=10)


            # Set Colors of the Box Whisker plot
            plt.setp(bp['whiskers'], color='k', linestyle='-')
            plt.setp(bp['medians'], color='k', linestyle='-')
            plt.setp(bp['boxes'], color='GREY', linestyle='-')
            plt.setp(bp['caps'], color='k')
            plt.setp(bp['fliers'], markersize=3.5, color=oneSeries.color)

            # self.plot.set_ybound(min(data),max(data))
            self.plots[i - 1].set_autoscale_on(True)
            self.plots[i - 1].set_xticklabels(oneSeries.BoxWhisker.currinterval.xlabels)

            i += 1

            left  = 0.125  # the left side of the subplots of the figure
            right = 0.9    # the right side of the subplots of the figure
            bottom = 0.21   # the bottom of the subplots of the figure
            top = .9      # the top of the subplots of the figure
            wspace = 0.8   # the amount of width reserved for blank space between subplots
            hspace = 0.8   # the amount of height reserved for white space between subplots
            self.figure.subplots_adjust(
                left=left, bottom=bottom, right=right, top=top, wspace=wspace, hspace=hspace
            )

        #self.figure.autofmt_xdate()

        #plt.xticks(rotation=30, size='small')
        #plt.margins(0.2)
        # Tweak spacing to prevent clipping of tick-labels
        #plt.subplots_adjust(bottom=0.55)

        self.canvas.draw()


    def setColor(self, color):
        # """Set figure and canvas colours to be the same."""
        self.figure.set_facecolor(color)
        self.figure.set_edgecolor(color)
        self.canvas.SetBackgroundColour(color)


    def monthly(self, str):
        # print "monthly"
        self.seriesPlotInfo.setBoxInterval("Monthly")
        self.updatePlot()

    def seasonaly(self, str):
        # print"seasonal"
        self.seriesPlotInfo.setBoxInterval("Seasonally")
        self.updatePlot()

    def yearly(self, str):
        # print "yearly"
        self.seriesPlotInfo.setBoxInterval("Yearly")
        self.updatePlot()

    def overall(self, str):
        # print "overall"
        self.seriesPlotInfo.setBoxInterval("Overall")
        self.updatePlot()


    def __init__(self, parent, id, pos, size, style, name):
        self._init_ctrls(parent)