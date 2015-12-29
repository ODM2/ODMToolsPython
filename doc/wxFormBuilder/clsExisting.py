# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun  5 2014)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class pnlExisting
###########################################################################

class pnlExisting ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.lblExisting = wx.StaticText( self, wx.ID_ANY, u"Select an Existing Series:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lblExisting.Wrap( -1 )
		bSizer1.Add( self.lblExisting, 0, wx.ALL, 5 )
		
		self.olvSeriesList = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_ICON )
		bSizer1.Add( self.olvSeriesList, 100, wx.ALL|wx.EXPAND, 5 )
		
		self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer1.Add( self.m_panel1, 1, wx.EXPAND |wx.ALL, 5 )
		
		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_panel3 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer6.Add( self.m_panel3, 10, wx.EXPAND |wx.ALL, 5 )
		
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		self.rbOverwrite = wx.RadioButton( self, wx.ID_ANY, u"Overwrite Entire Series", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.rbOverwrite, 0, wx.ALL, 5 )
		
		self.rbAppend = wx.RadioButton( self, wx.ID_ANY, u"Append To Series", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.rbAppend, 0, wx.ALL, 5 )
		
		bSizer5 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_panel2 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer5.Add( self.m_panel2, 10, wx.EXPAND |wx.ALL, 5 )
		
		bSizer3 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"If Data Overlaps:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		self.m_staticText2.Enable( False )
		
		bSizer3.Add( self.m_staticText2, 0, wx.ALL, 5 )
		
		self.rbNew = wx.RadioButton( self, wx.ID_ANY, u"Keep New", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.rbNew.Enable( False )
		
		bSizer3.Add( self.rbNew, 0, wx.ALL, 5 )
		
		self.rbOriginal = wx.RadioButton( self, wx.ID_ANY, u"Keep Original", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.rbOriginal.Enable( False )
		
		bSizer3.Add( self.rbOriginal, 0, wx.ALL, 5 )
		
		
		bSizer5.Add( bSizer3, 90, wx.EXPAND, 5 )
		
		
		bSizer2.Add( bSizer5, 1, wx.EXPAND, 5 )
		
		
		bSizer6.Add( bSizer2, 90, wx.EXPAND, 5 )
		
		
		bSizer1.Add( bSizer6, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		# Connect Events
		self.olvSeriesList.Bind( wx.EVT_LIST_ITEM_SELECTED, self.OnOLVItemSelected )
		self.rbOverwrite.Bind( wx.EVT_RADIOBUTTON, self.onOverwrite )
		self.rbAppend.Bind( wx.EVT_RADIOBUTTON, self.onAppend )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def OnOLVItemSelected( self, event ):
		event.Skip()
	
	def onOverwrite( self, event ):
		event.Skip()
	
	def onAppend( self, event ):
		event.Skip()
	

