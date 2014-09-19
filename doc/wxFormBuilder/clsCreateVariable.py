# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Feb 26 2014)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class clsCreateVariable
###########################################################################

class clsCreateVariable ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 553,388 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		fgSizer11 = wx.FlexGridSizer( 0, 1, 0, 0 )
		fgSizer11.SetFlexibleDirection( wx.VERTICAL )
		fgSizer11.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		fgSizer1 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer1.SetFlexibleDirection( wx.HORIZONTAL )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_NONE )
		
		self.stCode = wx.StaticText( self, wx.ID_ANY, u"Code:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.stCode.Wrap( -1 )
		fgSizer1.Add( self.stCode, 0, wx.ALIGN_RIGHT|wx.ALL|wx.EXPAND, 5 )
		
		self.txtVarCode = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.txtVarCode, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.stName = wx.StaticText( self, wx.ID_ANY, u"Name:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.stName.Wrap( -1 )
		fgSizer1.Add( self.stName, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		cbVarNameChoices = []
		self.cbVarName = wx.ComboBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, cbVarNameChoices, wx.CB_READONLY )
		fgSizer1.Add( self.cbVarName, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.stUnits = wx.StaticText( self, wx.ID_ANY, u"Units:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.stUnits.Wrap( -1 )
		fgSizer1.Add( self.stUnits, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		fgSizer4 = wx.FlexGridSizer( 0, 4, 0, 0 )
		fgSizer4.SetFlexibleDirection( wx.VERTICAL )
		fgSizer4.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		cbVarUnitsChoices = []
		self.cbVarUnits = wx.ComboBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, cbVarUnitsChoices, wx.CB_READONLY )
		fgSizer4.Add( self.cbVarUnits, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.stSpeciation = wx.StaticText( self, wx.ID_ANY, u"Speciation:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.stSpeciation.Wrap( -1 )
		fgSizer4.Add( self.stSpeciation, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		cbSpeciationChoices = []
		self.cbSpeciation = wx.ComboBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, cbSpeciationChoices, wx.CB_READONLY )
		fgSizer4.Add( self.cbSpeciation, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		fgSizer1.Add( fgSizer4, 1, wx.EXPAND, 5 )
		
		
		fgSizer11.Add( fgSizer1, 1, wx.ALL|wx.EXPAND, 5 )
		
		sbSizer3 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Time Support" ), wx.HORIZONTAL )
		
		fgSizer3 = wx.FlexGridSizer( 0, 4, 0, 0 )
		fgSizer3.SetFlexibleDirection( wx.HORIZONTAL )
		fgSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.stValue = wx.StaticText( self, wx.ID_ANY, u"Value:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.stValue.Wrap( -1 )
		fgSizer3.Add( self.stValue, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		self.txtTSValue = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer3.Add( self.txtTSValue, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.stTSUnits = wx.StaticText( self, wx.ID_ANY, u"Units:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.stTSUnits.Wrap( -1 )
		fgSizer3.Add( self.stTSUnits, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		cbTSUnitsChoices = []
		self.cbTSUnits = wx.ComboBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, cbTSUnitsChoices, wx.CB_DROPDOWN|wx.CB_READONLY )
		fgSizer3.Add( self.cbTSUnits, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		sbSizer3.Add( fgSizer3, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		fgSizer11.Add( sbSizer3, 1, wx.ALL|wx.EXPAND|wx.LEFT, 10 )
		
		fgSizer6 = wx.FlexGridSizer( 0, 4, 0, 0 )
		fgSizer6.SetFlexibleDirection( wx.BOTH )
		fgSizer6.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.stValType = wx.StaticText( self, wx.ID_ANY, u"Value Type:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.stValType.Wrap( -1 )
		fgSizer6.Add( self.stValType, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		cbValueTypeChoices = []
		self.cbValueType = wx.ComboBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, cbValueTypeChoices, wx.CB_READONLY )
		fgSizer6.Add( self.cbValueType, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.stDataType = wx.StaticText( self, wx.ID_ANY, u"Data Type:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.stDataType.Wrap( -1 )
		fgSizer6.Add( self.stDataType, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		cbDataTypeChoices = []
		self.cbDataType = wx.ComboBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, cbDataTypeChoices, wx.CB_READONLY )
		fgSizer6.Add( self.cbDataType, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.stGenCat = wx.StaticText( self, wx.ID_ANY, u"General Category:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.stGenCat.Wrap( -1 )
		fgSizer6.Add( self.stGenCat, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		self.txtGenCat = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer6.Add( self.txtGenCat, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.stNoDV = wx.StaticText( self, wx.ID_ANY, u"NoDataValue:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.stNoDV.Wrap( -1 )
		fgSizer6.Add( self.stNoDV, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		self.txtNoDV = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer6.Add( self.txtNoDV, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.stSampMed = wx.StaticText( self, wx.ID_ANY, u"Sample Medium:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.stSampMed.Wrap( -1 )
		fgSizer6.Add( self.stSampMed, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		cbSampleMediumChoices = []
		self.cbSampleMedium = wx.ComboBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, cbSampleMediumChoices, wx.CB_READONLY )
		fgSizer6.Add( self.cbSampleMedium, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.stReg = wx.StaticText( self, wx.ID_ANY, u"Is Regular:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.stReg.Wrap( -1 )
		fgSizer6.Add( self.stReg, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		self.cbIsRegular = wx.CheckBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer6.Add( self.cbIsRegular, 0, wx.ALL, 5 )
		
		
		fgSizer11.Add( fgSizer6, 1, wx.ALL|wx.EXPAND, 5 )
		
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_panel2 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer2.Add( self.m_panel2, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.btnCreate = wx.Button( self, wx.ID_ANY, u"Create", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.btnCreate, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		self.btnCancel = wx.Button( self, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.btnCancel, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		
		fgSizer11.Add( bSizer2, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.SetSizer( fgSizer11 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.btnCreate.Bind( wx.EVT_BUTTON, self.OnBtnCreateButton )
		self.btnCancel.Bind( wx.EVT_BUTTON, self.OnBtnCancelButton )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def OnBtnCreateButton( self, event ):
		event.Skip()
	
	def OnBtnCancelButton( self, event ):
		event.Skip()
	

