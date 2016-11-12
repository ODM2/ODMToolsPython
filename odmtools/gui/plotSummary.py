# Boa:FramePanel:plotSummary

import wx
import wx.grid
from wx.lib.wordwrap import wordwrap
import os
#import pandas as pd

[wxID_PLOTSUMMARY, wxID_PLOTSUMMARYGRDSUMMARY,
] = [wx.NewId() for _init_ctrls in range(2)]

import logging
# from odmtools.common.logger import LoggerTool
#
# tool = LoggerTool()
# logger = tool.setupLogger(__name__, __name__ + '.log', 'w', logging.DEBUG)
logger =logging.getLogger('main')

class plotSummary(wx.Panel):
    def __init__(self, parent, id, pos, size, style, name):
        self._init_ctrls(parent)

    def _init_coll_boxSizer1_Items(self, parent):
        # generated method, don't edit
        parent.Add(self.btnExport, 0, border=5)
        parent.AddWindow(self.grdSummary, 1, border=5, flag=wx.EXPAND | wx.GROW)


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

        self.btnExport = wx.Button(self, wx.ID_ANY, u"Export Statistics", wx.DefaultPosition, wx.DefaultSize, 0)
        self.btnExport.Enable(False)
        self.btnExport.Bind(wx.EVT_BUTTON, self.onBtnExport)
        self.grdSummary.Bind(wx.grid.EVT_GRID_COL_SIZE, self.onListColEndDrag)

        self.initPlot()
        self._init_sizers()

    def onBtnExport(self, event):

        dlg = wx.FileDialog(self, "Choose a save location", '', "", "*.csv", wx.SAVE | wx.OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            full_path = os.path.join(dlg.GetDirectory(), dlg.GetFilename())
            print full_path

            import csv

            ex_file = open(full_path, 'w')
            ex_writer = csv.writer(ex_file)

            #self.grdSummary
            titles = [u'Name'] + [self.grdSummary.GetRowLabelValue(x) for x in xrange(self.grdSummary.GetNumberRows())]
            data = []
            for c in xrange(self.grdSummary.GetNumberCols()):
                row = []
                row.append(self.grdSummary.GetColLabelValue(c).replace('\n', ' '))
                for r in xrange(self.grdSummary.GetNumberRows()):
                    row.append(self.grdSummary.GetCellValue(r, c).replace('\n', ' '))

                data.append(row)

            vals = [titles] + data

            ex_writer.writerows(vals)
            ex_file.close()

    def onListColEndDrag(self, event):
        col = event.GetRowOrCol()
        label = ' '.join(self.grdSummary.GetColLabelValue(col).split())
        self.setColLabel(col, label)
        event.Skip()

    def Plot(self, seriesPlotInfo):
        self.clear()
        for oneSeries in seriesPlotInfo.getAllSeries():
            if len(oneSeries.dataTable) > 0:
                if not self.btnExport.IsEnabled():
                    self.btnExport.Enable(True)
                self.addCol(oneSeries)

    def resizeLabel(self):
        numlines = -99
        #get the maximum number of lines
        for col in range(self.grdSummary.GetNumberCols()):
            val = self.grdSummary.GetColLabelValue(col).count('\n') + 1
            if val > numlines:
                numlines = val

        self.grdSummary.ColLabelSize = numlines * 16  #(16 is the number of pixels per line)

    def clear(self):
        self.btnExport.Enable(False)
        if self.grdSummary.GetNumberCols() > 0:
            # for columns in range(self.grdSummary.GetNumberCols())
            self.grdSummary.DeleteCols(pos=0, numCols=self.grdSummary.GetNumberCols(), updateLabels=True)


    def setColLabel(self, col, label):
        self.grdSummary.SetColLabelValue(col, wordwrap(label,
                                                       self.grdSummary.GetColSize(col), wx.ClientDC(self),
                                                       breakLongWords=False))
        self.resizeLabel()

    def initPlot(self):
        #self.grdSummary.AutoSize()
        self.grdSummary.CreateGrid(15, 0)

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

        #self.grdSummary.ColLabelSize=160


    def addCol(self, series):

        self.grdSummary.AppendCols(numCols=1, updateLabels=True)
        col = self.grdSummary.GetNumberCols() - 1
        self.setColLabel(col, series.siteName + "- " + series.variableName)
        #self.grdSummary.AutoSizeColLabelSize(columns)

        stats = series.Statistics
        count = stats.NumberofObservations
        self.grdSummary.SetCellValue(0, col, repr(series.seriesID))
        self.grdSummary.SetCellValue(1, col, repr(count))
        self.grdSummary.SetCellValue(2, col, repr(stats.NumberofCensoredObservations))
        self.grdSummary.SetCellValue(3, col, repr(stats.ArithemticMean))

        if count > 0:
            self.grdSummary.SetCellValue(4, col, repr(stats.GeometricMean))
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
        for i in range(self.grdSummary.GetNumberRows()):
            self.grdSummary.SetCellAlignment(i, col, wx.ALIGN_RIGHT, wx.ALIGN_CENTER)