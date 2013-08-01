#Boa:Dialog:frmAddPoint

import wx
import wx.lib.buttons
import wx.grid
import wx.lib.mixins.gridlabelrenderer as glr
from wx.lib.pubsub import pub as Publisher
import datetime

def create(parent):
    return frmAddPoint(parent)

[wxID_FRMADDPOINT, wxID_FRMADDPOINTBTNCANCEL, wxID_FRMADDPOINTBTNSAVE, 
 wxID_FRMADDPOINTGRDDATAVALUES, wxID_FRMADDPOINTPNLMAIN, 
] = [wx.NewId() for _init_ctrls in range(5)]

class frmAddPoint(wx.Dialog):
    def _init_coll_boxSizer1_Items(self, parent):
      # generated method, don't edit

      parent.AddWindow(self.grdDataValues, 90, border=0, flag=wx.EXPAND)
      parent.AddSizer(self.boxSizer2, 10, border=0, flag=wx.EXPAND)

    def _init_coll_boxSizer2_Items(self, parent):
      # generated method, don't edit

      parent.AddWindow(self.pnlMain, 70, border=0, flag=0)
      parent.AddWindow(self.btnSave, 15, border=0, flag=0)
      parent.AddWindow(self.btnCancel, 15, border=0, flag=0)

    def _init_sizers(self):
      # generated method, don't edit
      self.boxSizer1 = wx.BoxSizer(orient=wx.VERTICAL)

      self.boxSizer2 = wx.BoxSizer(orient=wx.HORIZONTAL)

      self._init_coll_boxSizer1_Items(self.boxSizer1)
      self._init_coll_boxSizer2_Items(self.boxSizer2)

      self.SetSizer(self.boxSizer1)

    def _init_ctrls(self, prnt):
      # generated method, don't edit
      wx.Dialog.__init__(self, id=wxID_FRMADDPOINT, name=u'frmAddPoint',
            parent=prnt, pos=wx.Point(573, 334), size=wx.Size(661, 277),
            style=wx.DEFAULT_DIALOG_STYLE, title=u'Add Point(s)')
      self.SetClientSize(wx.Size(645, 239))
      self.SetToolTipString(u'Dialog1')

      self.grdDataValues = MyGrid(id=wxID_FRMADDPOINTGRDDATAVALUES,
            name=u'grdDataValues', parent=self, pos=wx.Point(0, 0),
            size=wx.Size(645, 215), style=0)



      self.grdDataValues.SetLabel(u'grdDataValue')
      self.grdDataValues.SetToolTipString(u'Add Value')

      self.grdDataValues.SetRowLabelSize(20)
      self.grdDataValues.Bind(wx.grid.EVT_GRID_SELECT_CELL,
            self.OnGrdDataValuesGridSelectCell)

      self.grdDataValues.GetGridWindow().Bind(wx.EVT_MOTION, self.onMouseOver)
      # put a tooltip on a column label
      self.grdDataValues.GetGridColLabelWindow().Bind(wx.EVT_MOTION, 
                                             self.onMouseOverColLabel)
      

      self.pnlMain = wx.Panel(id=wxID_FRMADDPOINTPNLMAIN, name=u'pnlMain',
            parent=self, pos=wx.Point(0, 215), size=wx.Size(451, 29),
            style=wx.TAB_TRAVERSAL)

      self.btnSave = wx.Button(id=wxID_FRMADDPOINTBTNSAVE, label=u'Save',
            name=u'btnSave', parent=self, pos=wx.Point(451, 215),
            size=wx.Size(97, 23), style=0)
      self.btnSave.Bind(wx.EVT_BUTTON, self.OnBtnSaveButton,
            id=wxID_FRMADDPOINTBTNSAVE)

      self.btnCancel = wx.Button(id=wxID_FRMADDPOINTBTNCANCEL,
            label=u'Cancel', name=u'btnCancel', parent=self, pos=wx.Point(548,
            215), size=wx.Size(97, 23), style=0)
      self.btnCancel.Bind(wx.EVT_BUTTON, self.OnBtnCancelButton,
            id=wxID_FRMADDPOINTBTNCANCEL)

      self._init_sizers()

    def _init_table(self, series=None):
      self.grdDataValues.CreateGrid(1,10)
      # self.Service = Publisher.sendMessage(("GetDBService"), None)
      service_manager =self.parent.parent.GetDBService()
      # print DBConn
      self.service = service_manager.get_cv_service()

      self.otchoices = {x.description: x.id for x in self.service.get_offset_type_cvs()}
      self.ot_choice_editor = wx.grid.GridCellChoiceEditor(["<None>"] + self.otchoices.keys(), False)
      self.grdDataValues.SetCellEditor(0, 6, self.ot_choice_editor)

      ccchoices= list(x.term for x in self.service.get_censor_code_cvs())
      self.cc_choice_editor = wx.grid.GridCellChoiceEditor(ccchoices, False)
      self.grdDataValues.SetCellEditor(0, 7, self.cc_choice_editor)

      # qualchoices

      
      self.qualchoices = {x.code: x.id for x in self.service.get_qualifiers()}
      self.qual_choice_editor= wx.grid.GridCellChoiceEditor(["<None>"]+self.qualchoices.keys()+ ["<Create New...>"], False)

      self.grdDataValues.SetCellEditor(0, 8, self.qual_choice_editor)

      self.sampchoices = {x.lab_sample_code: x.id for x in self.service.get_samples()}
      self.samp_choice_editor= wx.grid.GridCellChoiceEditor(["<None>"] + self.sampchoices.keys(), False)
      self.grdDataValues.SetCellEditor(0, 9, self.samp_choice_editor)

      self.grdDataValues.Font.Weight = wx.LIGHT
      
      
      #HydroDesktop :
        # DataValue, req
        # ValueAccuracy, 
        # LocalDateTime, req
        # UTCOffset, req
        # DateTimeUTC, req
        # OffsetValue,
        # CensorCode, dd
        # OffsetType, dd
        # Qualifier, dd
        # Sample  dd


      # color = self.grdDataValues.GetLabelBackgroundColour()
      color= "Yellow"
      self.grdDataValues.SetColLabelValue(0, "DataValue")#Bold
      self.grdDataValues.SetColLabelRenderer(0, MyColLabelRenderer(color))
      self.grdDataValues.SetColLabelValue(1, "ValueAccuracy")
      self.grdDataValues.SetColLabelValue(2, "LocalDateTime")#Bold
      self.grdDataValues.SetColLabelRenderer(2, MyColLabelRenderer(color))
      self.grdDataValues.SetColLabelValue(3, "UTCOffset")#Bold
      self.grdDataValues.SetColLabelRenderer(3, MyColLabelRenderer(color))
      self.grdDataValues.SetColLabelValue(4, "DateTimeUTC")#Bold
      self.grdDataValues.SetColLabelRenderer(4, MyColLabelRenderer(color))
      self.grdDataValues.SetColLabelValue(5, "OffsetValue")
      self.grdDataValues.SetColLabelValue(6, "OffsetType")#DropDown
      self.grdDataValues.SetColLabelValue(7, "CensorCode")#Bold
      self.grdDataValues.SetColLabelRenderer(7, MyColLabelRenderer(color))#9
      self.grdDataValues.SetColLabelValue(8, "QualifierCode")#DropDown      
      self.grdDataValues.SetColLabelValue(9, "LabSampleCode")
     

      self.grdDataValues.AutoSizeColumns()

    def __init__(self, parent, record_service):
      self.parent = parent
      self.record_service = record_service
      self._init_ctrls(parent)
      self._init_table()

    def onMouseOver(self, event):
      
      # Use CalcUnscrolledPosition() to get the mouse position within the 
      # entire grid including what's offscreen
      # This method was suggested by none other than Robin Dunn
      x, y = self.grdDataValues.CalcUnscrolledPosition(event.GetX(),event.GetY())
      coords = self.grdDataValues.XYToCell(x, y)
      col = coords[1]
      row = coords[0]

      # Note: This only sets the tooltip for the cells in the column
      if col == 1:
          msg = "This is Row %s, Column %s!" % (row, col)
          event.GetEventObject().SetToolTipString(msg)
      else:
          event.GetEventObject().SetToolTipString('')
      event.Skip()
 
    #----------------------------------------------------------------------
    def onMouseOverColLabel(self, event):
      ##Displays a tooltip when mousing over certain column labels

      x = event.GetX()
      y = event.GetY()
      ##not accurate becasue of scrolling
      col = self.grdDataValues.XToCol(x, y)
      tip =""

      if col == 0 or col == 1 or col == 3 or col == 5 :
          tip = "Decimal"
      elif col == 2 or col == 4:
          tip = "mm/dd/yyyy h:mm:ss am"
      elif col == 6 or col == 7 or col == 8 or col == 9:
          tip = "Controlled Vocabulary"        
      else:
          tip = "None"
      self.grdDataValues.GetGridColLabelWindow().SetToolTipString(tip)
      event.Skip()

    def OnBtnSaveButton(self, event):
      # for row in self.grdDataValues
      num_rows = self.grdDataValues.GetNumberRows()
      num_cols = self.grdDataValues.GetNumberCols()
      datetime_format = "%m/%d/%Y %I:%M:%S %p"
      
      series = self.record_service.get_series()

      # check if the final row is formatted correctly
      if not self.IsRowFilled(num_rows - 1):
        # TODO: Implement error messages and highlight correct cell. For now, do nothing
        event.Skip()
        return

      points = []
      for r in range(num_rows):
        row = []
        for c in range(num_cols):
          row.append(self.grdDataValues.GetCellValue(r, c))
        # convert date fields to datetime objects
        row[2] = datetime.datetime.strptime(row[2], datetime_format)
        row[4] = datetime.datetime.strptime(row[4], datetime_format)
        if (row[6]): row[6] = self.otchoices[row[6]]
        if (row[8]): row[8] = self.qualchoices[row[8]]
        if (row[9]): row[9] = self.sampchoices[row[9]]

        # add other information for this series
        row.append(series.site_id)
        row.append(series.variable_id)
        row.append(series.method_id)
        row.append(series.source_id)
        row.append(series.quality_control_level_id)

        points.append(tuple(row))

      self.record_service.add_points(points)
      event.Skip()
      self.Close()

    def OnBtnCancelButton(self, event):
      self.Close()
      event.Skip()

    def OnGrdDataValuesGridSelectCell(self, event):
        
      # print "sel Cell"#, dir(event)
      # print event.Col, event.Row
      # print self.grdDataValues.GetNumberRows()


      #if last row AND and all req cells from previous row are filled out
      if event.Row == self.grdDataValues.GetNumberRows()-1 and self.IsRowFilled(event.Row):
        # TODO Test that all yellow boxes of previous row are filled first
        self.grdDataValues.AppendRows(numRows= 1) 
        ##format all of the cells with drop down boxes and fill in 5 identifiers  

        self.grdDataValues.SetCellEditor(self.grdDataValues.GetNumberRows()-1, 6, self.ot_choice_editor)     
        self.grdDataValues.SetCellEditor(self.grdDataValues.GetNumberRows()-1, 7, self.cc_choice_editor)
        self.grdDataValues.SetCellEditor(self.grdDataValues.GetNumberRows()-1, 8, self.qual_choice_editor)
        self.grdDataValues.SetCellEditor(self.grdDataValues.GetNumberRows()-1, 9, self.samp_choice_editor)

      
      event.Skip()

    def IsRowFilled(self, row):
      val = False
      datetime_format = "%m/%d/%Y %I:%M:%S %p"

      if (self.grdDataValues.GetCellValue(row, 0) != "" and   # Data Value
          self.grdDataValues.GetCellValue(row, 2) != "" and   # LocalDatetime
          self.grdDataValues.GetCellValue(row, 3) != "" and   # UTC Offset
          self.grdDataValues.GetCellValue(row, 4) != "" and   # UTCDateTime
          self.grdDataValues.GetCellValue(row, 7) != ""):     # Censor Code
        # Test date formats
        try:
          local_datetime = self.grdDataValues.GetCellValue(row, 2)
          utc_datetime = self.grdDataValues.GetCellValue(row, 4)

          print local_datetime
          print utc_datetime

          datetime.datetime.strptime(local_datetime, datetime_format)
          datetime.datetime.strptime(utc_datetime, datetime_format)

          # If no exceptions were thrown, both dates are in the correct format
          val = True
        except ValueError as err:
          # Do nothing, the return value will stay false
          print err

      return val

class MyColLabelRenderer(glr.GridLabelRenderer):
  def __init__(self, bgcolor):
    self._bgcolor = bgcolor 
      
  def Draw(self, grid, dc, rect, col):
    dc.SetBrush(wx.Brush(self._bgcolor))
    dc.SetPen(wx.TRANSPARENT_PEN)
    dc.DrawRectangleRect(rect)
    hAlign, vAlign = grid.GetColLabelAlignment()
    text = grid.GetColLabelValue(col)
    self.DrawBorder(grid, dc, rect)
    dc.Font.Weight = wx.BOLD
    # dc.Font.PointSize = 18
    self.DrawText(grid, dc, rect, text, hAlign, vAlign)

class MyGrid(wx.grid.Grid, glr.GridWithLabelRenderersMixin):
  def __init__(self, *args, **kw):
    wx.grid.Grid.__init__(self, *args, **kw)
    glr.GridWithLabelRenderersMixin.__init__(self)


