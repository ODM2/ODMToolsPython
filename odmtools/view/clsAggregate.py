# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Sep 12 2010)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx

###########################################################################
## Class dlg_aggregate
###########################################################################

class dlg_aggregate ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Aggregate Function", pos = wx.DefaultPosition, size = wx.Size( 300,300 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.Size( 300,300 ), wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer1.SetMinSize( wx.Size( 300,300 ) ) 
		m_radioBox2Choices = [ u"Hourly", u"Daily", u"Monthly" ]
		self.m_radioBox2 = wx.RadioBox( self, wx.ID_ANY, u"Duration", wx.DefaultPosition, wx.DefaultSize, m_radioBox2Choices, 1, wx.RA_SPECIFY_COLS )
		self.m_radioBox2.SetSelection( 1 )
		bSizer1.Add( self.m_radioBox2, 0, wx.ALL, 5 )
		
		m_radioBox1Choices = [ u"Minimum", u"Maximum", u"Average", u"Sum" ]
		self.m_radioBox1 = wx.RadioBox( self, wx.ID_ANY, u"Function", wx.DefaultPosition, wx.DefaultSize, m_radioBox1Choices, 1, wx.RA_SPECIFY_COLS )
		self.m_radioBox1.SetSelection( 0 )
		bSizer1.Add( self.m_radioBox1, 0, wx.ALL, 5 )
		
		fgSizer1 = wx.FlexGridSizer( 2, 2, 0, 0 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.btn_ok = wx.Button( self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.Bind(wx.EVT_BUTTON, self.onOK, self.btn_ok)
		fgSizer1.Add( self.btn_ok, 0, wx.ALL, 5 )
		
		self.btn_cancel = wx.Button( self, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.Bind(wx.EVT_BUTTON, self.onCancel, self.btn_cancel)
		fgSizer1.Add( self.btn_cancel, 0, wx.ALL, 5 )
		
		bSizer1.Add( fgSizer1, 1, wx.EXPAND, 5 )
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		self.Centre( wx.BOTH )

	# Virtual Event handlers - Override in subclass
	def onOK(self, event):
		event.Skip()
	
	def onCancel(self, event):
		event.Skip()

	def __del__( self ):
		pass
	

