import wx
import wx.wizard as wiz
from odmtools.view.clsWizSource import clsSource
from wx.lib.pubsub import pub as Publisher
from odmtools.controller.frmCreateSource import frmCreateSource




import logging
# tool = LoggerTool()
# logger = tool.setupLogger(__name__, __name__ + '.log', 'w', logging.DEBUG)
logger =logging.getLogger('main')

class pageSource(wiz.WizardPageSimple):
    def __init__(self, parent, title, service_manager, src):
        """Constructor"""
        wiz.WizardPageSimple.__init__(self, parent)

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = sizer
        self.SetSizer(sizer)
        series_service = service_manager.get_series_service()

        title = wx.StaticText(self, -1, title)
        title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        sizer.Add(title, 10, wx.ALIGN_CENTRE | wx.ALL, 5)
        sizer.Add(wx.StaticLine(self, -1), 5, wx.EXPAND | wx.ALL, 5)
        self.panel = pnlSource(self, id=wx.ID_ANY, title=u'pnlSource', service_manager=service_manager, src=src)
        self.sizer.Add(self.panel, 85, wx.ALL, 5)




        srcs = series_service.get_all_sources()
        index = 0
        for s, i in zip(srcs, range(len(srcs))):
            num_items = self.panel.lstSource.GetItemCount()
            self.panel.lstSource.InsertStringItem(num_items, str(s.organization))
            self.panel.lstSource.SetStringItem(num_items, 1, str(s.description))
            self.panel.lstSource.SetStringItem(num_items, 2, str(s.link))
            self.panel.lstSource.SetStringItem(num_items, 3, str(s.contact_name))
            self.panel.lstSource.SetStringItem(num_items, 4, str(s.phone))
            self.panel.lstSource.SetStringItem(num_items, 5, str(s.email))
            self.panel.lstSource.SetStringItem(num_items, 6, str(s.address))
            self.panel.lstSource.SetStringItem(num_items, 7, str(s.city))
            self.panel.lstSource.SetStringItem(num_items, 8, str(s.state))
            self.panel.lstSource.SetStringItem(num_items, 9, str(s.zip_code))
            self.panel.lstSource.SetStringItem(num_items, 10, str(s.citation))
            self.panel.lstSource.SetStringItem(num_items, 11, str(s.id))


            if s.organization == src.organization:
                index = i
        self.panel.lstSource.Focus(index)
        self.panel.lstSource.Select(index)



class pnlSource(clsSource):

    def __init__(self, parent, id, title, service_manager, src):

        clsSource.__init__(self, parent, id=id, name=title,
                           pos=wx.Point(536, 285), size=wx.Size(439, 357),
                           style=wx.TAB_TRAVERSAL)
        self.prev_val = src
        self.service_man= service_manager
        self.series_service = service_manager.get_series_service()

    def OnRbCurrentRadiobutton(self, event):
        self.lstSource.Enable(False)
        event.Skip()


    def OnRbSelectRadiobutton(self, event):
        self.lstSource.Enable(True)
        event.Skip()


    def OnRbCreateRadiobutton(self, event):
        self.lstSource.Enable(False)

        create_src = frmCreateSource(self, self.service_man, self.prev_val)
        returnVal = create_src.ShowModal()
        self.createdSrc = create_src.getSource()
        create_src.Destroy()

        # TODO if cancelled return to previous radio button
        # else enable text box and enter the text info.
        # get Variable object
        if returnVal == wx.ID_CANCEL:
            self.rbCurrent.SetValue(True)
        else:
            self.show_new_src(self.createdSrc)
        event.Skip()


    def OnListCtrl1ListItemSelected(self, event):
        event.Skip()


    def getSource(self):
        # s = Source()
        if self.rbCurrent.Value:
            s = self.prev_val
        elif self.rbSelect.Value:
            index = self.lstSource.GetFirstSelected()
            code = self.lstSource.GetItem(index, 11).GetText()
            logger.debug(code)
            s = self.series_service.get_src_by_id(code)
        elif self.rbCreate.Value:
            s = self.createdSrc
        return s


    def show_new_src(self, src):
        self.txtNewSrc.InsertStringItem(0, str(src.organization))
        self.txtNewSrc.SetStringItem(0, 1, str(src.description))
        self.txtNewSrc.SetStringItem(0, 2, str(src.contact_name))
        self.txtNewSrc.SetStringItem(0, 3, str(src.phone))
        self.txtNewSrc.SetStringItem(0, 4, str(src.email))
        self.txtNewSrc.SetStringItem(0, 5, str(src.address))
        self.txtNewSrc.SetStringItem(0, 6, str(src.city))
        self.txtNewSrc.SetStringItem(0, 7, str(src.state))
        self.txtNewSrc.SetStringItem(0, 8, str(src.zip_code))
        self.txtNewSrc.SetStringItem(0, 9, str(src.citation))
        self.txtNewSrc.SetStringItem(0, 10, str(src.iso_metadata_id))



        self.txtNewSrc.Focus(0)
        self.txtNewSrc.Select(0)
        self.txtNewSrc.Enable(True)
