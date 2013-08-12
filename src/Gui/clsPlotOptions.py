import numpy
import math



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

class axisData (object):
  def __init__(self, axisid, axis,  position, side="", rightadjust="", leftadjust="", minx="", maxx=""):
    self.axisid= axisid
    self.axis = axis
    self.rightadjust= rightadjust
    self.leftadjust = leftadjust
    self.position = position
    self.side = side
    self.minx= minx
    self.maxx= maxx

  def __repr__(self):
    return "<AxisData(id:'%s', axis:'%s', pos:'%s', side:'%s', radj:'%s', ladj:'%s')>" % (self.axisid, self.axis, self.position, self.side, self.rightadjust, self.leftadjust)

class PlotOptions(object):
    # def enum( **enums):
    #     return type('Enum', (), enums)

    # TimeSeriesType= enum('Both'=3, 'Line'=2, 'Point'=1, 'None'=0)
    # BoxWhiskerType = enum('Monthly'=0, 'Seasonal'= 2, 'Yearly'=3, 'Overall'=4)




    def __init__(self, TSMethod, color, showLegend, useCensoredData, isPlotCensored):
        self.colorList = ['blue', 'green', 'red', 'cyan', 'orange', 'magenta', 'yellow', 'teal', 'purple']

        self.timeSeriesMethod =TSMethod
        self.isPlotCensored = isPlotCensored
        self.plotColor = self.colorList[color]
        self.showLegend = showLegend
        self.useCensoredData = useCensoredData


        self.numBins = 25
        self.binWidth=1.5

        # self.timeSeriesMethod ="Both"
        self.boxWhiskerMethod = "Monthly"


        self.displayFullDate=True
        self._startDateTime=None
        self._endDateTime=None
        self._startDateLimit =None
        self._endDateLimit=None


class OneSeriesPlotInfo(object):


    def __init__ (self, prnt):
        self.parent=prnt

        self.seriesID=None
        self.series = None
        self.dataTable =None# link to sql database
        # self.cursor=None
        self.siteName=""
        self.variableName=""
        self.dataType=""
        self.variableUnits=""
        self.plotOptions=None
        self.BoxWhisker = None
        self.Probability=None
        self.statistics= None
        self.plotTitle=None

        self.color = "Black"

        #edit functions
        self.edit = False
        self.plotcolor = None



    def getPlotOptions(self):
        return self.plot_options

