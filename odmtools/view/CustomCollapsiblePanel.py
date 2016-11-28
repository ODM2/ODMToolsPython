import wx


class CustomCollapsiblePanel(wx.Panel):
    def __init__(self, parent, title="Sample Title", expand=0, use_combo=False, combo_trigger_item=-1):
        wx.Panel.__init__(self, parent)
        self.__master_sizer = wx.BoxSizer(wx.VERTICAL)

        self.parent = parent  # parent of this panel
        self.title = title
        self.is_expanded = expand  # is_expanded status
        self.__using_combo = use_combo
        self.trigger_item = combo_trigger_item

        # this will be the main sizer for this panel
        self.vbox = wx.BoxSizer(wx.VERTICAL)

        # this sizer contains is_expanded button and title of frame
        self.hbox = wx.BoxSizer(wx.VERTICAL)

        # self.interactive_item is the item that is interacted with to is_expanded or collapse the panel
        if self.__using_combo:
            self.interactive_item = wx.ComboBox(self, style=wx.CB_READONLY, name="interactive_item")
            self.interactive_item.Bind(wx.EVT_COMBOBOX, self.on_interactive_item)
        else:
            self.interactive_item = wx.Button(self, label=title, size=(-1, 18), style=wx.BU_LEFT | wx.STATIC_BORDER, name='interactive_item')
            self.interactive_item.Bind(wx.EVT_BUTTON, self.on_interactive_item)

        # self.lbl = wx.StaticText(self, -1, size=(-1, 5), name='cplbl')

        self.hbox.Add(self.interactive_item, 1, wx.EXPAND)
        # self.hbox.Add(self.lbl, 0)

        # add to main sizer(vbox)
        self.vbox.Add(self.hbox, 0, wx.EXPAND)

    def on_interactive_item(self, event=None):
        """
        Case for combo box: If the selected item matches the trigger item then expand, otherwise collapse
        Case for button: collapse if expanded and expand if collapsed
        :param event:
        :return:
        """
        if isinstance(self.interactive_item, wx.ComboBox):
            if self.interactive_item.GetStringSelection() == self.trigger_item:
                self.expand_panel()
            else:
                self.collapse_panel()
        else:
            if self.is_expanded:
                self.collapse_panel()
            else:
                self.expand_panel()

        if event:
            event.Skip()

    def expand_panel(self):
        self.is_expanded = True
        self.__redraw_panel()
        self.GetTopLevelParent().SetSize((400, 300))

    def __redraw_panel(self):
        for child in self.GetChildren():
            if child.GetName() == "interactive_item":
                continue
            child.Show(self.is_expanded)
        self.parent.Layout()
        self.parent.SendSizeEvent()  # make scrollbars visible if parent is scrolledWindow and if they are required automatically
        # self.lbl.SetFocus()  # Remove focus from button when pressed
        self.parent.Refresh()

    def collapse_panel(self):
        self.is_expanded = False
        self.__redraw_panel()
        self.GetTopLevelParent().SetSize((400, 150))

    def finish_layout(self):

        allSizers = []
        childSizer = None
        # Get all the sizers containing all the children of this panel
        for child in self.GetChildren():
            if child.GetName() == 'interactive_item' or child.GetName() == 'cplbl':
                continue

            childSizer = child.GetContainingSizer()
            if childSizer != None:
                # add the sizer in the list if it's no there.
                # can't use set as it changes the order of elements
                # this way we can have unique sizer or not repeating ones
                if not childSizer in allSizers:
                    allSizers.append(childSizer)

        # Get root level sizers and add to main sizer name 'vbox'
        if len(allSizers):
            for sizer in self.getRootSizers(allSizers):
                self.vbox.Add(sizer, 0, wx.EXPAND)
        else:
            print 'children of this panel are not in any sizers. They should be in a sizer/s'

            # When deleting this panel in any case, masterSizer is also getting deleted. we have to create it again
        if not isinstance(self.__master_sizer, wx._core.BoxSizer):
            self.__master_sizer = wx.BoxSizer(wx.VERTICAL)

            self.__master_sizer.Add(self, 0, wx.EXPAND)

        # Rearrange everything
        self.SetSizer(self.vbox)
        self.Fit()
        self.on_interactive_item()

    def getRootSizers(self, sizerList):
        '''
        'sizerList' contains many sizers and may possible nested sizers or sizers added inside another sizers.
        This function process the list and returns only root level sizers.
        We'll add only root level sizers to main sizer of this class name 'vbox'.
        '''
        finalList = sizerList[:]
        copyList = sizerList[:]

        for sizer in copyList:
            if len(sizer.GetChildren()):
                for child in sizer.GetChildren():
                    if child.GetClassName() == 'wxSizerItem':
                        try:
                            finalList.remove(child.GetSizer())
                        except:
                            pass
        return finalList
