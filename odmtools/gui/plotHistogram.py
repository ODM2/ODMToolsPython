import textwrap

import wx
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas
from mnuPlotToolbar import MyCustomToolbar as NavigationToolbar

import logging
from odmtools.common.logger import LoggerTool

tool = LoggerTool()
logger = tool.setupLogger(__name__, __name__ + '.log', 'w', logging.DEBUG)

class plotHist(wx.Panel):
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

        self.figure = Figure()

        plot = self.figure.add_subplot(111)
        plot.set_title("No Data To Plot")

        self.canvas = FigCanvas(self, -1, self.figure)
        # Create the navigation toolbar, tied to the canvas
        self.toolbar = NavigationToolbar(self.canvas, True)
        self.toolbar.Realize()
        self.figure.tight_layout()

        self.setColor("WHITE")
        self.canvas.SetFont(wx.Font(20, wx.SWISS, wx.NORMAL, wx.NORMAL,
                                    False, u'Tahoma'))
        self.canvas.draw()
        self._init_sizers()

        self.bins = 50


    def changeNumOfBins(self, bins):
        self.bins = bins
        self.updatePlot()


    def clear(self):
        self.figure.clear()
        # plt.clear()


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
        rows, cols = self.gridSize(self.seriesPlotInfo.count())
        logger.debug("Rows: %s, cols: %s" % (rows,cols))

        i = 1
        for oneSeries in self.seriesPlotInfo.getAllSeries():
            if len(oneSeries.dataTable) > 0:
                self._createPlot(oneSeries, rows, cols, i)
                i += 1

        #self.figure.tight_layout()
        self.canvas.draw()


    def _createPlot(self, oneSeries, rows, cols, index):
        ax = self.figure.add_subplot(repr(rows) + repr(cols) + repr(index))

        logger.debug("HISTOGRAM: %s"% ax)

        # oneSeries.filteredData.hist(ax= ax, color='k', alpha=0.5, bins=50)
        his = oneSeries.dataTable.hist(column="DataValue", ax=ax, bins=self.bins,
                                          facecolor=oneSeries.color,
                                          label=oneSeries.siteName + " " + oneSeries.variableName,
                                          grid=False)

        wrap, text = self.textSize(self.seriesPlotInfo.count())
        ax.set_xlabel("\n".join(textwrap.wrap(oneSeries.variableName, wrap)))
        ax.set_ylabel("Number of Observations")

        self.canvas.SetFont(wx.Font(text, wx.SWISS, wx.NORMAL, wx.NORMAL,
                                    False, u'Tahoma'))
        ax.set_title("\n".join(textwrap.wrap(oneSeries.siteName, wrap)))


    def setColor(self, color):
        """Set figure and canvas colours to be the same."""
        self.figure.set_facecolor(color)
        self.figure.set_edgecolor(color)
        self.canvas.SetBackgroundColour(color)


    def __init__(self, parent, id, pos, size, style, name):
        self._init_ctrls(parent)
