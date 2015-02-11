import wx
from odmtools.view.clsLinearDrift import clsLinearDrift

__author__ = 'jmeline'

class frmLinearDrift(clsLinearDrift):
    def __init__(self, parent, record_service):
        self._record_service = record_service
        clsLinearDrift.__init__(self, parent)

    def OnBtnOKButton(self, event):
        """
        Perform Drift Correction based on given input. Catch errors if the user enters something invalid
        """
        try:
            self._record_service.drift_correction(float(self.txtFinalGapValue.GetValue()))
        except Exception as e:
            dial = wx.MessageDialog(None, "Unable to convert value to float %s" % e, "Bad Input",
                wx.OK | wx.ICON_ERROR)
            dial.ShowModal()
        self.Close()

    def OnBtnCancelButton(self, event):
        self.Close()