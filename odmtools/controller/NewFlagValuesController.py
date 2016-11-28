import wx
from odmtools.view.NewFlagValuesView import NewFlagValuesView


class NewFlagValuesController(NewFlagValuesView):
    def __init__(self, parent, series_service, qualifier_choice, record_service):

        NewFlagValuesView.__init__(self, parent)
        self.series_service = series_service
        self.qualifer_choice = qualifier_choice
        self.record_service = record_service
        self.__new_annotation = "New Annontation"

        annotations = self.series_service.get_all_annotations()
        self.append_items_to_annotation(annotations)
        self.annotation_combo.SetSelection(0)
        self.annotation_combo.Append(self.__new_annotation)

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
        event.Skip()

    def on_ok(self, event):
        selection = self.annotation_combo.GetValue()
        if selection == self.__new_annotation:
            code = self.code_textbox.GetValue()
            text = self.text_textbox.GetValue()

            annotation = self.series_service.create_annotation(code, text)
            self.record_service.flag(annotation.AnnotationID)

        self.on_cancel(event)

if __name__ == '__main__':
    app = wx.App(False)
    controller = NewFlagValuesController(None, None, None, None)
    controller.Show()
    app.MainLoop()

