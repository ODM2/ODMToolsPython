import wx
from odmtools.view.WizardProcessLevelView import WizardProcessLevelView
from wx.wizard import WizardPageSimple


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

    def __fetch_data(self):
        series_service = self.service_manager.get_series_service()
        processes = series_service.get_all_qcls()

        data = []
        for proc in processes:
            data.append([
                proc.code,
                proc.definition,
                proc.explanation,
                proc.id
            ])

        self.processing_level_view.existing_process_table.set_table_content(data=data)
