import math
import datetime

from pandas import DataFrame
import pandas
import wx

import numpy
from functools import partial



class OneSeriesPlotInfo(object):
    def __init__(self, prnt):
        self.parent = prnt

        self.seriesID = None
        self.series = None
        self.noDataValue= -9999

        self.startDate = None
        self.endDate = None

        self.dataTable = None  # link to sql database
        # self.cursor=None
        self.siteName = ""
        self.variableName = ""
        self.dataType = ""
        self.variableUnits = ""
        self.filteredData=None
        self.BoxWhisker = None
        self.Probability = None
        self.Statistics = None
        self.plotTitle = None
        self.numBins = 25
        self.binWidth = 1.5
        self.boxWhiskerMethod = "Monthly"

        self.yrange=0
        self.color = ""

        #edit functions
        self.edit = False
        #the color the plot should be when not editing
        self.plotcolor = None



class SeriesPlotInfo(object):
    # self._siteDisplayColumn = ""

    def __init__(self, memDB):

        #memDB is a connection to the memory_database
        self.memDB = memDB
        self._seriesInfos = {}
        self.editID = None
        self.colorList = ['blue', 'green',  'cyan', 'orange', 'purple',  'saddlebrown', 'magenta', 'teal','red']
        self.startDate = datetime.datetime(2100, 12, 31)
        self.endDate= datetime.datetime(1800, 01, 01)
        self.currentStart=self.startDate
        self.currentEnd=self.endDate
        self.isSubsetted = False



    def getDates(self):
        return self.startDate, self.endDate, self.currentStart, self.currentEnd

    def setCurrentStart(self, start):
        self.currentStart = start

    def setCurrentEnd(self, end):
        self.currentEnd= end

    def resetDates(self):
        self.startDate = datetime.datetime(2100, 12, 31)
        self.endDate = datetime.datetime(1800, 01, 01)

        #self.isSubsetted = False
        for key in self.getSeriesIDs():
            start = self._seriesInfos[key].startDate
            end = self._seriesInfos[key].endDate

            if start < self.startDate:
                self.startDate = start

            if end > self.endDate:
                self.endDate = end

        if not self.isSubsetted:
            self.currentStart = self.startDate
            self.currentEnd = self.endDate




    def isPlotted(self, sid):
        if int(sid) in self._seriesInfos:
            return True
        else:
            return False

    def getEditSeriesID(self):
        if self.editID:
            return int(self.editID)
        else:
            return None

    def setEditSeries(self, seriesID):

        self.editID = int(seriesID)
        #self.memDB.initEditValues(self.editID)

        if self.editID not in self._seriesInfos:
            self.update(self.editID, True)
           # self.getSeriesInfo(self.editID)
        else:
            self._seriesInfos[self.editID].dataTable = self.memDB.getEditDataValuesforGraph()

        self._seriesInfos[self.editID].edit = True
        self._seriesInfos[self.editID].plotcolor = self._seriesInfos[self.editID].color
        self._seriesInfos[self.editID].color = "Black"


    def updateEditSeries(self):
        if self.editID in self._seriesInfos:
            self._seriesInfos[self.editID].dataTable = self.memDB.getEditDataValuesforGraph()

    def stopEditSeries(self):

        if self.editID in self._seriesInfos:
            self._seriesInfos[self.editID].dataTable = \
                self.memDB.getDataValuesforGraph(self.editID, self._seriesInfos[self.editID].noDataValue,
                                                 self._seriesInfos[self.editID].startDate,
                                                 self._seriesInfos[self.editID].endDate)
            self._seriesInfos[self.editID].edit = False
            self._seriesInfos[self.editID].color = self._seriesInfos[self.editID].plotcolor
        self.editID = None
        self.memDB.stopEdit()

    def getEditSeriesInfo(self):
        if self.editID and (self.editID in self._seriesInfos):
            return self._seriesInfos[self.editID]
        else:
            return None

    def count(self):
        return len(self._seriesInfos)

    def update(self, key, isselected):
        if not isselected:
            try:
                self.colorList.append(self._seriesInfos[key].color)
                del self._seriesInfos[key]
            except KeyError:
                self.resetDates()
        else:
            ## add dictionary entry with no data

            self._seriesInfos[key] = self.getSeriesInfo(key)



    # def Update(self):
    #     for key, value in enumerate(self._seriesInfos):
    #         self._seriesInfos[key]=None

    def setBoxInterval(self, title):

        for key, value in self._seriesInfos.items():
            value.BoxWhisker.setInterval(title)

    def getSeriesIDs(self):
        return self._seriesInfos.keys()

    def getSeries(self, seriesID):
        if int(seriesID) in self._seriesInfos:
            return self._seriesInfos[int(seriesID)]
        else:
            return None

    def getAllSeries(self):
        return self._seriesInfos.values()

    def getSeriesById(self, seriesID):
        try:
            series = self.memDB.series_service.get_series_by_id(seriesID)
            self.memDB.series_service.reset_session()
            return series
        except:
            return None

    def getSelectedSeries(self, seriesID):
        seriesInfo = OneSeriesPlotInfo(self)
        series = self.getSeriesById(seriesID)
        return self.createSeriesInfo(seriesID, seriesInfo, series)

    def createSeriesInfo(self, seriesID, seriesInfo, series):
        startDate = series.begin_date_time
        endDate = series.end_date_time

        if endDate > self.endDate:
            self.endDate = endDate
        if startDate < self.startDate:
            self.startDate = startDate

        if not self.isSubsetted:
            self.currentStart = self.startDate
            self.currentEnd = self.endDate

        variableName = series.variable_name
        unitsName = series.variable_units_name
        siteName = series.site_name
        dataType = series.data_type
        noDataValue = series.variable.no_data_value
        if self.editID == seriesID:
            #d= DataFrame(pandas.read_sql())
            data = DataFrame(self.memDB.getEditDataValuesforGraph())

        else:
            # using current variable keeps the series subsetted
            data = DataFrame(self.memDB.getDataValuesforGraph(seriesID, noDataValue, self.currentStart, self.currentEnd))
        data.columns = self.memDB.columns
        seriesInfo.seriesID = seriesID
        seriesInfo.series = series

        seriesInfo.startDate = startDate
        seriesInfo.endDate = endDate
        seriesInfo.dataType = dataType
        seriesInfo.siteName = siteName
        seriesInfo.variableName = variableName
        seriesInfo.variableUnits = unitsName
        seriesInfo.plotTitle = "Site: " + siteName + "\nVarName: " + variableName + "\nQCL: " + series.quality_control_level_code
        seriesInfo.axisTitle = variableName + " (" + unitsName + ")"
        seriesInfo.noDataValue = noDataValue
        seriesInfo.dataTable = data
        #remove all of the nodatavalues from the pandas table
        seriesInfo.filteredData= data[data["DataValue"]!=noDataValue]


        if len(data)>0:
            seriesInfo.yrange = data['DataValue'].max() - data['DataValue'].min()
        else:
            seriesInfo.yrange=0

        return seriesInfo

    def getSeriesInfo(self, seriesID):
        assert seriesID is not None

        #if seriesInfo is None:

        oneSeriesInfo = OneSeriesPlotInfo(self)
        series = self.getSeriesById(seriesID)

        #add dictionary entry
        #self._seriesInfos[key] = seriesInfo
        #print "series date: ", type(series.begin_date_time)
        if not series:
            message = "Please check your database connection. Unable to retrieve series %d from the database" % seriesID
            wx.MessageBox(message, 'ODMTool Python', wx.OK | wx.ICON_EXCLAMATION)
            return

        seriesInfo = self.createSeriesInfo(seriesID, oneSeriesInfo, series)


        #Tests to see if any values were returned for the given daterange
        self.build(seriesInfo)

        i = len(self._seriesInfos)
        if self.editID == seriesInfo.seriesID:
            #set color to black for editing
            seriesInfo.edit = True
            seriesInfo.plotcolor = self.colorList.pop(0)
            seriesInfo.color = "Black"
        else:
            seriesInfo.color = self.colorList.pop(0)
        #lst.append(seriesInfo)
        #return lst
        return seriesInfo

    import threading
    class ThreadHandler(threading.Thread):
        def __init__(self, type=""):
            pass

        def run(self):
            pass

    def build(self, seriesInfo):

        seriesInfo.Probability = Probability(seriesInfo.filteredData)
        seriesInfo.Statistics = Statistics(seriesInfo.filteredData)
        seriesInfo.BoxWhisker = BoxWhisker(seriesInfo.filteredData, seriesInfo.boxWhiskerMethod)


    def updateDateRange(self, startDate=None, endDate=None):
        self.currentStart = startDate
        self.currentEnd=endDate
        for key in self.getSeriesIDs():
            seriesInfo = self._seriesInfos[key]
            if startDate:
                data = self.memDB.getDataValuesforGraph(key, seriesInfo.noDataValue, startDate, endDate)
                self.isSubsetted=True
                self.currentStart = startDate
                self.currentEnd=endDate
            else:
                #this returns the series to its full daterange
                data = self.memDB.getDataValuesforGraph(key, seriesInfo.noDataValue, seriesInfo.startDate, seriesInfo.endDate)
                self.isSubsetted = False
                self.currentStart = self.startDate
                self.currentEnd = self.endDate

            seriesInfo.dataTable = data
            #Tests to see if any values were returned for the given daterange
            self.build(seriesInfo)


