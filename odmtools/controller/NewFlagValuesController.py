import wx
from odmtools.view.NewFlagValuesView import NewFlagValuesView


class NewFlagValuesController(NewFlagValuesView):
    def __init__(self, parent, series_service, qualifier_choice, record_service):

        NewFlagValuesView.__init__(self, parent)
        self.series_service = series_service
        self.qualifer_choice = qualifier_choice
        self.record_service = record_service

        annotations = self.series_service.get_all_annotations()
        self.append_items_to_annotation(annotations)
        self.annotation_combo.SetSelection(0)

        self.cancel_button.Bind(wx.EVT_BUTTON, self.on_cancel)
        self.ok_button.Bind(wx.EVT_BUTTON, self.on_ok)
        self.MakeModal(True)

    def append_items_to_annotation(self, annotations):
        self.annotation_combo.Append("[New Annontation]")
        if not isinstance(annotations, list):
            print "type(annotations) must be list of annotations"
            return

        for item in annotations:
            self.annotation_combo.Append(item.AnnotationCode + item.AnnotationText)

    def on_cancel(self, event):
        self.MakeModal(False)
        self.Destroy()
        event.Skip()

    def on_ok(self, event):
        code = self.code_textbox.GetValue()
        text = self.text_textbox.GetValue()

        self.series_service.create_annotation(code, text)
        self.on_cancel(event)