class SeriesPlotInfo(object):
    # self._siteDisplayColumn = ""

    def __init__(self, dbConn,  plotOptions):#siteDisplayColumn,
        # self._siteDisplayColumn = siteDisplayColumn
        self._plotOptions= plotOptions
        self.dbConn= dbConn
        self._seriesInfos = {}
        self.editID= None

    def SetEditSeries(self, seriesID):
        self.editID = int(seriesID)
        if self.editID in self._seriesInfos:
            self._seriesInfos[self.editID].edit = True
            self._seriesInfos[self.editID].plotcolor = self._seriesInfos[self.editID].color
            self._seriesInfos[self.editID].color = "Black"

    def UpdateEditSeries(self):
        if self.editID in self._seriesInfos:
            self._seriesInfos[self.editID].dataTable= self.dbConn.getEditDataValuesforGraph()


    def IsPlotted(self, sid ):
        if int(sid) in self._seriesInfos:
            return True
        else:
            return False

    def GetEditSeriesID(self):
        if self.editID:
            return int(self.editID)
        else: return None

    def StopEditSeries(self):
        if self.editID in self._seriesInfos:
            self._seriesInfos[self.editID].edit = False
            self._seriesInfos[self.editID].color = self._seriesInfos[self.editID].plotcolor
        self.editID = None


    def GetEditSeriesInfo(self):
        if self.editID and (self.editID in self._seriesInfos):
            return self._seriesInfos[self.editID]
        else:
            return None


    def count(self):
        return len(self._seriesInfos)

    def Update(self, e, isselected):
        if not isselected :
            del self._seriesInfos[e]
        else:
        ## add dictionary entry with no data
            self._seriesInfos[e]=None

    # def Update(self):
    #     for key, value in enumerate(self._seriesInfos):
    #         self._seriesInfos[key]=None

    def SetBoxInterval(self, title):
        self._plotOptions.boxWhiskerMethod = title
        for key, value in self._seriesInfos.items():
            value.BoxWhisker.setInterval(title)

    def GetSeriesIDs(self):
        return self._seriesInfos.keys()

    def GetSeries(self, seriesID):
        if seriesID in self._seriesInfos:
            return self._seriesInfos[seriesID]
        else:
            return None

    def GetSeriesInfo(self):

        lst = []#of length len(seriesInfos)

        for key in self.GetSeriesIDs():

            #if the current series is not already in the list
            seriesInfo = self._seriesInfos[key]
            if seriesInfo is None:
            # if key in self._seriesInfos.keys():
            # if not self._seriesInfos[key] == None:
                seriesInfo = OneSeriesPlotInfo(self)
                #add dictionary entry
                self._seriesInfos[key] = seriesInfo


                seriesID = key
                series =  self.dbConn.series_service.get_series_by_id(seriesID)
                strStartDate= series.begin_date_time#self._plotOptions._startDateTime
                strEndDate = series.end_date_time#self._plotOptions._endDateTime#+1 day - 1 millisecond
                variableName = series.variable_name
                unitsName = series.variable_units_name
                siteName = series.site_name
                dataType = series.data_type
                noDataValue = series.variable.no_data_value
                if self.editID == seriesID:
                    data = self.dbConn.getEditDataValuesforGraph()
                else:
                    data = self.dbConn.getDataValuesforGraph(seriesID, repr(noDataValue), strStartDate.strftime('%y-%m-%d %H:%M:%S'), strEndDate.strftime('%y-%m-%d %H:%M:%S'))

                seriesInfo.seriesID = seriesID
                seriesInfo.series = series
                seriesInfo.dataTable = data
                seriesInfo.dataType = dataType
                seriesInfo.siteName =siteName
                seriesInfo.variableName = variableName
                seriesInfo.variableUnits = unitsName
                seriesInfo.plotTitle = siteName+" "+variableName
                seriesInfo.axisTitle = variableName+ "("+unitsName+")"
                seriesInfo.Probability = Probability(data)
                seriesInfo.statistics =  Statistics(data, self._plotOptions.useCensoredData)
                seriesInfo.BoxWhisker = BoxWhisker(data, self._plotOptions.boxWhiskerMethod)
            else:
                seriesinfo = self._seriesInfos[key]

            i = len(lst)
            if self.editID == seriesInfo.seriesID:
                #set color to black for editing
                seriesInfo.edit = True
                seriesInfo.plotcolor = self._plotOptions.colorList[i % len(self._plotOptions.colorList)]
                seriesInfo.color = "Black"
            else:
                seriesInfo.color = self._plotOptions.colorList[i % len(self._plotOptions.colorList)]
            lst.append(seriesInfo)
        return lst

class Statistics(object):

    def __init__(self, dataTable, useCensoredData):

        if useCensoredData:
            dataValues =[x[0] for x in dataTable ]
        else:
            dataValues =[x[0] for x in dataTable if x[2] =='nc']
        data=sorted(dataValues)
        count = self.NumberofObservations = len(data)
        self.NumberofCensoredObservations=  [x[2] for x in dataTable].count('nc') #self.cursor.fetchone()[0]
        self.ArithemticMean=round(numpy.mean(data),5)

        sumval = 0
        sign = 1
        for dv in data:
            if dv == 0:
                sumval = sumval+ numpy.log2(1)
            else:
                if dv < 0:
                    sign = sign * -1
                sumval = sumval+ numpy.log2(numpy.absolute(dv))

        if count > 0:
            self.GeometricMean= round(sign * (2 ** float(sumval / float(count))),5)
            self.Maximum= round(max(data),5)
            self.Minimum= round(min(data), 5)
            self.StandardDeviation= round(numpy.std(data),5)
            self.CoefficientofVariation= round(numpy.var(data),5)


            ##Percentiles
            self.Percentile10=round(data[int(math.floor(count/10))],5)
            self.Percentile25=round(data[int(math.floor(count/4))],5)


            if count % 2 == 0 :
                self.Percentile50= round((data[int(math.floor((count/2)-1))]+ data[int(count/2)])/2,5)
            else:
                self.Percentile50= round(data[int(numpy.ceil(count/2))],5)

            self.Percentile75=round(data[int(math.floor(count/4*3))],5)
            self.Percentile90= round(data[int(math.floor(count/10*9))],5)