class Statistics(object):
    def __init__(self, data):


        #dataValues = [x[0] for x in dataTable if x[0] <> noDataValue]
        #data = sorted(dataValues)
        d= data.describe(percentiles = [.10,.25,.5,.75,.90])
        count = self.NumberofObservations = d["DataValue"]["count"]
        self.NumberofCensoredObservations = data[data["CensorCode"]!= "nc"].count().DataValue
        self.ArithemticMean = round(d["DataValue"]["mean"], 5)


        sumval = 0
        sign = 1
        for dv in data["DataValue"]:
            if dv == 0:
                sumval = sumval + numpy.log2(1)
            else:
                if dv < 0:
                    sign = sign * -1
                sumval = sumval + numpy.log2(numpy.absolute(dv))

        if count > 0:
            self.GeometricMean = round(sign * (2 ** float(sumval / float(count))), 5)
            self.Maximum = round(d["DataValue"]["max"], 5)
            self.Minimum = round(d["DataValue"]["min"], 5)
            self.StandardDeviation = round(d["DataValue"]["std"], 5)
            self.CoefficientofVariation = round(data.var().DataValue, 5)

            ##Percentiles
            self.Percentile10 = round(d["DataValue"]["10%"], 5)
            self.Percentile25 = round(d["DataValue"]["25%"], 5)
            self.Percentile50 = round(d["DataValue"]["50%"], 5)
            self.Percentile75 = round(d["DataValue"]["75%"], 5)
            self.Percentile90 = round(d["DataValue"]["90%"], 5)


