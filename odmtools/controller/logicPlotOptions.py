
import datetime
import math
import wx
import numpy as np
import pandas as pd
from scipy import stats

import logging
from odmtools.common.logger import LoggerTool

import timeit

tool = LoggerTool()
logger = tool.setupLogger(__name__, __name__ + '.log', 'w', logging.DEBUG)


def calcSeason(x):
    x = int(x)
    if x in (1, 2, 3):
        return "1"
    elif x in (4, 5, 6):
        return "2"
    elif x in (7, 8, 9):
        return "3"
    elif x in (10, 11, 12):
        return "4"

        # return x*2, x*3


class OneSeriesPlotInfo(object):
    def __init__(self, prnt):
        self.parent = prnt

        self.seriesID = None
        self.series = None
        self.noDataValue = -9999

        self.startDate = None
        self.endDate = None

        self.dataTable = None  # link to sql database
        # self.cursor=None
        self.siteName = ""
        self.variableName = ""
        self.dataType = ""
        self.variableUnits = ""
        self.filteredData = None
        self.BoxWhisker = None
        self.Probability = None
        self.Statistics = None
        self.plotTitle = None
        self.numBins = 25
        self.binWidth = 1.5
        self.boxWhiskerMethod = "Month"

        self.yrange = 0
        self.color = ""

        # edit functions
        self.edit = False
        #the color the plot should be when not editing
        self.plotcolor = None


