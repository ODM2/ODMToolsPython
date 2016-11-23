import wx
from odmtools.view.WizardProcessLevelView import WizardProcessLevelView
from wx.wizard import WizardPageSimple
from odm2api.ODM2.models import ProcessingLevels


class WizardProcessLevelController(WizardPageSimple):
    def __init__(self, parent, service_manager):
        WizardPageSimple.__init__(self, parent)

        self.service_manager = service_manager
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.processing_level_view = WizardProcessLevelView(self)
        main_sizer.Add(self.processing_level_view, 1, wx.EXPAND | wx.RIGHT, -16)
        self.SetSizer(main_sizer)

        table_columns = ["Code", "Definition", "Explanation", "ID"]
        self.processing_level_view.existing_process_table.set_columns(table_columns)
        self.__fetch_data()

        self.processing_level_view.create_process_level_radio.Bind(wx.EVT_RADIOBUTTON, self.on_create_radio)
        self.processing_level_view.existing_process_radio.Bind(wx.EVT_RADIOBUTTON, self.on_existing_radio)

    def on_create_radio(self, event):
        self.processing_level_view.existing_process_table.Enable(False)
        self.__set_create_proces_section(True)

    def on_existing_radio(self, event):
        self.processing_level_view.existing_process_table.Enable(True)
        self.__set_create_proces_section(False)

    def __set_create_proces_section(self, active):
        if not isinstance(active, bool):
            raise Exception("activet must be type bool")

        self.processing_level_view.level_code_text_ctrl.Enable(active)
        self.processing_level_view.definition_text_ctrl.Enable(active)
        self.processing_level_view.explanation_text_ctrl.Enable(active)

    def __fetch_data(self):
        series_service = self.service_manager.get_series_service()
        processes = series_service.get_all_processing_levels()

        data = []
        for proc in processes:
            data.append([
                proc.ProcessingLevelCode,
                proc.Definition,
                proc.Explanation,
                proc.ProcessingLevelID
            ])

        self.processing_level_view.existing_process_table.set_table_content(data=data)

    def get_processing_level(self):
        if self.processing_level_view.create_process_level_radio.GetValue():
            return self.__select_existing_processing_level()

        if self.processing_level_view.existing_process_radio.GetValue():
            return self.__select_existing_processing_level()

        return None

    def __select_existing_processing_level(self):
        selected_row = self.processing_level_view.existing_process_table.get_selected_row()
        code = selected_row[0]
        proc_level = self.service_manager.get_series_service().get_processing_level_by_code(codes=code)
        return proc_level

    def __create_processing_level(self):
        code = self.processing_level_view.level_code_text_ctrl.GetValue()
        definition = self.processing_level_view.definition_text_ctrl.GetValue()
        explanation = self.processing_level_view.explanation_text_ctrl.GetValue()

        proc = ProcessingLevels()
        proc.ProcessingLevelCode = code
        proc.Definition = definition
        proc.Explanation = explanation

        return proc
