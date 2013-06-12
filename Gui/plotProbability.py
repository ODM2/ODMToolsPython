
import wx

from wx.lib.pubsub import pub as Publisher

import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas
from matplotlib.widgets import Lasso
from mnuPlotToolbar import MyCustomToolbar as NavigationToolbar
import matplotlib.pyplot as plt
import mpl_toolkits.axisartist as AA
from matplotlib.font_manager import FontProperties
import textwrap


class plotProb(wx.Panel):
   
   
  def _init_coll_boxSizer1_Items(self, parent):
      # generated method, don't edit

      parent.AddWindow(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
      parent.AddWindow(self.toolbar, 0,  wx.EXPAND)
       

  def _init_sizers(self):
      # generated method, don't edit
      self.boxSizer1 = wx.BoxSizer(orient=wx.VERTICAL)
      self._init_coll_boxSizer1_Items(self.boxSizer1)
      self.SetSizer(self.boxSizer1)
   
   
  def Clear(self):
    self.plot.clear()

  def _init_ctrls(self, prnt):
      #matplotlib.figure.Figure.__init__(self)
      wx.Panel.__init__(self, prnt, -1)
      
      self.figure = matplotlib.figure.Figure()
      self.plot=self.figure.add_subplot(111)
      self.plot.axis([0, 1, 0, 1])#
      self.plot.plot([],[])
      self.plot.set_title("No Data To Plot")
            
      self.canvas = FigCanvas(self, -1, self.figure)
      # Create the navigation toolbar, tied to the canvas
      self.toolbar = NavigationToolbar(self.canvas)
      self.toolbar.Realize()
       
       
      #self.canvas.SetCursor(wx.StockCursor(wx.CURSOR_CROSS))        
      #self.canvas.SetScrollbar(wx.HORIZONTAL, 0,5, 1000)
      self.SetColor("WHITE")
      self.canvas.SetFont(wx.Font(20, wx.SWISS, wx.NORMAL, wx.NORMAL,
            False, u'Tahoma'))

      self.fontP = FontProperties()
      self.fontP.set_size('small')
      
       
      self.canvas.draw()
       
      self._init_sizers()

   
  def OnPlotType(self, ptype):
    # self.timeSeries.clear()
    if ptype == "line":
      ls = '-'
      m='None'
    elif ptype == "point":
      ls='None'
      m='s'      
    else:
      ls = '-'
      m='s'
    # print plt.setp(self.lines)
    # print(len(self.lines))
    format = ls+m
    for line in self.lines:
      plt.setp(line, linestyle = ls, marker =  m)

    self.canvas.draw()

  def OnShowLegend(self, isVisible):
    # print self.timeSeries.show_legend
    if isVisible:
      plt.subplots_adjust(bottom=.1+.1)
      self.plot.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
               ncol=2, prop = self.fontP)

    else:
      plt.subplots_adjust(bottom=.1)
      self.plot.legend_=None
    # self.timeSeries.plot(legend= not isVisible)
    self.canvas.draw()


  def Plot(self, seriesPlotInfo):
      self.seriesPlotInfo= seriesPlotInfo
      self.updatePlot()


  def updatePlot(self):
      self.Clear() 
      count = self.seriesPlotInfo.count()   
      self.lines=[]
      self.plot=self.figure.add_subplot(111)
      for oneSeries in self.seriesPlotInfo.GetSeriesInfo():

        self.plot.set_xlabel("Cumulative Frequency < Stated Value %")
        if count > 1: 
          self.plot.set_ylabel("\n".join(textwrap.wrap(oneSeries.axisTitle,50)))
          self.plot.set_title("")

        else: 
          self.plot.set_ylabel("\n".join(textwrap.wrap(oneSeries.axisTitle,50)))
          self.plot.set_title("\n".join(textwrap.wrap(oneSeries.plotTitle,55)))            
        
        self.lines.append(self.plot.plot( oneSeries.Probability.Xaxis, oneSeries.Probability.Yaxis, 'bs', color = oneSeries.color, label = oneSeries.plotTitle))
       
      self.setXaxis()

      if count >1:
        plt.subplots_adjust(bottom=.1+.1)
        self.plot.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
             ncol=2, prop = self.fontP)

      else:
        plt.subplots_adjust(bottom=.1)
        self.plot.legend_=None
      self.canvas.draw()






  def addPlot(self, cursor, series, Filter):

      # self.cursor = Values[0]
      self.cursor=cursor


      self.cursor.execute("SELECT DataValue FROM DataValues"+Filter)
      self.dataValues =[x[0] for x in self.cursor.fetchall()]

     
      # self.Series= Values[1]
      self.Series= series

      self.plot.clear()
     
      length = len(self.dataValues)
      
      self.Yaxis = sorted(self.dataValues)
      self.Xaxis = []
      for it in range (0, length):
          #curValue = datavalues[it]
          curFreq= self.CalcualteProbabilityFreq(it+1, length)
          curX = self.CalculateProbabilityXPosition(curFreq)
          #self.Yaxis.append(curValue)
          self.Xaxis.append(curX)
      
      #print self.Xaxis
     # print self.Yaxis

      
      self.plot.clear()
      x = range(len(self.Xaxis))
      self.plot.set_xlabel("Cumulative Frequency < Stated Value %")
      self.plot.set_ylabel("\n".join(textwrap.wrap(self.Series.variable_name+ "("+self.Series.variable_units_name+")",50)))
      self.plot.set_title("\n".join(textwrap.wrap(self.Series.site_name+" "+self.Series.variable_name,55)))
             
      self.plot=self.figure.add_subplot(111)
      self.lines=self.plot.plot( self.Xaxis, self.Yaxis, 'bs')
       
      self.setXaxis()
      self.canvas.draw()







 
  def setXaxis(self):
          
      self.plot.set_xticklabels(["0.01","0.02", "0.02","1", "2", "5", "10", "20", "30", "40", "50", "60", "70", "80", "90", "95", "98", "99", "99.9", "99.98", "99.99"])
      self.plot.set_xticks([-3.892,-3.5,-3.095,-2.323,-2.055,-1.645,-1.282,-0.842,-0.542,-0.254,0,0.254,0.542,0.842,1.282,1.645,2.055,2.323,3.095,3.5,3.892])
      self.plot.set_xbound(-4,4)
 
   
  def SetColor( self, color):
      """Set figure and canvas colours to be the same."""        
      self.figure.set_facecolor( color )
      self.figure.set_edgecolor( color )
      self.canvas.SetBackgroundColour( color )

  def CalculateProbabilityXPosition(self, freq):
      try:
        return round(4.91*((freq **.14) -(1.00 - freq)**.14), 3)
      except:
        print "An error occurred while calculating the X-Position for a point in the prob plot"
        pass

  def CalcualteProbabilityFreq(self, rank, numRows):     
      try:
        return round((rank - .0375)/(numRows+1-(2*0.375)), 3)
      except:
        print "An error occured while calculating the frequency for a point in the prob plot"
        pass

             
         
       
  def __init__(self, parent, id, pos, size, style, name):
      self._init_ctrls(parent)


class plotData (object):
  def __init__(self, sID, dValues, dTimes,  ylabel, title, color ):
    self.SeriesID= sID
    self.DataValues = dValues
    self.DateTimes=dTimes

    self.startDate= min(dTimes)
    self.endDate=max(dTimes)
    self.ylabel = ylabel
    self.title = title
    self.color = color