class SeriesPlotInfo(object):
    # self._siteDisplayColumn = ""

    def __init__(self, memDB, taskserver):
        logger.debug("Initializing SeriesPlotInfo")

        # memDB is a connection to the memory_database
        self.memDB = memDB
        self.taskserver = taskserver
        self._seriesInfos = {}
        self.editID = None
        self.colorList = ['blue', 'green', 'cyan', 'orange', 'purple', 'saddlebrown', 'magenta', 'teal', 'red']
        self.startDate = datetime.datetime(2100, 12, 31)
        self.endDate = datetime.datetime(1800, 01, 01)
        self.currentStart = self.startDate
        self.currentEnd = self.endDate
        self.isSubsetted = False


    def getDates(self):
        return self.startDate, self.endDate, self.currentStart, self.currentEnd

    def setCurrentStart(self, start):
        self.currentStart = start

    def setCurrentEnd(self, end):
        self.currentEnd = end

    def resetDates(self):
        self.startDate = datetime.datetime(2100, 12, 31)
        self.endDate = datetime.datetime(1800, 01, 01)

        # self.isSubsetted = False
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
        # self.memDB.initEditValues(self.editID)

        if self.editID not in self._seriesInfos:
            self.update(self.editID, True)
            # self.getSeriesInfo(self.editID)
        else:
            ## Pandas DataFrame
            #self._seriesInfos[self.editID].dataTable = self.memDB.getEditDataValuesforGraph()
            data = pd.DataFrame(self.memDB.getEditDataValuesforGraph(), columns=self.memDB.columns)
            data.set_index(data['LocalDateTime'], inplace=True)
            self._seriesInfos[self.editID].dataTable = data

        self._seriesInfos[self.editID].edit = True
        self._seriesInfos[self.editID].plotcolor = self._seriesInfos[self.editID].color
        self._seriesInfos[self.editID].color = "Black"


    def updateEditSeries(self):
        if self.editID in self._seriesInfos:
            # self._seriesInfos[self.editID].dataTable = self.memDB.getEditDataValuesforGraph()
            data = pd.DataFrame(self.memDB.getEditDataValuesforGraph(), columns=self.memDB.columns)
            data.set_index(data['LocalDateTime'], inplace=True)
            self._seriesInfos[self.editID].dataTable = data


    def stopEditSeries(self):
        if self.editID in self._seriesInfos:
            data = pd.DataFrame(self.memDB.getDataValuesforGraph(
                self.editID, self._seriesInfos[self.editID].noDataValue,
                self._seriesInfos[self.editID].startDate,
                self._seriesInfos[self.editID].endDate), columns=self.memDB.columns)
            data.set_index(data['LocalDateTime'], inplace=True)
            self._seriesInfos[self.editID].dataTable = data
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
        logger.debug("Begin generating plots")
        if not isselected:
            try:
                self.colorList.append(self._seriesInfos[key].color)
                del self._seriesInfos[key]
            except KeyError:
                self.resetDates()
        else:
            self._seriesInfos[key] = self.getSeriesInfo(key)
            results = self.taskserver.getCompletedTasks()
            self._seriesInfos[key].Probability = results['Probability']
            self._seriesInfos[key].Statistics = results['Summary']
            self._seriesInfos[key].BoxWhisker = results['BoxWhisker']

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
            logger.debug("editing -- getting datavalues for graph")
            data = self.memDB.getEditDataValuesforGraph()
            logger.debug("Finished editing -- getting datavalues for graph")


        else:
            logger.debug("plotting -- getting datavalues for graph")
            data = self.memDB.getDataValuesforGraph(seriesID, noDataValue, self.currentStart, self.currentEnd)
            logger.debug("Finished plotting -- getting datavalues for graph")

        data.set_index(["LocalDateTime"], inplace=True)
        logger.debug("assigning variables...")
        seriesInfo.seriesID = seriesID
        seriesInfo.series = series
        seriesInfo.columns = self.memDB.columns
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
        seriesInfo.filteredData = data[data["DataValue"] != noDataValue]
        val = seriesInfo.filteredData["Month"].map(calcSeason)
        seriesInfo.filteredData["Season"] = val
        #calcSeason(seriesInfo.filteredData["Month"])


        if len(data) > 0:
            seriesInfo.yrange = data['DataValue'].max() - data['DataValue'].min()
        else:
            seriesInfo.yrange = 0


        logger.debug("Finished creating SeriesInfo")
        return seriesInfo

    def getSeriesInfo(self, seriesID):
        assert seriesID is not None

        logger.debug("Obtain SeriesInfo")
        oneSeriesInfo = OneSeriesPlotInfo(self)

        series = self.getSeriesById(seriesID)

        if not series:
            message = "Please check your database connection. Unable to retrieve series %d from the database" % seriesID
            wx.MessageBox(message, 'ODMTool Python', wx.OK | wx.ICON_EXCLAMATION)
            return

        logger.debug("Create Series Info")
        seriesInfo = self.createSeriesInfo(seriesID, oneSeriesInfo, series)

        # construct tasks for the task server
        tasks = [("Probability", seriesInfo.filteredData),
                 ("BoxWhisker", (seriesInfo.filteredData, seriesInfo.boxWhiskerMethod)),
                 ("Summary", seriesInfo.filteredData)]

        # Give tasks to the taskserver to run parallelly
        logger.debug("Sending tasks to taskserver")
        self.taskserver.setTasks(tasks)
        self.taskserver.processTasks()

        if self.editID == seriesInfo.seriesID:
            #set color to black for editing
            seriesInfo.edit = True
            seriesInfo.plotcolor = self.colorList.pop(0)
            seriesInfo.color = "Black"
        else:
            seriesInfo.color = self.colorList.pop(0)
        return seriesInfo

    def updateDateRange(self, startDate=None, endDate=None):
        self.currentStart = startDate
        self.currentEnd = endDate
        for key in self.getSeriesIDs():
            seriesInfo = self._seriesInfos[key]
            if startDate:
                data = self.memDB.getDataValuesforGraph(key, seriesInfo.noDataValue, startDate, endDate)
                self.isSubsetted = True
                self.currentStart = startDate
                self.currentEnd = endDate
            else:
                #this returns the series to its full daterange
                data = self.memDB.getDataValuesforGraph(key, seriesInfo.noDataValue, seriesInfo.startDate,
                                                        seriesInfo.endDate)
                self.isSubsetted = False
                self.currentStart = self.startDate
                self.currentEnd = self.endDate

            seriesInfo.dataTable = data
            #Tests to see if any values were returned for the given daterange
            self.build(seriesInfo)


