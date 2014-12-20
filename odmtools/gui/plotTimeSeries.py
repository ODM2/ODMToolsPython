#!/usr/bin/python
import datetime
from matplotlib.ticker import FormatStrFormatter

import wx
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd

import mpl_toolkits.axisartist as AA

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas
from mpl_toolkits.axes_grid1 import host_subplot


from matplotlib.lines import Line2D
from matplotlib.text import Text

from matplotlib.font_manager import FontProperties
from wx.lib.pubsub import pub as Publisher
from mnuPlotToolbar import MyCustomToolbar as NavigationToolbar

## Enable logging
import logging
from odmtools.common.logger import LoggerTool

tool = LoggerTool()
logger = tool.setupLogger(__name__, __name__ + '.log', 'w', logging.DEBUG)


class plotTimeSeries(wx.Panel):
    def __init__(self, parent, id, pos, size, style, name):
        self._init_ctrls(parent)


    def _init_coll_boxSizer1_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        parent.AddWindow(self.toolbar, 0, wx.EXPAND)

    def _init_ctrls(self, parent):
        wx.Panel.__init__(self, parent, -1)
        self.parent = parent

        #init Plot
        # matplotlib.figure.Figure
        self.figure = plt.figure()

        # matplotlib.axes.AxesSubplot
        self.timeSeries = host_subplot( 111, axes_class=AA.Axes)
        #self.timeSeries = self.figure.add_subplot(111)
        #self.timeSeries.plot([], [], picker=5)
        self.setTimeSeriesTitle("No Data to Plot")

        # matplotlib.backends.backend_wxagg.FigureCanvasWxAgg
        self.canvas = FigCanvas(self, -1, self.figure)

        self.canvas.SetFont(wx.Font(20, wx.SWISS, wx.NORMAL, wx.NORMAL, False, u'Tahoma'))
        self.isShowLegendEnabled = False

        '''
        import pandas as pd
        import numpy as np

        self.data = pd.DataFrame(np.random.randn(14, 2),
                    index=np.arange('2005-02', '2005-02-15', dtype='datetime64[D]'),
                    columns=['first', 'sec'])

        #ax = self.data.plot(ax=self.timeSeries, title='sample')
        '''

        #self.hoverAction = self.canvas.mpl_connect('motion_notify_event', self._onMotion)
        #self.pointPick = self.canvas.mpl_connect('pick_event', self._onPick)
        self.canvas.mpl_connect('figure_leave_event', self._onFigureLeave)
        Publisher.subscribe(self.updateCursor, "updateCursor")

        # Create the navigation toolbar, tied to the canvas
        self.toolbar = NavigationToolbar(self.canvas, allowselect=True)
        self.toolbar.Realize()
        self.seriesPlotInfo = None

        #set properties
        self.fontP = FontProperties()
        self.fontP.set_size('x-small')

        self.format = '-o'
        self.alpha=1
        self._setColor("WHITE")

        left = 0.125  # the left side of the subplots of the figure
        #right = 0.9  # the right side of the subplots of the figure
        #bottom = 0.51  # the bottom of the subplots of the figure
        #top = 1.2  # the top of the subplots of the figure
        #wspace = .8  # the amount of width reserved for blank space between subplots
        #hspace = .8  # the amount of height reserved for white space between subplots
        plt.subplots_adjust(
            left=left#, bottom=bottom, right=right, top=top, wspace=wspace, hspace=hspace
        )
        plt.tight_layout()

        #init hover tooltip

        # create a long tooltip with newline to get around wx bug (in v2.6.3.3)
        # where newlines aren't recognized on subsequent self.tooltip.SetTip() calls
        self.tooltip = wx.ToolTip(tip='tip with a long %s line and a newline\n')
        self.canvas.SetToolTip(self.tooltip)
        self.tooltip.Enable(False)
        self.tooltip.SetDelay(0)

        #init lists
        #self.lines = {}
        self.lines = []
        self.axislist = {}
        self.curveindex = -1
        self.editseriesID = -1
        self.editCurve = None
        self.editPoint =None
        self.hoverAction = None
        self.selplot= None

        self.cursors = []

        self.canvas.draw()
        self._init_sizers()

    def _init_sizers(self):
        # generated method, don't edit
        self.boxSizer1 = wx.BoxSizer(orient=wx.VERTICAL)
        self._init_coll_boxSizer1_Items(self.boxSizer1)
        self.SetSizer(self.boxSizer1)

    '''
    def changePlotSelection(self, datetime_list=[]):
        cc= ColorConverter()
        # k black,    # r red
        # needs to have graph first
        selected = cc.to_rgba('r', 1)
        unselected = cc.to_rgba('k', 0.1)
        allunselected = cc.to_rgba('k', 1)
        if self.editPoint:
            colorlist=[allunselected] *len(self.editCurve.dataTable)
            if len(datetime_list)>0:
                for i in xrange(len(self.editCurve.dataTable)):
                    if  self.editCurve.dataTable[i][1] in datetime_list:
                        colorlist[i]=selected
                    else:
                        colorlist[i]=unselected

            self.editPoint.set_color(colorlist)
            #self.editPoint.set_color(['k' if x == 0 else 'r' for x in tflist])
            self.canvas.draw()

    '''
    ## TODO 10/15/2014 Change function so that it will accept a list of datavalues. This will remove the need to loop through the values currently plotted and we would instead plot the list of datetimes and datavalues together.

    def changePlotSelection(self,  datetime_list=[]):
        if self.selplot:
            self.selplot.remove()
            del(self.selplot)
            self.selplot = None

        if not len(datetime_list) > 0:
            return

        result = None
        if isinstance(datetime_list, list):
            df = self.editCurve.dataTable
            result = df[df['LocalDateTime'].isin(datetime_list)].astype(datetime.datetime)

        elif isinstance(datetime_list, pd.DataFrame):
            filtered_datetime_dataframe = datetime_list
            result = filtered_datetime_dataframe.astype(datetime.datetime)

        if result.empty:
            return

        values = result['DataValue'].values.tolist()
        dates = result.LocalDateTime.values.tolist()
        self.selplot = self.axislist[self.editSeries.axisTitle].scatter(dates, values, s=35, c='red',
                                                                        edgecolors='none', zorder=12, marker='s', alpha=1)
        self.canvas.draw()


    def lassoChangeSelection(self, datetime_list=[]):
        self.changePlotSelection(datetime_list)
        self.parent.record_service.select_points(datetime_list=datetime_list)
        Publisher.sendMessage("changeTableSelection",  datetime_list=datetime_list)


    def onShowLegend(self, isVisible):
        if isVisible:
            self.isShowLegendEnabled = True
            plt.subplots_adjust(bottom=.1 + .1)
            leg = self.timeSeries.legend(loc='upper right', ncol=2, fancybox=True, prop=self.fontP)
            leg.get_frame().set_alpha(.5)
            leg.draggable(state=True)
        else:
            self.isShowLegendEnabled = False
            plt.subplots_adjust(bottom=.1)
            self.timeSeries.legend_ = None

        plt.gcf().autofmt_xdate()
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

        self.format = ls + m
        for line, i in zip(self.lines, range(len(self.lines))):
            if not (i == self.curveindex):
                plt.setp(line, linestyle=ls, marker=m)

        if self.isShowLegendEnabled:
            self.onShowLegend(self.isShowLegendEnabled)

        plt.gcf().autofmt_xdate()
        self.canvas.draw()

    def stopEdit(self):
        self.clear()
        self.selectedlist = None

        self.selplot = None
        self.lman = None

        #self.canvas.mpl_disconnect(self.hoverAction)
        try:
            self.canvas.mpl_disconnect(self.pointPick)
            self.pointPick = None
        except AttributeError as e:
            logger.error(e)

        self.hoverAction = None
        self.xys = None
        self.alpha=1

        self.curveindex = -1
        self.editCurve = None
        # self.RefreshPlot()
        if self.seriesPlotInfo and self.seriesPlotInfo.isPlotted(self.editseriesID):
            self.updatePlot()
        self.toolbar.stopEdit()
        self.editseriesID = -1

    def updateValues(self):
        # self.addEdit(self.editCursor, self.editSeries, self.editDataFilter)

        #clear current edit points and curve
        if self.editCurve:
            curraxis = self.axislist[self.editCurve.axisTitle]
            for l in curraxis.lines:
                if l.get_label() == self.editCurve.plotTitle:
                    curraxis.lines.remove(l)

            #redraw editpoints and curve
            self.seriesPlotInfo.updateEditSeries()
            self.editCurve = self.seriesPlotInfo.getEditSeriesInfo()
            self.drawEditPlot(self.editCurve)
            self.canvas.draw()
        Publisher.sendMessage("refreshTable", e=None)
        # self.parent.parent.dataTable.Refresh()
        plt.gcf().autofmt_xdate()
        self.canvas.draw()

    def drawEditPlot(self, oneSeries):
        self.axislist[oneSeries.axisTitle].set_zorder(10)
        self.lines[self.curveindex] = self.axislist[oneSeries.axisTitle]
        data = oneSeries.dataTable
        dates = data['LocalDateTime'].astype(datetime.datetime)
        curraxis = self.axislist[oneSeries.axisTitle]

        curraxis.plot_date(dates, data['DataValue'], "-s",
                 color=oneSeries.color, xdate=True, label=oneSeries.plotTitle, zorder=10, alpha=1,
                 picker=5.0, pickradius=5.0, markersize=4.5)
        curraxis.set_xlabel('Date')

        convertedDates = matplotlib.dates.date2num(dates)
        self.xys = zip(convertedDates, oneSeries.dataTable['DataValue'])
        self.toolbar.editSeries(self.xys, self.editCurve)
        self.pointPick = self.canvas.mpl_connect('pick_event', self._onPick)
        self.editSeries = oneSeries


    def _setColor(self, color):
        """Set figure and canvas colours to be the same.
        :rtype : object
        """
        plt.gcf().set_facecolor(color)
        plt.gcf().set_edgecolor(color)
        self.canvas.SetBackgroundColour(color)

    def close(self):
        #plt.clf()
        #plt.close()
        pass

    def Plot(self, seriesPlotInfo):
        self.seriesPlotInfo = seriesPlotInfo
        self.updatePlot()
        # resets the home view - will remove any previous zooming
        self.toolbar.update()
        self.toolbar.push_current()

        #self._views.home()
        #self._positions.home()
        #self.set_history_buttons()

    #clear plot
    def clear(self):
        """

        :return:
        """

        lines = []
        for key, ax in self.axislist.items():
            ax.clear()
        self.axislist = {}
        #self.canvas.draw()
            # self.stopEdit()
        #print "TimeSeries: ", dir(self.timeSeries), type(self.timeSeries)
        #plt.cla()
        #plt.clf()
        #self.timeSeries.plot([], [], picker=5)


    def setUpYAxis(self):
        """ Setting up multiple axes

        :return:
        """

        self.axislist = {}
        left = 0
        right = 0
        adj = .05
        editaxis = None

        ## Identify Axes and save them to axislist
        #loop through the list of curves and add an axis for each
        for oneSeries in self.seriesPlotInfo.getAllSeries():
            #test to see if the axis already exists
            if oneSeries.edit:
                editaxis = oneSeries.axisTitle
            if not oneSeries.axisTitle in self.axislist:
                self.axislist[oneSeries.axisTitle] = None
        keys = self.axislist.keys()

        ## Put editing axis at the beginning of the list
        if editaxis:
            for i in range(len(keys)):
                if keys[i] == editaxis:
                    keys.pop(i)
                    break
            keys.insert(0, editaxis)

        leftadjust = -30
        for i, axis in zip(range(len(self.axislist)), keys):
            if i % 2 == 0:
                left = left + 1
                #add to the left(yaxis)
                if i == 0:
                    #if first plot use the orig axis
                    newAxis = self.timeSeries
                else:
                    newAxis = self.timeSeries.twinx()
                    '''
                    Spines idea
                    #newAxis.spines["left"].set_position(("axes", leftadjust * left))
                    newAxis.spines["left"].set_position(("axes", -.1))
                    newAxis.spines["left"].set_visible(True)
                    newAxis.yaxis.set_label_position("left")
                    newAxis.yaxis.set_ticks_position("left")
                    '''

                    new_fixed_axis = newAxis.get_grid_helper().new_fixed_axis
                    newAxis.axis['left'] = new_fixed_axis(loc='left', axes=newAxis, offset=(leftadjust * left, 0))
                    newAxis.axis["left"].toggle(all=True)
                    newAxis.axis["right"].toggle(all=False)

                    leftadjust -= 15

            else:
                right = right + 1
                #add to the right(y2axis)
                newAxis = self.timeSeries.twinx()

                '''
                Spines idea
                #newAxis.spines["right"].set_position(("axes", -1*60*(right - 1)))
                newAxis.spines["right"].set_position(("axes", 1.0))
                newAxis.spines["right"].set_visible(True)
                newAxis.yaxis.set_label_position("right")
                newAxis.yaxis.set_ticks_position("right")
                '''

                new_fixed_axis = newAxis.get_grid_helper().new_fixed_axis
                newAxis.axis['right'] = new_fixed_axis(loc='right', axes=newAxis, offset=(60 * (right - 1), 0))
                newAxis.axis['right'].toggle(all=True)


            a = newAxis.set_ylabel(axis, picker=True)
            a.set_picker(True)

            #logger.debug("axis label: %s" % (axis))
            self.axislist[axis] = newAxis

    def updatePlot(self):
        self.clear()
        count = self.seriesPlotInfo.count()
        self.setUpYAxis()
        self.lines = []

        ## Spine initialization ##
        for oneSeries in self.seriesPlotInfo.getAllSeries():
            if oneSeries.seriesID == self.seriesPlotInfo.getEditSeriesID():
                """

                Edited Series

                """
                self.curveindex = len(self.lines)
                self.lines.append("")
                self.editCurve = oneSeries
                self.drawEditPlot(oneSeries)



            else:
                """

                Plotted Series

                """
                curraxis = self.axislist[oneSeries.axisTitle]
                curraxis.set_zorder(1)

                data = oneSeries.dataTable
                dates = data['LocalDateTime'].astype(datetime.datetime)
                #data.plot(ax=curraxis)
                curraxis.plot_date(dates, data['DataValue'],
                        color=oneSeries.color, fmt=self.format, xdate=True, tz=None, antialiased=True,
                        label=oneSeries.plotTitle, alpha=self.alpha, picker=5.0, pickradius=5.0,
                        markersize=4)

                curraxis.set_xlabel('Date')


                '''
                data = oneSeries.dataTable
                #dates = data['LocalDateTime'].astype(datetime.datetime)

                data['LocalDateTime'] = pd.to_datetime(data['LocalDateTime'])
                data['LocalDateTime'].astype(datetime.datetime)

                data.plot(ax=curraxis)
                oneSeries.dataTable.plot(ax=curraxis)
                curraxis.set_xlabel('Date')
                '''




        if count > 1:
            self.setTimeSeriesTitle("")
            plt.subplots_adjust(bottom=.1 + .1)
            # self.timeSeries.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
            #      ncol=2, prop = self.fontP)
            self.timeSeries.legend(loc='upper center', bbox_to_anchor=(0.5, -1.75),
                                   ncol=2, prop=self.fontP)

        elif count == 0:
            self.setTimeSeriesTitle("")
            self.timeSeries.legend_ = None
        else:
            self.setTimeSeriesTitle(oneSeries.siteName)
            plt.subplots_adjust(bottom=.1)
            self.timeSeries.legend_ = None

        self.timeSeries.set_xlabel("Date", picker=True)
        #self.timeSeries.set_xlim(matplotlib.dates.date2num([self.seriesPlotInfo.currentStart, self.seriesPlotInfo.currentEnd]))

        #self.timeSeries.axis[:].set_major_formatter(FormatStrFormatter('%.2f'))

        self.timeSeries.axis[:].major_ticks.set_tick_out(True)
        self.timeSeries.axis["bottom"].label.set_pad(20)
        self.timeSeries.axis["bottom"].major_ticklabels.set_pad(15)
        self.timeSeries.axis["bottom"].major_ticklabels.set_rotation(15)
        self.timeSeries.axis[:].major_ticklabels.set_picker(True)


        plt.gcf().autofmt_xdate()

        self.figure.tight_layout()
        if not self.toolbar._views.empty():
            for v in self.toolbar._views:
                del(v)
            self.toolbar.push_current()

        self.canvas.draw()

    def updateCursor(self, selectedObject):
        """
        :param selectedObject:
        """

        try:
            if selectedObject:
                if self.seriesPlotInfo:
                    seriesInfo = self.seriesPlotInfo.getSelectedSeries(selectedObject.id)

                    if seriesInfo:
                        currentAxis = None
                        # If there a key with the axisTitle we are interested in, set currentaxis to that.
                        if seriesInfo.axisTitle in self.axislist.keys():
                            currentAxis = self.axislist[seriesInfo.axisTitle]
                        # If nothing is in the axislist, we don't care about it
                        elif len(self.axislist) < 1:
                            currentAxis = None
                        self.configureCursor(currentAxis)

        except AttributeError as e:
            print "Ignoring Attribute Error", e


    def configureCursor(self, currentAxis=None):
        """Creates the cursors for each axes in order to provide data hovering"""

        # Disable existing Cursors
        if self.cursors:
            for i in self.cursors:
                i.disable()
        self.cursors = []

        # initialize cursors for axes from currently selected axes
        for k, v in self.axislist.iteritems():
            i = Cursor(self.canvas, self.toolbar, v, k)
            ## If I have selected an axis that is in the axislist
            if v == currentAxis:
                i.enable()
                i.setSelected(currentAxis)
            # If there is only one axis in the axislist, default to the first axis
            elif len(self.axislist) == 1:
                i.enable()
                i.setSelected(self.axislist.values()[0])
            # Else I disable the other axes that I don't care about
            else:
                i.setSelected(None)
                i.disable()

            self.cursors.append(i)

    def setTimeSeriesTitle(self, title=""):
        """Set the title of the TimeSeries plot"""
        self.timeSeries.set_title(title, picker=True)

    def setEdit(self, id):
        self.editseriesID = id
        self.alpha = .5

        if self.seriesPlotInfo and self.seriesPlotInfo.isPlotted(self.editseriesID):
            self.editCurve = self.seriesPlotInfo.getSeries(self.editseriesID)

            ## TODO Duplicate UpdatePlot?
            logger.debug("Called duplicate updateplot")
            #self.updatePlot()



    def make_patch_spines_invisible(self, ax):
        ax.set_frame_on(True)
        ax.patch.set_visible(False)
        for sp in ax.spines.itervalues():
            sp.set_visible(False)

    def _onMotion(self, event):
        """

        :type event: matplotlib.backend_bases.MouseEvent
        :return:
        """
        try:
            if event.xdata and event.ydata:
                xValue = matplotlib.dates.num2date(event.xdata).replace(tzinfo=None)
                #self.toolbar.msg.SetLabelText("X= %s,  Y= %.2f" % (xValue.strftime("%Y-%m-%d %H:%M:%S"), event.ydata))
                #self.toolbar.msg.SetLabelText("X= %s,  Y= %.2f" % (xValue.strftime("%b %d, %Y %H:%M:%S"), event.ydata))
                self.toolbar.msg.SetLabelText("X= %s,  Y= %.2f" % (xValue.strftime("%b %d, %Y %H:%M"), event.ydata))
                self.toolbar.msg.SetForegroundColour((66, 66, 66))
            else:
                self.toolbar.msg.SetLabelText("")
        except ValueError:
            pass

    def _onPick(self, event):
        """

        :param event:
        :return:
        """

        if isinstance(event.artist, Line2D):
            thisline = event.artist
            xdata = thisline.get_xdata()
            ydata = thisline.get_ydata()
            ind = event.ind

            xValue = xdata[ind][0]
            yValue = ydata[ind][0]
            #tip = '(%s, %s)' % (xValue.strftime("%Y-%m-%d %H:%M:%S"), yValue)
            #tip = '(%s, %s)' % (xValue.strftime("%b %d, %Y %H:%M:%S"), yValue)
            tip = '(%s, %s)' % (xValue.strftime("%b %d, %Y %H:%M"), yValue)

            self.tooltip.SetTip(tip)
            self.tooltip.Enable(True)
            self.tooltip.SetAutoPop(10000)

        elif isinstance(event.artist, Text):
            text = event.artist
            #print "Picking Label: ", text.get_text()

    def _onFigureLeave(self, event):
        """Catches mouse leaving the figure

        :param event:
        :return:
        """

        if self.tooltip.Window.Enabled:
            self.tooltip.SetTip("")

