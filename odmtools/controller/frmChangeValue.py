import wx
from odmtools.view.clsChangeValue import clsChangeValue
__author__ = 'jmeline'

class frmChangeValue(clsChangeValue):
    def __init__(self, parent, record_service):

        self.record_service = record_service

        clsChangeValue.__init__(self, parent)

    def OnBtnOk(self, event):
        operator = self.cbValue.GetStringSelection()
        value = self.txtValue.GetValue()

        try:
            if not operator or not value:
                raise ValueError
        except ValueError as e:
            dial = wx.MessageDialog(None, "Please make sure that the method and value "
                                          "fields are filled out", "Bad Input", wx.OK | wx.ICON_WARNING)
            dial.ShowModal()
            return

        if operator == 'Add':
            operator = '+'
        if operator == 'Subtract':
            operator = '-'
        if operator == 'Multiply':
            operator = '*'
        if operator == 'Set to':
            operator = '='

        self.record_service.change_value(value, operator)

        self.Close()


    def OnBtnCancel(self, event):
        self.Close()
