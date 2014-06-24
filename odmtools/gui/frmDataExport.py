import os
import wx
from wx.lib.pubsub import pub as Publisher
from odmservices import ServiceManager

def create(parent):
	return frmDataExport(parent)

[wxID_FRMDATAEXPORT, wxID_FRMDATAEXPORTBTNOK, wxID_FRMDATAEXPORTBTNCANCEL, 
 wxID_FRMDATAEXPORTCHKUTC, wxID_FRMDATAEXPORTCHKSITE, wxID_FRMDATAEXPORTCHKVAR,
 wxID_FRMDATAEXPORTCHKOFFSET, wxID_FRMDATAEXPORTCHKQUAL, wxID_FRMDATAEXPORTCHKSRC,
 wxID_FRMDATAEXPORTCHKQCL, wxID_FRMDATAEXPORTPANEL
] = [wx.NewId() for _init_ctrls in range(11)]

class frmDataExport(wx.Dialog):
	def _init_ctrls(self, prnt):

		wx.Dialog.__init__(self, id=wxID_FRMDATAEXPORT, name=u'frmDataExport',
			parent=prnt, pos=wx.Point(599, 384), size=wx.Size(250, 300),
			style=wx.DEFAULT_DIALOG_STYLE, title=u'Data Export for Series %s' % self.series_id)
		self.SetClientSize(wx.Size(225, 275))
		self.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL, False, u'MS Shell Dlg 2'))

		self.panel = wx.Panel(id=wxID_FRMDATAEXPORTPANEL, name='panel',
			parent=self, pos=wx.Point(0,0), size=wx.Size(225, 275),
			style=wx.TAB_TRAVERSAL)

		self.chkUTC = wx.CheckBox(id=wxID_FRMDATAEXPORTCHKUTC,
			name=u'checkboxUTC', label='Include UTC data',
			parent=self.panel, pos=wx.Point(8, 20),
			size=wx.Size(200,25), style=0)

		self.chkSite = wx.CheckBox(id=wxID_FRMDATAEXPORTCHKSITE,
			name=u'checkboxSite', label='Include Site data',
			parent=self.panel, pos=wx.Point(8, 45),
			size=wx.Size(200,25), style=0)

		self.chkVar = wx.CheckBox(id=wxID_FRMDATAEXPORTCHKVAR,
			name=u'checkboxVar', label='Include Variable data',
			parent=self.panel, pos=wx.Point(8, 70),
			size=wx.Size(200,25), style=0)

		self.chkOffset = wx.CheckBox(id=wxID_FRMDATAEXPORTCHKOFFSET,
			name=u'checkboxOffset', label='Include Offset data',
			parent=self.panel, pos=wx.Point(8, 95),
			size=wx.Size(200,25), style=0)

		self.chkQual = wx.CheckBox(id=wxID_FRMDATAEXPORTCHKQUAL,
			name=u'checkboxQual', label='Include Qualifier data',
			parent=self.panel, pos=wx.Point(8, 120),
			size=wx.Size(200,25), style=0)
		
		self.chkSrc = wx.CheckBox(id=wxID_FRMDATAEXPORTCHKSRC,
			name=u'checkboxSrc', label='Include Source data',
			parent=self.panel, pos=wx.Point(8, 145),
			size=wx.Size(200,25), style=0)

		self.chkQcl = wx.CheckBox(id=wxID_FRMDATAEXPORTCHKQCL,
			name=u'checkboxQcl', label='Include Quality Control Level data',
			parent=self.panel, pos=wx.Point(8, 170),
			size=wx.Size(200,25), style=0)


		self.btnOK = wx.Button(id=wxID_FRMDATAEXPORTBTNOK, label=u'OK',
			name=u'btnOK', parent=self.panel, pos=wx.Point(8, 230),
			size=wx.Size(48, 23), style=0)
		self.btnOK.Bind(wx.EVT_BUTTON, self.OnBtnOKButton,
			id=wxID_FRMDATAEXPORTBTNOK)

		self.btnCancel = wx.Button(id=wxID_FRMDATAEXPORTBTNCANCEL, label=u'Cancel',
			name=u'btnCancel', parent=self.panel, pos=wx.Point(64, 230),
			size=wx.Size(48, 23), style=0)
		self.btnCancel.Bind(wx.EVT_BUTTON, self.OnBtnCancelButton,
			id=wxID_FRMDATAEXPORTBTNCANCEL)


	def __init__(self, parent, series_id):
		self.series_id = series_id
		self._init_ctrls(parent)

		sm = ServiceManager()
		self.export_service = sm.get_export_service()


	def OnBtnOKButton(self, event):
		utc    = self.chkUTC.GetValue()
		site   = self.chkSite.GetValue()
		var    = self.chkVar.GetValue()
		offset = self.chkOffset.GetValue()
		qual   = self.chkQual.GetValue()
		src    = self.chkSrc.GetValue()
		qcl    = self.chkQcl.GetValue()

		dlg = wx.FileDialog(self, "Choose a save location", '', "", "*.csv", wx.SAVE | wx.OVERWRITE_PROMPT)
		if dlg.ShowModal() == wx.ID_OK:
			full_path = os.path.join(dlg.GetDirectory(), dlg.GetFilename())
			print full_path

			self.export_service.export_series_data(self.series_id, full_path, utc, site, var, offset, qual, src, qcl)
			self.Close()

		dlg.Destroy()

	def OnBtnCancelButton(self, event):
		self.Close()