class BoxWhisker(object):
    def __init__(self, dataTable, method):

        self.intervals = {}
        self.method = method
        # for x in dataTable:
        #     print x, x[3]


        data = [x[0] for x in dataTable]
        self.intervals["Overall"] = BoxWhiskerPlotInfo("Overall", data, [''], self.calcConfInterval(data))



        years = sorted(list(set([x[4] for x in dataTable] )))
        data = []
        for y in years:
          data.append([x[0] for x in dataTable if x[4]==y])
        self.intervals["Yearly"] = BoxWhiskerPlotInfo("Yearly", data, years, self.calcConfInterval(data))


        data = [[x[0] for x in dataTable if x[1].month in (1,2,3)],
                [x[0] for x in dataTable if x[1].month in (4,5,6)],
                [x[0] for x in dataTable if x[1].month in (6,7,8)],
                [x[0] for x in dataTable if x[1].month in (10,11,12)]]
        self.intervals["Seasonally"] = BoxWhiskerPlotInfo("Seasonally", data, ['Winter', 'Spring', 'Summer', 'Fall'], self.calcConfInterval(data))


        data =[ [x[0] for x in dataTable if x[1].month ==1],
                [x[0] for x in dataTable if x[1].month ==2],
                [x[0] for x in dataTable if x[1].month ==3],
                [x[0] for x in dataTable if x[1].month ==4],
                [x[0] for x in dataTable if x[1].month ==5],
                [x[0] for x in dataTable if x[1].month ==6],
                [x[0] for x in dataTable if x[1].month ==7],
                [x[0] for x in dataTable if x[1].month ==8],
                [x[0] for x in dataTable if x[1].month ==9],
                [x[0] for x in dataTable if x[1].month ==10],
                [x[0] for x in dataTable if x[1].month ==11],
                [x[0] for x in dataTable if x[1].month ==12]]
        self.intervals["Monthly"] = BoxWhiskerPlotInfo("Monthly", data, ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], self.calcConfInterval(data))
        self.currinterval= self.intervals[self.method]


    def setInterval(self, title):
        self.method = title
        self.currinterval= self.intervals[self.method]

    def calcConfInterval(self, PlotData):
      medians = []
      confint = []
      conflimit = []
      means = []
      if len(PlotData)>12 :
        vals = self.indivConfInter(PlotData)
        medians.append(vals[0])
        means.append(vals[1])
        conflimit.append((vals[4], vals[5]))
        confint.append((vals[2], vals[3]))
        # print vals

      else:
        for data in PlotData:
          vals = self.indivConfInter(data)
          medians.append(vals[0])
          means.append(vals[1])
          conflimit.append((vals[4], vals[5]))
          confint.append((vals[2], vals[3]))
          # print vals

      return medians, conflimit, means, confint



    def indivConfInter(self, data):
      if len(data)>0:
        med = numpy.median(data)
        mean = numpy.mean(data)
        stdDev = math.sqrt(numpy.var(data))
        ci95low = mean - 10*(1.96 *(stdDev/math.sqrt(len(data))))
        ci95up = mean + 10*(1.96 *(stdDev/math.sqrt(len(data))))

        cl95low = med - (1.96 *(stdDev/math.sqrt(len(data))))
        cl95up = med + (1.96 *(stdDev/math.sqrt(len(data))))

        return [med, mean, ci95low, ci95up, cl95low, cl95up]
      else: return [ None, None, None, None, None, None]

class  BoxWhiskerPlotInfo(object):
    def __init__( self, title, data, xLabels, dets):
        self.title = title
        self.data = data
        self.xlabels= xLabels

        self.medians = dets[0]
        self.confint= dets[1]
        self.means = dets[2]
        self.conflimit = dets[3]

class Probability(object):
    def __init__(self, dataTable):
        dataValues =[x[0] for x in dataTable]
        self.curFreq = None
        self.Xaxis = []
        self.Yaxis = sorted(dataValues)
        length =len(dataValues)

        for it in range (length):
          #curValue = datavalues[it]
          curFreq= self.CalcualteProbabilityFreq(it+1, length)
          curX = self.CalculateProbabilityXPosition(curFreq)
          #self.Yaxis.append(curValue)
          self.Xaxis.append(curX)

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




















