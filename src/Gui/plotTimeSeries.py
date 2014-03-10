#!/usr/bin/python
import datetime

import wx
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
from matplotlib.font_manager import FontProperties
from matplotlib.widgets import Lasso
from matplotlib import path
from wx.lib.pubsub import pub as Publisher

from mnuPlotToolbar import MyCustomToolbar as NavigationToolbar

## Enable logging
import logging
from common.logger import LoggerTool
tool = LoggerTool()

logger = tool.setupLogger(__name__, __name__ + '.log', 'w' ,logging.DEBUG)

class plotTimeSeries(wx.Panel):
    def _init_coll_boxSizer1_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        parent.AddWindow(self.toolbar, 0, wx.EXPAND)


    def _init_sizers(self):
        # generated method, don't edit
        self.boxSizer1 = wx.BoxSizer(orient=wx.VERTICAL)
        self._init_coll_boxSizer1_Items(self.boxSizer1)
        self.SetSizer(self.boxSizer1)


    def _init_ctrls(self, parent):
        wx.Panel.__init__(self, parent, -1)
        self.parent = parent


        #init Plot
        self.timeSeries = host_subplot(111, axes_class=AA.Axes)
        self.timeSeries.plot([], [])
        self.timeSeries.set_title("No Data To Plot")
        self.canvas = FigCanvas(self, -1, plt.gcf())
        self.canvas.SetFont(wx.Font(20, wx.SWISS, wx.NORMAL, wx.NORMAL,
                                    False, u'Tahoma'))

        # Create the navigation toolbar, tied to the canvas
        self.toolbar = NavigationToolbar(self.canvas, allowselect=True)
        self.toolbar.Realize()
        self.seriesPlotInfo = None

        #set properties
        self.fontP = FontProperties()
        self.fontP.set_size('small')

        self.format = '-o'
        self._setColor("WHITE")

        #init hover tooltip

        # create a long tooltip with newline to get around wx bug (in v2.6.3.3)
        # where newlines aren't recognized on subsequent self.tooltip.SetTip() calls
        self.tooltip = wx.ToolTip(tip='tip with a long %s line and a newline\n')
        self.canvas.SetToolTip(self.tooltip)
        self.tooltip.Enable(False)
        self.tooltip.SetDelay(0)

        #init lists
        self.lines = []
        self.axislist = {}
        self.curveindex = -1
        self.editseriesID = -1
        self.editCurve = None
        self.lassoAction = None
        self.hoverAction = None

        self.maxStart = datetime.datetime(1900, 01, 01, 0, 0, 0)
        self.maxEnd = datetime.datetime.now()

        self.canvas.draw()
        self._init_sizers()

    def changeSelection(self, sellist):

        #print "sellist: ", sellist
        # k black
        # r red
        # needs to have graph first

        #list of True False
        self.editPoint.set_color(['k' if x == 0 else 'r' for x in sellist])
        self.parent.record_service.select_points_tf(sellist)
        Publisher.sendMessage(("changeTableSelection"), sellist=sellist)

        self.canvas.draw()

    def onDateChanged(self, startDate, endDate):
        self.startDate = startDate
        self.endDate = endDate
        self.timeSeries.axis.axes.set_xbound(startDate, endDate)
        self.canvas.draw()


    def setDateBound(self, start, end):
        if start > self.maxStart:
            self.startDate = self.maxStart = start
        if end < self.maxEnd:
            self.endDate = self.maxEnd = end
        Publisher.sendMessage(("resetdate"), startDate=self.maxStart, endDate=self.maxEnd)


    def onShowLegend(self, isVisible):
        # print self.timeSeries.show_legend
        if isVisible:
            plt.subplots_adjust(bottom=.1 + .1)
            self.timeSeries.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
                                   ncol=2, prop=self.fontP)
        else:
            plt.subplots_adjust(bottom=.1)
            self.timeSeries.legend_ = None
        # self.timeSeries.plot(legend= not isVisible)
        self.canvas.draw()


    def onPlotType(self, ptype):
        # self.timeSeries.clear()
        if ptype == "line":
            ls = '-'
            m = 'None'
        elif ptype == "point":
            ls = 'None'
            m = 'o'
        else:
            ls = '-'
            m = 'o'

        format = ls + m
        for line, i in zip(self.lines, range(len(self.lines))):
            if not (i == self.curveindex):
                plt.setp(line, linestyle=ls, marker=m)

        self.canvas.draw()