class BoxWhisker(object):
    def __init__(self, data, method):

        self.intervals = {}
        self.method = method
        mean = []
        median=[]
        confint=[]
        conflimit=[]
        values=[]
        names =[]
        from scipy import stats

        # for x in dataTable:
        #     print x, x[3]

        mean.append(data.mean())
        median.append(data.median())
        ci = stats.norm.interval(.95, data.mean(), scale = 10*(data.std()/math.sqrt(len(data))))
        confint.append((ci[0][0], ci[1][0]))
        cl= stats.norm.interval(.95, data.median(), scale = (data.std()/math.sqrt(len(data))))
        conflimit.append((cl[0][0], cl[1][0]))



        self.intervals["Overall"] = BoxWhiskerPlotInfo("Overall", None, [''], [median, conflimit, mean, confint])

        mean = []
        median=[]
        confint=[]
        conflimit=[]
        values=[]
        y=data.groupby("DateYear")

        for name, group in y:
            names.append(name)
            mean.append(group.mean())
            median.append(group.median())
            ci = stats.norm.interval(.95, data.mean(), scale = 10*(data.std()/math.sqrt(len(data))))
            confint.append((ci[0][0], ci[1][0]))
            cl= stats.norm.interval(.95, data.median(), scale = (data.std()/math.sqrt(len(data))))
            conflimit.append((cl[0][0], cl[1][0]))

        # return medians, conflimit, means, confint
        self.intervals["Yearly"] = BoxWhiskerPlotInfo("Yearly", "DateYear", names,[ median, conflimit, mean, confint])




        mean = []
        names=[]
        median=[]
        confint=[]
        conflimit=[]
        values=[]
        m=data.groupby("DateMonth")

        for name, group in m:
            names.append(name)
            mean.append(group.mean())
            median.append(group.median())
            ci = stats.norm.interval(.95, group.mean(), scale = 10*(group.std()/math.sqrt(len(group))))
            confint.append((ci[0][0], ci[1][0]))
            cl= stats.norm.interval(.95, group.median(), scale = (group.std()/math.sqrt(len(group))))
            conflimit.append((cl[0][0], cl[1][0]))


        self.intervals["Monthly"] = BoxWhiskerPlotInfo("Monthly", "DateMonth" , names,
                                                       [median, conflimit, mean, confint])


        '''

        ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        data = [[x[0] for x in dataTable if x[1].month in (1, 2, 3) if x[0] <> noDataValue],
                [x[0] for x in dataTable if x[1].month in (4, 5, 6) if x[0] <> noDataValue],
                [x[0] for x in dataTable if x[1].month in (7, 8, 9) if x[0] <> noDataValue],
                [x[0] for x in dataTable if x[1].month in (10, 11, 12) if x[0] <> noDataValue]]
        self.intervals["Seasonally"] = BoxWhiskerPlotInfo("Seasonally", data, ['Winter', 'Spring', 'Summer', 'Fall'],
                                                          self.calcConfInterval(data))
        '''
        self.currinterval = self.intervals[self.method]


    def setInterval(self, title):
        self.method = title
        self.currinterval = self.intervals[self.method]






class BoxWhiskerPlotInfo(object):
    def __init__(self, title, groupby ,  xLabels, dets):
        self.title = title

        self.xlabels = xLabels
        self.groupby = groupby

        self.medians = dets[0]
        self.confint = dets[1]
        self.means = dets[2]
        self.conflimit = dets[3]


class Probability(object):
    def __init__(self, data):

        self.curFreq = None
        self.Xaxis = []
        #self.Yaxis = sorted(data)
        length = len(data)

        probX = lambda freq: round(4.91 * ((freq ** .14) - (1.00 - freq) ** .14), 3)
        probFreq = lambda rank: round((rank - .0375) / (length + 1 - (2 * 0.375)), 3)

        self.yAxis = data['DataValue'].apply(probFreq)
        self.xAxis = self.yAxis.apply(probX)

        '''
        for it in range(length):
            #curValue = datavalues[it]
            curFreq = self.calcualteProbabilityFreq(it + 1, length)
            curX = self.calculateProbabilityXPosition(curFreq)
            #self.Yaxis.append(curValue)
            self.Xaxis.append(curX)
        '''

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



















