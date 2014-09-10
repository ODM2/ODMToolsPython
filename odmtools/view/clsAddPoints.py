# -*- coding: utf-8 -*- 

# ##########################################################################
# # Python code generated with wxFormBuilder (version Jun  5 2014)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################
from collections import OrderedDict

import wx
import wx.xrc
from ObjectListView import FastObjectListView as objectListView, ColumnDefn

from odmtools.common.icons.icons import add, stop_edit, deletered

###########################################################################
## Class AddPoints
###########################################################################

class AddPoints(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString,
                           pos=wx.DefaultPosition, size=wx.Size(1400, 300),
                           style=wx.DEFAULT_DIALOG_STYLE | wx.CLOSE_BOX | wx.RESIZE_BORDER)

        self.m_toolBar1 = wx.ToolBar(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL)
        self.addTool = self.m_toolBar1.AddSimpleTool(wx.ID_ANY, add.GetBitmap(), u"Add Points")
        self.closeTool = self.m_toolBar1.AddSimpleTool(wx.ID_ANY, stop_edit.GetBitmap(), u"Close", )
        #
        # self.m_tool3 = self.m_toolBar1.AddLabelTool(wx.ID_ANY, u"tool", wx.NullBitmap, wx.NullBitmap, wx.ITEM_NORMAL,
        #                                             wx.EmptyString, wx.EmptyString, None)
        #
        # self.m_tool4 = self.m_toolBar1.AddLabelTool(wx.ID_ANY, u"tool", wx.NullBitmap, wx.NullBitmap, wx.ITEM_NORMAL,
        #                                             wx.EmptyString, wx.EmptyString, None)

        self.m_toolBar1.Realize()

        self.olv = objectListView(self, wx.ID_ANY, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.olv.useAlternateBackColors = True
        self.olv.cellEditMode = objectListView.CELLEDIT_DOUBLECLICK

        self.olv.SetEmptyListMsg("Add points either by csv or manually")
        #self.olv.AddNamedImages("delete", deletered.GetBitmap())
        self.buildOlv()
        self.olv.CreateCheckStateColumn()
        self.olv.SetObjects([Points('1'), Points('2'), Points('3'), Points('4')])

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        olvSizer = wx.BoxSizer(wx.HORIZONTAL)
        olvSizer.Add(self.olv, 1, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 5)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(olvSizer, 1, wx.EXPAND, 5)
        mainSizer.Add(self.m_toolBar1, 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(mainSizer)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.Bind(wx.EVT_TOOL, self.onClickAdd, id=self.addTool.GetId())
        self.Bind(wx.EVT_TOOL, self.onClose, id=self.closeTool.GetId())
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onSelected, id=self.olv.GetId())

    def __del__(self):
        pass

    def imageGetter(self, model):
        return "delete"

    def buildOlv(self):
        keys = ['DataValue', 'ValueAccuracy', 'LocalDateTime', 'UTCOffset', 'DateTimeUTC',
                'OffsetValue', 'OffsetType', 'CensorCode', 'QualifierCode', 'LabSampleCode']
        values = ['dataValue', 'valueAccuracy', 'localDateTime', 'utcOffSet', 'dateTimeUTC',
                  'offSetValue', 'offSetType', 'censorCode', 'qualifierCode', 'labSampleCode']
        elements = OrderedDict(zip(keys, values))
        self.olv.SetColumns([ColumnDefn(key, align='left', minimumWidth=125,
                                        valueGetter=value)
                                        #imageGetter=(self.imageGetter if key == '' else None)
                             for key, value in elements.iteritems()]
        )

    # Virtual event handlers, override them in your derived class
    def onClickAdd(self, event):
        event.Skip()

    def onClose(self, event):
        event.Skip()

    def onSelected(self, event):
        event.Skip()

class Points(object):
    def __init__(self, dataValue=None, valueAccuracy=None, localDateTime=None, utcOffSet=None,
                 dateTimeUTC=None, offSetValue=None, offSetType=None, censorCode=None,
                 qualifierCode=None, labSampleCode=None):
        self.dataValue = dataValue
        self.valueAccuracy = valueAccuracy
        self.localDateTime = localDateTime
        self.utcOffSet = utcOffSet
        self.dateTimeUTC = dateTimeUTC
        self.offSetValue = offSetValue
        self.offSetType = offSetType
        self.censorCode = censorCode
        self.qualiferCode = qualifierCode
        self.labSampleCode = labSampleCode
