import math
import datetime

import numpy



#class PlotOptions(object):

    # def __init__(self, TSMethod, showLegend, useCensoredData):
    #
    #
    #     self.timeSeriesMethod = TSMethod
    #     self.showLegend = showLegend
    #     self.useCensoredData = useCensoredData
    #
    #     self.numBins = 25
    #     self.binWidth = 1.5
    #
    #     # self.timeSeriesMethod ="Both"
    #     self.boxWhiskerMethod = "Monthly"
    #
    #     self.displayFullDate = True



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
        self.BoxWhisker = None
        self.Probability = None
        self.Statistics = None
        self.plotTitle = None
        self.numBins = 25
        self.binWidth = 1.5
        self.boxWhiskerMethod = "Monthly"
        self.useCensoredData = False
        self.yrange=0

        self.color = ""

        #edit functions
        self.edit = False
        #the color the plot should be when not editing
        self.plotcolor = None
        self.timeRadius= None



class SeriesPlotInfo(object):
    # self._siteDisplayColumn = ""

    def __init__(self, memDB):

        #memDB is a connection to the memory_database
        self.memDB = memDB
        self._seriesInfos = {}
        self.editID = None
        self.colorList = ['blue', 'green',  'cyan', 'orange', 'purple',  'yellow', 'magenta', 'teal','red']
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
            data = self.memDB.getEditDataValuesforGraph()
        else:
            # using current variable keeps the series subsetted
            data = self.memDB.getDataValuesforGraph(seriesID, noDataValue, self.currentStart, self.currentEnd)
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
        seriesInfo.timeRadius = self.setTimeRadius(series)
        yvals = [y[0] for y in data]
        if len(data)>0:
            seriesInfo.yrange = max(yvals) - min(yvals)
        else:
            seriesInfo.yrange=0

        return seriesInfo

    def getSeriesInfo(self, seriesID):
        assert seriesID is not None
        #lst = []  #of length len(seriesInfos)

        #for key in self.getSeriesIDs():

        #if the current series is not already in the list
        #seriesInfo = self._seriesInfos[key

        #if seriesInfo is None:
        # if key in self._seriesInfos.keys():
        # if not self._seriesInfos[key] == None:
        oneSeriesInfo = OneSeriesPlotInfo(self)
        series = self.getSeriesById(seriesID)
        #add dictionary entry
        #self._seriesInfos[key] = seriesInfo
        #print "series date: ", type(series.begin_date_time)

        seriesInfo = self.createSeriesInfo(seriesID, oneSeriesInfo, series)
        #Tests to see if any values were returned for the given daterange
        #if data is not None:
        self.build(seriesInfo)

        # else:
        #     seriesInfo = self._seriesInfos[key]
        #     #print "seriesInfo.startDate ", seriesInfo.startDate
        #     #print "seriesInfo.endDate ", seriesInfo.endDate

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

    def build(self, seriesInfo):
        data = seriesInfo.dataTable
        seriesInfo.Probability = Probability(data, seriesInfo.noDataValue)
        seriesInfo.Statistics = Statistics(data, seriesInfo.useCensoredData, seriesInfo.noDataValue)
        seriesInfo.BoxWhisker = BoxWhisker(data, seriesInfo.boxWhiskerMethod, seriesInfo.noDataValue)

    def setTimeRadius(self, series):
        ts = series.time_support
        if ts ==0:  ts = 1

        if series.time_units_name == 'second':
            return ts/2
        elif series.time_units_name == 'minute':
            return ts/2 *60 #convert minutes to seconds
        elif series.time_units_name == 'hour':
            return ts/2 *120 #120 converts hours to seconds
        else:
            return 43200 #12 hours in seconds


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
    def __init__(self, dataTable, useCensoredData, noDataValue):
        useCensoredData=True
        #TODO do we plot censored datavalues
        if useCensoredData:
            dataValues = [x[0] for x in dataTable if x[0] <> noDataValue]
        else:
            dataValues = [x[0] for x in dataTable if x[2] == 'nc' if x[0] <> noDataValue]
        data = sorted(dataValues)
        count = self.NumberofObservations = len(data)
        self.NumberofCensoredObservations = count-len([x[0] for x in dataTable if x[2] == 'nc'])  #self.cursor.fetchone()[0]
        self.ArithemticMean = round(numpy.mean(data), 5)

        sumval = 0
        sign = 1
        for dv in data:
            if dv == 0:
                sumval = sumval + numpy.log2(1)
            else:
                if dv < 0:
                    sign = sign * -1
                sumval = sumval + numpy.log2(numpy.absolute(dv))

        if count > 0:
            self.GeometricMean = round(sign * (2 ** float(sumval / float(count))), 5)
            self.Maximum = round(max(data), 5)
            self.Minimum = round(min(data), 5)
            self.StandardDeviation = round(numpy.std(data), 5)
            self.CoefficientofVariation = round(numpy.var(data), 5)


            ##Percentiles
            self.Percentile10 = round(data[int(math.floor(count / 10))], 5)
            self.Percentile25 = round(data[int(math.floor(count / 4))], 5)

            if count % 2 == 0:
                self.Percentile50 = round((data[int(math.floor((count / 2) - 1))] + data[int(count / 2)]) / 2, 5)
            else:
                self.Percentile50 = round(data[int(numpy.ceil(count / 2))], 5)

            self.Percentile75 = round(data[int(math.floor(count / 4 * 3))], 5)
            self.Percentile90 = round(data[int(math.floor(count / 10 * 9))], 5)


