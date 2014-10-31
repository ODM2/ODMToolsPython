import textwrap

import wx
import matplotlib
import matplotlib.pyplot as plt
from wx.lib.pubsub import pub as Publisher
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas

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
        # matplotlib.figure.Figure.__init__(self)
        wx.Panel.__init__(self, prnt, -1)

        Publisher.subscribe(self.monthly, ("box.Monthly"))
        Publisher.subscribe(self.yearly, ("box.Yearly"))
        Publisher.subscribe(self.seasonaly, ("box.Seasonal"))
        Publisher.subscribe(self.overall, ("box.Overall"))

        self.figure = matplotlib.figure.Figure()
        #self.figure = plt.figure()

        self.plot = self.figure.add_subplot(111)
        #self.plot.axis([0, 1, 0, 1])  #
        self.plot.set_title("No Data To Plot")

        import pandas as pd
        import numpy as np
        self.data = pd.DataFrame(np.random.randn(10,2), columns=['first', 'sec'])
        #plt = self.data.plot(kind='box', ax=self.plot, title='sample' )
        pl = self.data.boxplot( ax=self.plot )



        self.canvas = FigCanvas(self, -1, self.figure)
        # Create the navigation toolbar, tied to the canvas
        self.toolbar = NavigationToolbar(self.canvas, True)
        self.toolbar.Realize()
        self.figure.tight_layout()


        #self.canvas.SetCursor(wx.StockCursor(wx.CURSOR_CROSS))
        #self.canvas.SetScrollbar(wx.HORIZONTAL, 0,5, 1000)
        self.setColor("WHITE")
        self.canvas.SetFont(wx.Font(15, wx.SWISS, wx.NORMAL, wx.NORMAL, False, u'Tahoma'))
        self.canvas.draw()
        self._init_sizers()

    def clear(self):
        self.figure.clear()

    def close(self):
        plt.clf()
        plt.close('all')

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
        wrap = 40
        wrap = wrap - (cells * 3)
        text = 20 - cells
        return wrap, text

    def Plot(self, seriesPlotInfo):
        self.seriesPlotInfo = seriesPlotInfo
        self.updatePlot()

    def updatePlot(self):
        self.clear()

        rows, cols = self.gridSize(self.seriesPlotInfo.count())
       # self.figure, self.axes = plt.subplots(nrows=rows, ncols=cols)
        i = 1


        for oneSeries in self.seriesPlotInfo.getAllSeries():
            if len(oneSeries.dataTable) > 0:
                self._createPlot(oneSeries, rows, cols, i)
                i += 1

        left = 0.125  # the left side of the subplots of the figure
        right = 0.9  # the right side of the subplots of the figure
        bottom = 0.51  # the bottom of the subplots of the figure
        top = 1.2  # the top of the subplots of the figure
        wspace = .8  # the amount of width reserved for blank space between subplots
        hspace = .8  # the amount of height reserved for white space between subplots
        self.figure.subplots_adjust(left=left, bottom=bottom, right=right, top=top, wspace=wspace, hspace=hspace)

        self.figure.tight_layout()

        self.canvas.draw()

    def _createPlot(self, oneSeries, rows, cols, index):


        count = self.seriesPlotInfo.count()
        ax = self.figure.add_subplot(repr(rows) + repr(cols) + repr(index))

        med = oneSeries.BoxWhisker.currinterval.medians
        ci = oneSeries.BoxWhisker.currinterval.confint
        mean = oneSeries.BoxWhisker.currinterval.means
        cl = oneSeries.BoxWhisker.currinterval.conflimit

        wrap, text = self.textSize(count)
        self.canvas.SetFont(wx.Font(text, wx.SWISS, wx.NORMAL, wx.NORMAL, False, u'Tahoma'))

        ax.set_xlabel("\n".join(textwrap.wrap(oneSeries.BoxWhisker.currinterval.title, wrap)))


        ax.set_ylabel(
            "\n".join(textwrap.wrap(oneSeries.variableName + "\n (" + oneSeries.variableUnits + ")", wrap)))
        ax.set_title("\n".join(textwrap.wrap(oneSeries.siteName, wrap)))

        # Plot Means confidence level
        for x in range(len(mean)):
            ax.vlines(x + 1, cl[x][0], cl[x][1], color='r', linestyle="solid")
        #Plot Mean
        ax.scatter([range(1, len(mean) + 1)], mean, marker='o', c='r', s=10)


        # Plot Median
        ax.scatter([range(1, len(med) + 1)], med, marker='s', c="k", s=10)


        bp = oneSeries.BoxWhisker.data.boxplot(column = "DataValue", ax = ax, by = oneSeries.BoxWhisker.currinterval.groupby,
                                                rot = 35, return_type = 'dict', notch=True, sym="-s", conf_intervals=ci)

        # Set Colors of the Box Whisker plot
        '''
        plt.setp(bp['whiskers'], color='k', linestyle='-')
        plt.setp(bp['medians'], color='k', linestyle='-')
        plt.setp(bp['boxes'], color='GREY', linestyle='-')
        plt.setp(bp['caps'], color='k')
        plt.setp(bp['fliers'], markersize=3.5, color=oneSeries.color)
        '''




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