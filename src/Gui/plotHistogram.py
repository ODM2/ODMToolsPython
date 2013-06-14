
import wx
import numpy
import math
from wx.lib.pubsub import pub as Publisher

import matplotlib
import matplotlib.pyplot as plt
import textwrap
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas
from matplotlib.widgets import Lasso
from mnuPlotToolbar import MyCustomToolbar as NavigationToolbar



class plotHist(wx.Panel):


  def _init_coll_boxSizer1_Items(self, parent):
      # generated method, don't edit

      parent.AddWindow(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
      parent.AddWindow(self.toolbar, 0,  wx.EXPAND)


  def _init_sizers(self):
      # generated method, don't edit
      self.boxSizer1 = wx.BoxSizer(orient=wx.VERTICAL)
      self._init_coll_boxSizer1_Items(self.boxSizer1)
      self.SetSizer(self.boxSizer1)



  def _init_ctrls(self, prnt):
      #matplotlib.figure.Figure.__init__(self)
      wx.Panel.__init__(self, prnt, -1)

      self.figure = matplotlib.figure.Figure()
      self.plot=self.figure.add_subplot(111)

      self.plot.set_title("No Data To Plot")

      self.canvas = FigCanvas(self, -1, self.figure)
      
      # Create the navigation toolbar, tied to the canvas
      self.toolbar = NavigationToolbar(self.canvas, True)
      self.toolbar.Realize()


      self.SetColor("WHITE")
      self.canvas.SetFont(wx.Font(20, wx.SWISS, wx.NORMAL, wx.NORMAL,
            False, u'Tahoma'))


      self.canvas.draw()
      self._init_sizers()
      self.hist=[]
      self.bins=50



  def ChangeNumOfBins(self, bins):
      self.bins = bins
      self.updatePlot()


  def Clear(self):
      self.figure.clear()
      self.hist=[]

  def GridSize(self, cells):
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
      wrap = wrap-(cells*3)
      text= 20 -cells
      return wrap, text

  def Plot(self, seriesPlotInfo):
      self.seriesPlotInfo= seriesPlotInfo
      self.updatePlot()

  def updatePlot(self):
      self.Clear()
      count = self.seriesPlotInfo.count()
      rows, cols = self.GridSize(count)
      self.plots=[]
      i=1
      for oneSeries in self.seriesPlotInfo.GetSeriesInfo():
        self.plots.append(self.figure.add_subplot(repr(rows)+repr(cols)+repr(i)))

        wrap, text = self.textSize(count)
        self.plots[i-1].set_xlabel("\n".join(textwrap.wrap(oneSeries.variableName,wrap)))
        self.plots[i-1].set_ylabel("Number of Observations")

        self.canvas.SetFont(wx.Font(text, wx.SWISS, wx.NORMAL, wx.NORMAL,
            False, u'Tahoma'))

        self.plots[i-1].set_title("\n".join(textwrap.wrap(oneSeries.siteName+" "+oneSeries.variableName,wrap)))


        self.hist.append(self.plots[i-1].hist([x[0] for x in oneSeries.dataTable], bins=self.bins, normed=False, facecolor='g', alpha=0.75, label = oneSeries.siteName+" "+oneSeries.variableName))
        i=i+1

      self.canvas.draw()


  def SetColor( self, color):
      """Set figure and canvas colours to be the same."""
      self.figure.set_facecolor( color )
      self.figure.set_edgecolor( color )
      self.canvas.SetBackgroundColour( color )







  def __init__(self, parent, id, pos, size, style, name):
      self._init_ctrls(parent)