class BoxWhisker(object):
    def __init__(self, dataTable, method, noDataValue):

        self.intervals = {}
        self.method = method

        # for x in dataTable:
        #     print x, x[3]


        data = [x[0] for x in dataTable if x[0] <> noDataValue]
        self.intervals["Overall"] = BoxWhiskerPlotInfo("Overall", data, [''], self.calcConfInterval([data,]))

        years = sorted(list(set([x[4] for x in dataTable])))
        data = []
        for y in years:
            data.append([x[0] for x in dataTable if x[4] == y if x[0] <> noDataValue])
        self.intervals["Yearly"] = BoxWhiskerPlotInfo("Yearly", data, years, self.calcConfInterval(data))

        data = [[x[0] for x in dataTable if x[1].month in (1, 2, 3) if x[0] <> noDataValue],
                [x[0] for x in dataTable if x[1].month in (4, 5, 6) if x[0] <> noDataValue],
                [x[0] for x in dataTable if x[1].month in (7, 8, 9) if x[0] <> noDataValue],
                [x[0] for x in dataTable if x[1].month in (10, 11, 12) if x[0] <> noDataValue]]
        self.intervals["Seasonally"] = BoxWhiskerPlotInfo("Seasonally", data, ['Winter', 'Spring', 'Summer', 'Fall'],
                                                          self.calcConfInterval(data))

        data = [[x[0] for x in dataTable if x[1].month == 1 if x[0] <> noDataValue],
                [x[0] for x in dataTable if x[1].month == 2 if x[0] <> noDataValue],
                [x[0] for x in dataTable if x[1].month == 3 if x[0] <> noDataValue],
                [x[0] for x in dataTable if x[1].month == 4 if x[0] <> noDataValue],
                [x[0] for x in dataTable if x[1].month == 5 if x[0] <> noDataValue],
                [x[0] for x in dataTable if x[1].month == 6 if x[0] <> noDataValue],
                [x[0] for x in dataTable if x[1].month == 7 if x[0] <> noDataValue],
                [x[0] for x in dataTable if x[1].month == 8 if x[0] <> noDataValue],
                [x[0] for x in dataTable if x[1].month == 9 if x[0] <> noDataValue],
                [x[0] for x in dataTable if x[1].month == 10 if x[0] <> noDataValue],
                [x[0] for x in dataTable if x[1].month == 11 if x[0] <> noDataValue],
                [x[0] for x in dataTable if x[1].month == 12 if x[0] <> noDataValue]]
        self.intervals["Monthly"] = BoxWhiskerPlotInfo("Monthly", data,
                                                       ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sep',
                                                        'Oct', 'Nov', 'Dec'], self.calcConfInterval(data))
        self.currinterval = self.intervals[self.method]


    def setInterval(self, title):
        self.method = title
        self.currinterval = self.intervals[self.method]

    def calcConfInterval(self, PlotData):
        medians = []
        confint = []
        conflimit = []
        means = []
        '''if len(PlotData) > 12:
            vals = self.indivConfInter(PlotData)
            medians.append(vals[0])
            means.append(vals[1])
            conflimit.append((vals[4], vals[5]))
            confint.append((vals[2], vals[3]))
            # print vals

        else:'''
        for data in PlotData:
            vals = self.indivConfInter(data)
            medians.append(vals[0])
            means.append(vals[1])
            conflimit.append((vals[4], vals[5]))
            confint.append((vals[2], vals[3]))
            # print vals

        return medians, conflimit, means, confint


    def indivConfInter(self, data):
        if type(data) is float:
            med = numpy.median(data)
            mean = numpy.mean(data)
            stdDev = math.sqrt(numpy.var(data))
            ci95low = mean - 10 * (1.96 * (stdDev / math.sqrt(1)))
            ci95up = mean + 10 * (1.96 * (stdDev / math.sqrt(1)))

            cl95low = med - (1.96 * (stdDev / math.sqrt(1)))
            cl95up = med + (1.96 * (stdDev / math.sqrt(1)))

            return [med, mean, ci95low, ci95up, cl95low, cl95up]
        elif len(data) > 0:
            med = numpy.median(data)
            mean = numpy.mean(data)
            stdDev = math.sqrt(numpy.var(data))
            ci95low = mean - 10 * (1.96 * (stdDev / math.sqrt(len(data))))
            ci95up = mean + 10 * (1.96 * (stdDev / math.sqrt(len(data))))

            cl95low = med - (1.96 * (stdDev / math.sqrt(len(data))))
            cl95up = med + (1.96 * (stdDev / math.sqrt(len(data))))

            return [med, mean, ci95low, ci95up, cl95low, cl95up]
        else:
            return [None, None, None, None, None, None]


class BoxWhiskerPlotInfo(object):
    def __init__(self, title, data,  xLabels, dets):
        self.title = title
        self.data = data
        self.xlabels = xLabels

        self.medians = dets[0]
        self.confint = dets[1]
        self.means = dets[2]
        self.conflimit = dets[3]


class Probability(object):
    def __init__(self, dataTable, noDataValue):
        dataValues = [x[0] for x in dataTable if x[0] <> noDataValue]
        self.curFreq = None
        self.Xaxis = []
        self.Yaxis = sorted(dataValues)
        length = len(dataValues)

        for it in range(length):
            #curValue = datavalues[it]
            curFreq = self.calcualteProbabilityFreq(it + 1, length)
            curX = self.calculateProbabilityXPosition(curFreq)
            #self.Yaxis.append(curValue)
            self.Xaxis.append(curX)

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



















