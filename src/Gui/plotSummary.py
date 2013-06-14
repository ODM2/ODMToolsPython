#Boa:FramePanel:plotSummary

import wx
import wx.grid
import numpy
import math

[wxID_PLOTSUMMARY, wxID_PLOTSUMMARYGRDSUMMARY, 
] = [wx.NewId() for _init_ctrls in range(2)]

class plotSummary(wx.Panel):
    def _init_coll_boxSizer1_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.grdSummary, 100, border=0, flag=wx.GROW)

    def _init_sizers(self):
        # generated method, don't edit
        self.boxSizer1 = wx.BoxSizer(orient=wx.VERTICAL)

        self._init_coll_boxSizer1_Items(self.boxSizer1)

        self.SetSizer(self.boxSizer1)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PLOTSUMMARY, name=u'plotSummary',
              parent=prnt, pos=wx.Point(747, 267), size=wx.Size(437, 477),
              style=wx.TAB_TRAVERSAL)
        self.SetClientSize(wx.Size(421, 439))

        self.grdSummary = wx.grid.Grid(id=wxID_PLOTSUMMARYGRDSUMMARY,
              name=u'grdSummary', parent=self, pos=wx.Point(0, 0),
              size=wx.Size(421, 439), style=wx.HSCROLL | wx.VSCROLL)
        self.grdSummary.SetLabel(u'')
        self.grdSummary.EnableEditing(False)
        self.initPlot()
        self._init_sizers()

    def Plot(self, seriesPlotInfo):
        self.Clear()
        for oneSeries in seriesPlotInfo.GetSeriesInfo():
            self.addCol( oneSeries)
            


    def Clear(self):        
        if self.grdSummary.GetNumberCols()>0:
        # for col in range(self.grdSummary.GetNumberCols())
            self.grdSummary.DeleteCols(pos = 0, numCols = self.grdSummary.GetNumberCols(),  updateLabels = True)

    # def addPlot(self, cursor, series, Filter):

    #     # series=Values[1]

    #     self.grdSummary.AppendCols(numCols = 1, updateLabels = True)
    #     count = self.grdSummary.GetNumberCols()
    #     self.grdSummary.SetColLabelValue(count-1, series.site_name +"-"+ series.variable_name)
    #     self.fillValues(cursor, series, Filter, count-1)
        
    # def removePlot(self, id):
    #     #loop through each column and find position
    #     # self.grdSummary.
    #     self.grdSummary.DeleteCols(pos = 0, numCols = 1,  updateLabels = True)
        
    def initPlot(self):
        self.grdSummary.AutoSize()    
        self.grdSummary.CreateGrid (15,0) 
        self.grdSummary.SetRowLabelSize(160)
        self.grdSummary.SetRowLabelValue(0, "Series ID")
        self.grdSummary.SetRowLabelValue(1, "# of Observations")
        self.grdSummary.SetRowLabelValue(2, "# of censored Obs.")
        self.grdSummary.SetRowLabelValue(3, "Arithmetic Mean")
        self.grdSummary.SetRowLabelValue(4, "Geometric Mean")
        self.grdSummary.SetRowLabelValue(5, "Maximum")
        self.grdSummary.SetRowLabelValue(6, "Minimum")
        self.grdSummary.SetRowLabelValue(7, "Standard Deviation")
        self.grdSummary.SetRowLabelValue(8, "Coefficiant of Variation")
        self.grdSummary.SetRowLabelValue(9, "Percentiles:")
        self.grdSummary.SetRowLabelValue(10, "10%")
        self.grdSummary.SetRowLabelValue(11, "25%")
        self.grdSummary.SetRowLabelValue(12, "(Median) 50%")
        self.grdSummary.SetRowLabelValue(13, "75%")
        self.grdSummary.SetRowLabelValue(14, "90%")
        
    def addCol(self, series) :

        self.grdSummary.AppendCols(numCols = 1, updateLabels = True)
        col = self.grdSummary.GetNumberCols()-1
        self.grdSummary.SetColLabelValue(col, series.siteName +"-"+ series.variableName)
    #     self.fillValues(cursor, series, Filter, count-1)


        stats = series.statistics
        count = stats.NumberofObservations 
        self.grdSummary.SetCellValue(0, col, repr(series.seriesID)) 
        self.grdSummary.SetCellValue(1, col, repr(count))        
        self.grdSummary.SetCellValue(2, col, repr(stats.NumberofCensoredObservations))
        self.grdSummary.SetCellValue(3, col, repr(stats.ArithemticMean))  


        if count > 0:
            self.grdSummary.SetCellValue(4, col,  repr(stats.GeometricMean))
            self.grdSummary.SetCellValue(5, col, repr(stats.Maximum))  
            self.grdSummary.SetCellValue(6, col, repr(stats.Minimum)) 
            self.grdSummary.SetCellValue(7, col, repr(stats.StandardDeviation))  
            self.grdSummary.SetCellValue(8, col, repr(stats.CoefficientofVariation))


            ##Percentiles
            self.grdSummary.SetCellValue(10, col, repr(stats.Percentile10))  
            self.grdSummary.SetCellValue(11, col, repr(stats.Percentile25))
            self.grdSummary.SetCellValue(12, col, repr(stats.Percentile50))   

            self.grdSummary.SetCellValue(13, col, repr(stats.Percentile75))        
            self.grdSummary.SetCellValue(14, col, repr(stats.Percentile90))











    # def fillValues(self, cursor, series, Filter, col):
    #     #SetCellValue(int row, int col, const wxString& s)  

    #     # self.cursor = Values[0] 
    #     self.cursor = cursor       


    #     self.cursor.execute("SELECT DataValue FROM DataValues"+Filter)
    #     dataValues =[x[0] for x in self.cursor.fetchall()]

    #     self.cursor.execute("SELECT Count(ValueID) FROM DataValues WHERE CensorCode <> 'nc'")
    #     val= self.cursor.fetchone()[0]
    #     print(val)
    #     data= sorted(dataValues)
    #     count=len(data)

    #     self.grdSummary.SetCellValue(0, col, repr(series.id))  
    #     self.grdSummary.SetCellValue(1, col, repr(count))        
    #     self.grdSummary.SetCellValue(2, col, repr(val))
    #     self.grdSummary.SetCellValue(3, col, repr(round(numpy.mean(data),5)))  

       
    #     sumval = 0 
    #     sign = 1 
    #     for dv in data:
    #         if dv == 0:
    #             sumval = sumval+ numpy.log2(1)
    #         else:
    #             if dv < 0:
    #                 sign = sign * -1
    #             sumval = sumval+ numpy.log2(numpy.absolute(dv))    

    #     if count > 0:
    #         self.grdSummary.SetCellValue(4, col,  repr(round(sign * (2 ** float(sumval / float(count))),5)))
    #         self.grdSummary.SetCellValue(5, col, repr(round(max(data),5)))  
    #         self.grdSummary.SetCellValue(6, col, repr(round(min(data),5))) 
    #         self.grdSummary.SetCellValue(7, col, repr(round(numpy.std(data),5)))  
    #         self.grdSummary.SetCellValue(8, col, repr(round(numpy.var(data),5)))


    #         ##Percentiles
    #         self.grdSummary.SetCellValue(10, col, repr(round(data[int(math.floor(count/10))],5)))  
    #         self.grdSummary.SetCellValue(11, col, repr(round(data[int(math.floor(count/4))],5)))

                 
    #         if count % 2 == 0 :
    #             self.grdSummary.SetCellValue(12, col, repr(round((data[int(math.floor((count/2)-1))]+ data[int(count/2)])/2,5)))  
    #         else:
    #             self.grdSummary.SetCellValue(12, col, repr(round(data[int(numpy.ceil(count/2))],5)))    

    #         self.grdSummary.SetCellValue(13, col, repr(round(data[int(math.floor(count/4*3))],5)))        
    #         self.grdSummary.SetCellValue(14, col, repr(round(data[int(math.floor(count/10*9))],5)))

        

    def __init__(self, parent, id, pos, size, style, name):
        self._init_ctrls(parent)
