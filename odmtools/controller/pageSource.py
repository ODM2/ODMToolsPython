import wx
import wx.wizard as wiz
from odmtools.view.clsSource import pnlSource
from wx.lib.pubsub import pub as Publisher




import logging
# tool = LoggerTool()
# logger = tool.setupLogger(__name__, __name__ + '.log', 'w', logging.DEBUG)
logger =logging.getLogger('main')

class pageSource:
    def __init__(self, parent, id, pos, size, style, name, sm, src):
        pnlSource.__init__(self,parent,id,pos,sixe,style,name)
        self.prev_src = src
        self.service_man = sm
        self.series_service = sm.get_series_service()


        self.SetClientSize(wx.Size(423, 319))


    def OnRbCurrentRadiobutton(self, event):
        self.lstSource.Enable(False)
        self.txtNewVar.Enable(False)

        event.Skip()


    def OnRbSelectRadiobutton(self, event):
        self.lstSource.Enable(True)
        self.txtNewVar.Enable(False)

        event.Skip()


    def OnRbCreateRadiobutton(self, event):
        self.lstSource.Enable(False)

        create_src = frmCreateSource(self, self.service_man, self.prev_src)
        returnVal = create_src.ShowModal()
        self.createdSrc = create_Src.getSource()
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
        s = Source()
        if self.rbCurrent.Value:
            v = self.prev_src
        elif self.rbSelect.Value:
            index = self.lstSource.GetFirstSelected()
            code = self.lstSource.GetItem(index, 0).GetText()
            logger.debug(code)
            v = self.series_service.get_variable_by_code(code)
        elif self.rbCreate.Value:
            v = self.createdSrc
        return v


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
        self.txtNewSrc.SetStringItem(0, 10, str(src.metadata_id))

        self.txtNewSrc.Focus(0)
        self.txtNewSrc.Select(0)
        self.txtNewSrc.Enable(True)