class Cursor(object):
    def __init__(self, canvas, toolbar, ax, name):
        self.canvas = canvas
        self.toolbar = toolbar
        self.ax = ax
        self.name = name
        self.cid = None
        self.selected = None

    def enable(self):
        self.cid = self.canvas.mpl_connect('motion_notify_event', self)

    def disable(self):
        if self.cid:
            self.canvas.mpl_disconnect(self.cid)

    def setSelected(self, selected):
        #logger.debug("Enabling %s" % selected)
        self.selected = selected

    def __call__(self, event):
        if event.inaxes is None:
            return
        ax = self.ax


        #print " before event.x:%s, event.y:%s" % (event.x, event.y),

        if ax != event.inaxes:
            inv = ax.transData.inverted()
            x, y = inv.transform(np.array((event.x, event.y)).reshape(1, 2)).ravel()
        elif ax == event.inaxes:
            x, y = event.xdata, event.ydata
        else:
            return

        #print " after x:%s, y:%s" % (x, y),

        #if self.selected:
        xValue = matplotlib.dates.num2date(x).replace(tzinfo=None)

        #self.toolbar.msg.SetLabelText("X= %s,  Y= %.4f (%s)" % (xValue.strftime("%b %d, %Y %H:%M"), y, self.name))
        self.toolbar.msg.SetLabelText("X= %s,  Y= %.4f (%s)" % (xValue, y, self.name))
        self.toolbar.msg.SetForegroundColour((66, 66, 66))
        #logger.debug('{n}: ({x}, {y:0.2f})'.format(n=self.name, x=xValue.strftime("%Y-%m-%d %H:%M:%S"), y=y))
