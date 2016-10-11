# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class dlgFill
###########################################################################

class dlgFill ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 315,174 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.Size( 315,174 ), wx.Size( 315,174 ) )
		
		bsForm = wx.BoxSizer( wx.VERTICAL )
		
		bsGap = wx.BoxSizer( wx.HORIZONTAL )
		
		self.lblGap = wx.StaticText( self, wx.ID_ANY, u"Gap", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lblGap.Wrap( -1 )
		bsGap.Add( self.lblGap, 0, wx.ALL, 5 )
		
		self.txtGap = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bsGap.Add( self.txtGap, 0, wx.ALL, 5 )
		
		cbGapChoices = [ u"second", u"minute", u"hour", u"days", u"week", u"month", u"day", u"year", wx.EmptyString, wx.EmptyString, wx.EmptyString ]
		self.cbGap = wx.ComboBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, cbGapChoices, 0 )
		self.cbGap.SetSelection( 1 )
		bsGap.Add( self.cbGap, 1, wx.ALL, 5 )
		
		
		bsForm.Add( bsGap, 1, wx.EXPAND, 5 )
		
		bsFill = wx.BoxSizer( wx.HORIZONTAL )
		
		self.lblFill = wx.StaticText( self, wx.ID_ANY, u"Fill", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lblFill.Wrap( -1 )
		bsFill.Add( self.lblFill, 0, wx.ALL, 5 )
		
		self.txtFill = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bsFill.Add( self.txtFill, 0, wx.ALL, 5 )
		
		cbFillChoices = [ u"second", u"minute", u"hour", u"day", u"week", u"month", u"year" ]
		self.cbFill = wx.ComboBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, cbFillChoices, 0 )
		self.cbFill.SetSelection( 1 )
		bsFill.Add( self.cbFill, 1, wx.ALL, 5 )
		
		
		bsForm.Add( bsFill, 1, wx.EXPAND, 5 )
		
		bsButtons = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bsButtons.Add( self.m_panel1, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.btnOK = wx.Button( self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btnOK.SetDefault() 
		bsButtons.Add( self.btnOK, 0, wx.ALL, 5 )
		
		self.btnCancel = wx.Button( self, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
		bsButtons.Add( self.btnCancel, 0, wx.ALL, 5 )
		
		
		bsForm.Add( bsButtons, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bsForm )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.btnOK.Bind( wx.EVT_BUTTON, self.onOKBtn )
		self.btnCancel.Bind( wx.EVT_BUTTON, self.OnCancelBtn )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onOKBtn( self, event ):
		event.Skip()
	
	def OnCancelBtn( self, event ):
		event.Skip()
	