#clear plot
    def clear(self):
        lines = []
        for key, ax in self.axislist.items():
            ax.clear()
            # self.stopEdit()


    def stopEdit(self):
        self.clear()
        self.selectedlist = None
        self.editPoint = None
        self.lman = None
        self.canvas.mpl_disconnect(self.lassoAction)
        self.canvas.mpl_disconnect(self.hoverAction)
        self.lassoAction = None
        self.hoverAction = None
        self.xys = None

        self.curveindex = -1
        self.editCurve = None
        # self.RefreshPlot()
        if self.seriesPlotInfo and self.seriesPlotInfo.isPlotted(self.editseriesID):
            self.updatePlot()
        self.editseriesID = -1


    def updateValues(self):
        # self.addEdit(self.editCursor, self.editSeries, self.editDataFilter)

        #clear current edit points and curve
        curraxis = self.axislist[self.editCurve.axisTitle]
        for l in curraxis.lines:
            if l.get_label() == self.editCurve.plotTitle:
                curraxis.lines.remove(l)
        self.editPoint.remove()


        #redraw editpoints and curve
        self.seriesPlotInfo.updateEditSeries()
        self.editCurve = self.seriesPlotInfo.getEditSeriesInfo()
        self.drawEditPlot(self.editCurve)
        Publisher.sendMessage(("refreshTable"), e=None)
        # self.parent.parent.dataTable.Refresh()
        self.canvas.draw()


    def drawEditPlot(self, oneSeries):
        curraxis = self.axislist[oneSeries.axisTitle]
        self.lines[self.curveindex] = curraxis.plot_date([x[1] for x in oneSeries.dataTable],
                                                         [x[0] for x in oneSeries.dataTable], "-",
                                                         color=oneSeries.color, xdate=True, tz=None,
                                                         label=oneSeries.plotTitle)

        self.selectedlist = self.parent.record_service.get_filter_list()
        self.editPoint = curraxis.scatter([x[1] for x in oneSeries.dataTable], [x[0] for x in oneSeries.dataTable],
                                          s=20, c=['k' if x == 0 else 'r' for x in self.selectedlist])
        self.xys = [(matplotlib.dates.date2num(x[1]), x[0]) for x in oneSeries.dataTable]

        self.lassoAction = self.canvas.mpl_connect('button_press_event', self._onPress)
        self.hoverAction = self.canvas.mpl_connect('motion_notify_event', self._onMotion)


    def _setColor(self, color):
        """Set figure and canvas colours to be the same.
        :rtype : object
        """
        plt.gcf().set_facecolor(color)
        plt.gcf().set_edgecolor(color)
        self.canvas.SetBackgroundColour(color)


    def close(self):
        plt.close()


    def Plot(self, seriesPlotInfo):
        self.seriesPlotInfo = seriesPlotInfo
        self.updatePlot()


    def updatePlot(self):
        self.clear()
        count = self.seriesPlotInfo.count()
        self.lines = []

        # self.timeSeries=self.canvas.add_subplot(111)
        self.setUpYAxis()

        for oneSeries in self.seriesPlotInfo.getSeriesInfo():
            #is this the series to be edited
            if oneSeries.seriesID == self.seriesPlotInfo.getEditSeriesID():

                self.curveindex = len(self.lines)
                self.lines.append("")
                self.editCurve = oneSeries
                self.drawEditPlot(oneSeries)

            else:
                curraxis = self.axislist[oneSeries.axisTitle]
                self.lines.append(
                    curraxis.plot_date([x[1] for x in oneSeries.dataTable], [x[0] for x in oneSeries.dataTable],
                                       self.format, color=oneSeries.color, xdate=True, tz=None,
                                       label=oneSeries.plotTitle))

            self.setDateBound(oneSeries.dataTable[1][1], oneSeries.dataTable[-1][1])
        if count > 1:
            # self.timeSeries.set_title("Multiple Series plotted")
            self.timeSeries.set_title("")
            plt.subplots_adjust(bottom=.1 + .1)
            # self.timeSeries.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
            #      ncol=2, prop = self.fontP)
            self.timeSeries.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
                                   ncol=2, prop=self.fontP)
        elif count == 0:
            self.timeSeries.set_title("")
            self.timeSeries.legend_ = None
        else:
            self.timeSeries.set_title(oneSeries.plotTitle)
            plt.subplots_adjust(bottom=.1)
            self.timeSeries.legend_ = None


        # self.timeSeries.set_xlim([0,1000])
        self.timeSeries.set_xlabel("Date Time")
        self.canvas.draw()


    def setEdit(self, id):
        self.editseriesID = id
        if self.seriesPlotInfo and self.seriesPlotInfo.isPlotted(self.editseriesID):
            self.editCurve = self.seriesPlotInfo.getSeries(self.editseriesID)
            self.updatePlot()
            # print self.editCurve


    def setUpYAxis(self):
        self.axislist = {}
        left = 0
        right = 0
        adj = .05
        #loop through the list of curves and add an axis for each
        for oneSeries in self.seriesPlotInfo.getSeriesInfo():
            #test to see if the axis already exists
            if not oneSeries.axisTitle in self.axislist:
                self.axislist[oneSeries.axisTitle] = None

        for i, axis in zip(range(len(self.axislist)), self.axislist):
            if i % 2 == 0:
                left = left + 1
                #add to the left(yaxis)
                if i == 0:
                    #if first plot use the orig axis
                    newAxis = self.timeSeries
                else:
                    newAxis = self.timeSeries.twinx()
                    new_fixed_axis = newAxis.get_grid_helper().new_fixed_axis
                    newAxis.axis['left'] = new_fixed_axis(loc='left', axes=newAxis, offset=(-30 * left, 0))
                    newAxis.axis["left"].toggle(all=True)
                    newAxis.axis["right"].toggle(all=False)
                    plt.subplots_adjust(left=.10 + (adj * (left - 1)))

            else:
                right = right + 1
                #add to the right(y2axis)
                newAxis = self.timeSeries.twinx()
                new_fixed_axis = newAxis.get_grid_helper().new_fixed_axis
                newAxis.axis['right'] = new_fixed_axis(loc='right', axes=newAxis, offset=(60 * (right - 1), 0))
                newAxis.axis['right'].toggle(all=True)
                plt.subplots_adjust(right=.9 - (adj * right))

            newAxis.set_ylabel(axis)
            self.axislist[axis] = newAxis


    def callback(self, verts):
        seldatetimes = [matplotlib.dates.num2date(x[0]) for x in verts]
        #print seldatetimes

        self.parent.record_service.select_points(datetime_list=seldatetimes)

        p = path.Path(verts)
        ind = p.contains_points(self.xys)
        self.changeSelection(ind)

        self.canvas.draw_idle()
        self.canvas.widgetlock.release(self.lasso)
        del self.lasso


    def _onPress(self, event):
        if self.canvas.widgetlock.locked(): return
        if event.inaxes is None: return
        self.lasso = Lasso(event.inaxes, (event.xdata, event.ydata), self.callback)
        # acquire a lock on the widget drawing
        self.canvas.widgetlock(self.lasso)

    def _onMotion(self, event):
        collisionFound = False
        if event.xdata != None and event.ydata != None:  #mouse is inside the axes
            #print len(self.editCurve.dataTable), len(self.editCurve.dataTable[:1])
            for i in xrange(len(self.editCurve.dataTable)):
                radius = 3
                #print "row: ", i,  self.editCurve.dataTable[i][1].toordinal(), event.xdata, abs(event.xdata - self.editCurve.dataTable[i][1].toordinal())

                if abs(event.xdata - self.editCurve.dataTable[i][1].toordinal()) < radius and abs(
                                event.ydata - self.editCurve.dataTable[i][0]) < radius:
                    top = tip = '(%s, %f)' % (self.editCurve.dataTable[i][1], self.editCurve.dataTable[i][0])
                    self.tooltip.SetTip(tip)
                    self.tooltip.Enable(True)
                    collisionFound = True
                    break
        if not collisionFound:
            self.tooltip.Enable(False)

    def __init__(self, parent, id, pos, size, style, name):
        self._init_ctrls(parent)

