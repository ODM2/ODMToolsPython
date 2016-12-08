import wx
from odmtools.view.NewFlagValuesView import NewFlagValuesView
import odmtools.controller.olvAddPoint


class NewFlagValuesController(NewFlagValuesView):
    def __init__(self, parent, series_service, qualifier_choice, record_service):

        NewFlagValuesView.__init__(self, parent)
        self.parent = parent
        self.series_service = series_service
        self.qualifer_choice = qualifier_choice
        self.record_service = record_service
        self.__new_annotation = "New Annontation"

        if self.qualifer_choice:
            annotations = self.series_service.get_all_annotations()
            self.append_items_to_annotation(annotations)

        self.annotation_combo.Append(self.__new_annotation)
        self.annotation_combo.SetSelection(0)

        self.cancel_button.Bind(wx.EVT_BUTTON, self.on_cancel)
        self.Bind(wx.EVT_CLOSE, self.on_cancel)
        self.ok_button.Bind(wx.EVT_BUTTON, self.on_ok)
        self.MakeModal(True)

    def append_items_to_annotation(self, annotations):
        if not isinstance(annotations, list):
            print "type(annotations) must be list of annotations"
            return

        for item in annotations:
            self.annotation_combo.Append(str(item.AnnotationCode + ":" + item.AnnotationText))

    def on_cancel(self, event):
        self.MakeModal(False)
        self.Destroy()

        if event:
            event.Skip()

    def on_ok(self, event):
        selection = self.annotation_combo.GetValue()
        if selection == self.__new_annotation:
            code = self.code_textbox.GetValue()
            text = self.text_textbox.GetValue()

            annotation = self.series_service.create_annotation(code, text)
        else:
            code = selection.split(':')[0]
            annotation = self.series_service.get_annotation_by_code(code)
        self.record_service.flag(annotation.AnnotationID)

        if isinstance(self.parent, odmtools.controller.olvAddPoint.OLVAddPoint):
            self.parent.refresh_annotations()

        self.on_cancel(event)

if __name__ == '__main__':
    app = wx.App(False)
    controller = NewFlagValuesController(None, None, None, None)
    controller.Show()
    app.MainLoop()