class Statistics(object):
    def __init__(self, data):

        # dataValues = [x[0] for x in dataTable if x[0] <> noDataValue]
        #data = sorted(dataValues)
        d = data.describe(percentiles=[.10, .25, .5, .75, .90])
        count = self.NumberofObservations = d["DataValue"]["count"]
        self.NumberofCensoredObservations = data[data["CensorCode"] != "nc"].count().DataValue
        self.ArithemticMean = round(d["DataValue"]["mean"], 5)

        sumval = 0
        sign = 1
        for dv in data["DataValue"]:
            if dv == 0:
                sumval = sumval + np.log2(1)
            else:
                if dv < 0:
                    sign = sign * -1
                sumval = sumval + np.log2(np.absolute(dv))

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

        interval_types = ["Overall", "Year", "Month", "Season"]
        intervals = ["Overall", "Year", "Month", "Season"]

        interval_options = zip(interval_types, intervals)
        for interval_type, interval in interval_options:
            start_time = timeit.default_timer()
            if interval_type == "Overall":
                interval = data
            else:
                interval = data.groupby(interval_type)
            self.calculateBoxWhiskerData(interval, interval_type)
            elapsed = timeit.default_timer() - start_time
            logger.debug("elapsed time for %s: %s" % (interval_type, elapsed))

        self.currinterval = self.intervals[self.method]

    def calculateBoxWhiskerData(self, interval, interval_type):
        """

        :param interval:
        :return:
        """

        results = self.calculateIntervalsOnGroups(interval)

        if interval_type == "Season" or interval_type == "Month":
            func = None
            if interval_type == "Season":
                func = numToSeason
            elif interval_type == "Month":
                func = numToMonth

            self.intervals[interval_type] = BoxWhiskerPlotInfo(
                interval_type, interval_type, [func(x) for x in results["names"]],
                [results["median"], results["conflimit"], results["mean"], results["confint"]])

        elif interval_type == "Overall":
            self.intervals[interval_type] = BoxWhiskerPlotInfo(
                interval_type, None, [],
                [results["median"], results["conflimit"], results["mean"], results["confint"]])

        else:
            self.intervals[interval_type] = BoxWhiskerPlotInfo(
                interval_type, interval_type, results["names"],
                [results["median"], results["conflimit"], results["mean"], results["confint"]])


    def calculateIntervalsOnGroups(self, interval):

        mean = []
        median = []
        confint = []
        conflimit = []
        names = []

        if isinstance(interval, pd.core.groupby.DataFrameGroupBy):
            for name, group in interval:
                datavalue = group['DataValue']
                group_mean = np.mean(datavalue)
                group_median = np.median(datavalue)
                group_std = math.sqrt(np.var(datavalue))
                group_sqrt = math.sqrt(len(group))
                group_deviation = group_std / group_sqrt
                ci = stats.norm.interval(.95, group_mean, scale=10*group_deviation)
                cl = stats.norm.interval(.95, group_median, scale=group_deviation)

                names.append(name)
                conflimit.append((cl[0], cl[1]))
                confint.append((ci[0], ci[1]))
                median.append(group_median)
                mean.append(group_mean)
        else:
            name = "Overall"
            datavalue = interval['DataValue']
            data_mean = np.mean(datavalue)
            data_median = np.median(datavalue)
            data_std = math.sqrt(np.var(datavalue))
            data_sqrt = math.sqrt(len(interval))
            data_deviation = data_std / data_sqrt

            ci = stats.norm.interval(.95, data_mean, scale=10*data_deviation)
            cl = stats.norm.interval(.95, data_median, scale=data_deviation)

            mean.append(data_mean)
            median.append(data_median)
            confint.append((ci[0], ci[1]))
            conflimit.append((cl[0], cl[1]))

        results = {}
        results["names"] = names
        results["mean"] = mean
        results["median"] = median
        results["confint"] = confint
        results["conflimit"] = conflimit

        return results

    def setInterval(self, title):
        self.method = title
        self.currinterval = self.intervals[self.method]


class BoxWhiskerPlotInfo(object):
    def __init__(self, title, groupby, xLabels, dets):
        self.title = title

        self.xlabels = xLabels
        self.groupby = groupby

        self.medians = dets[0]
        self.confint = dets[1]
        self.means = dets[2]
        self.conflimit = dets[3]


class Probability(object):
    def __init__(self, data):
        """

        Probability (Frequency of Exceedence) Algorithm
        * sorted = Sort values
        * ranks = Rank sorted values
        * Reverse the ranking
        * Calculate Probability of Exceedence using algorithm: ranks/(len(sorted)+1) * 100

        #First, I sort the values.
        ##sorted <- sort(TSSpred)

        #Then, I rank the sorted values.
        ##ranks <- rank(sorted, ties.method="max")

        #Then, I reverse the ranking.
        ##ranks <- max(ranks)-ranks

        #This is the actual formula- rank/(length+1) as a %
        #PrbExc = ranks/(length(sorted)+1)*100

        #Here I plot the probability of exceedance (PrbExc) against the sorted initial values (sorted).
        #plot(PrbExc, sorted, type='n', col='white', font.lab=1.5, xlab="Frequency of Exceedance, percent", ylab="TSS, mg/L",log="y")


        :param data:
        :return:
        """

        # Determine rank, sorting values doesn't change outcome while using pandas.
        ranks = data['DataValue'].rank()
        PrbExc = ranks / (len(ranks) + 1) * 100

        self.xAxis = PrbExc
        self.yAxis = data['DataValue']


def numToMonth(date):
    date = int(date)
    return {
        1: 'Jan',
        2: 'Feb',
        3: 'Mar',
        4: 'Apr',
        5: 'May',
        6: 'Jun',
        7: 'Jul',
        8: 'Aug',
        9: 'Sep',
        10: 'Oct',
        11: 'Nov',
        12: 'Dec'
    }[date]


def numToSeason(date):
    date = int(date)
    return {
        1: 'Winter',
        2: 'Spring',
        3: 'Summer',
        4: 'Fall'

    }[date]












