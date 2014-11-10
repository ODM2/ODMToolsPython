import os

import wx
from wx.lib.pubsub import pub as Publisher

from odmtools.controller import odmHighlightSTC


ID_NEW = 101
ID_OPEN = 102
ID_SAVE = 103
ID_SAVE_AS = 104
ID_EXECUTE_BUTTON = 300
ID_EXECUTE_SELECTION_BUTTON = 301
ID_EXECUTE_LINE_BUTTON = 302

#wildcard = "Python Source (*.py, .py)|*" #All files (*.*)|*.*"
wildcard = "Python source (*.py)|*.py|" \
            "All files (*.*)|*.*"

class pnlScript(wx.Panel):
    def __init__(self, parent, id=wx.ID_ANY, name="", pos=(0, 0), size=(200, 200)):
        #super(pnlScript, self).__init__(parent, id, name=name, pos=pos, size=size, style=0)
        wx.Panel.__init__(self, parent, id)
        self.console = parent.txtPythonConsole
        self.control = odmHighlightSTC.highlightSTC(self)
        self.parent = parent
        # self.control = stc.StyledTextCtrl(self, 1, style=wx.TE_MULTILINE)

        # Set up menu
        #filemenu = wx.Menu()
        # use ID_ for future easy reference -- much better than "48", "404", etc.
        # The & character indicates the shortcut key
        #filemenu.Append(ID_NEW, "&New", "New file")
        #filemenu.Append(ID_OPEN, "&Open Existing", "Append to an existing file")
        #filemenu.AppendSeparator()
        #filemenu.Append(ID_SAVE, "&Save", " Save current file")
        #filemenu.Append(ID_SAVE_AS, "Save &As...", " Save to specific file")

        # create the menubar
        #menuBar = wx.MenuBar()
        #menuBar.Append(filemenu, "&File")
        #self.SetMenuBar(menuBar)

        #wx.EVT_MENU(self, ID_NEW, self.OnNew)
        #wx.EVT_MENU(self, ID_OPEN, self.OnOpen)
        #wx.EVT_MENU(self, ID_SAVE, self.OnSave)
        #wx.EVT_MENU(self, ID_SAVE_AS, self.OnSaveAs)

        # Set up execute buttons
        self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.executeButton = wx.Button(self, ID_EXECUTE_BUTTON, "&Execute")
        self.executeButton.Bind(wx.EVT_BUTTON, self.OnExecute)
        self.sizer2.Add(self.executeButton, 1, wx.ALIGN_LEFT)

        self.executeSelectionButton = wx.Button(self, ID_EXECUTE_SELECTION_BUTTON, "Execute &Selection")
        self.executeSelectionButton.Bind(wx.EVT_BUTTON, self.OnExecuteSelection)
        self.sizer2.Add(self.executeSelectionButton, 1, wx.ALIGN_LEFT)

        self.executeLineButton = wx.Button(self, ID_EXECUTE_LINE_BUTTON, "Execute &Line")
        self.executeLineButton.Bind(wx.EVT_BUTTON, self.OnExecuteLine)
        self.sizer2.Add(self.executeLineButton, 1, wx.ALIGN_LEFT)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.sizer2, 0, wx.EXPAND)
        self.sizer.Add(self.control, 1, wx.EXPAND)

        self.SetSizer(self.sizer)
       # self.SetAutoLayout(1)
        self.sizer.Fit(self)

        self.dirname = ''
        self.filename = ''
        self._styles = [None] * 32
        self._free = 1

    def newScript(self):
        self.filename = ''
        self.control.SetText('')
        # self.SetTitle("Editing a new file")
        Publisher.sendMessage("script.title", title="Editing a new file")
        record_service = self.parent.getRecordService()
        print"Parent=%s" % self.parent
        record_service.write_header()

    def getOverwriteDialog(self):
        return wx.MessageBox("Please check that your script has been saved before it is overwritten. "
                    "Would you like to save it now? \n\nSelecting 'No' will delete anything you "
                    "may have in the script", 'Save Script?', wx.CANCEL | wx.YES_NO | wx.ICON_EXCLAMATION | wx.NO_DEFAULT)

    def OnNew(self, e):
        ## Check if data already exists
        if len(self.control.GetText()) > 0:
            val = self.getOverwriteDialog()
            if val == wx.YES:
                if self.OnSaveAs(e):
                    self.newScript()
            elif val == wx.NO:
                self.newScript()
            else:
                pass
        else:
            self.newScript()


    def OnOpen(self, e):
        ## Check if data already exists
        if len(self.control.GetText()) > 0:
            val = self.getOverwriteDialog()
            if val == wx.YES:
                self.OnSaveAs(e)
            elif val == wx.CANCEL:
                return
            elif val == wx.NO:
                pass

        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", wildcard, wx.OPEN | wx.CHANGE_DIR | wx.MULTIPLE )
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            # Open the file and set its contents into the edit window
            filehandle = open(os.path.join(self.dirname, self.filename), 'r')
            if filehandle:
                self.control.SetText(filehandle.read())
                self.control.EmptyUndoBuffer()
                filehandle.close()
                # self.SetTitle("Editing: %s" % self.filename)
                Publisher.sendMessage("script.title", title="Editing: %s" % self.filename)
            else:
                pass

        dlg.Destroy()

    def OnSave(self, e):
        if self.filename:
            self.OnSaveAs(e)
        else:
            saved_text = self.control.GetText()
            filehandle = open(os.path.join(self.dirname, self.filename), 'w')
            filehandle.write(saved_text)
            filehandle.close()
            self.setTitle("Editing: %s" % self.filename)

    def OnSaveAs(self, e):
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", wildcard, wx.SAVE | wx.OVERWRITE_PROMPT)
        result = dlg.ShowModal()
        if result == wx.ID_OK:
            saved_text = self.control.GetText()
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            filehandle = open(os.path.join(self.dirname, self.filename), 'w')
            filehandle.write(saved_text)
            filehandle.close()

            # self.SetTitle("Editing: %s" % self.filename)
            self.setTitle("Editing: %s" % self.filename)
            dlg.Destroy()
            return True

        elif result == wx.ID_CANCEL:
            dlg.Destroy()
            return False
    def runCommand(self, text):
        #TODO Stop recording
        # get ahold of record service and turn it off do i need a publisher command?
        
        self.parent.record_service.toggle_record(False)
        for line in text.split("\n"):
            self.console.shell.run(line)
        self.console.shell.run("\n")
        self.parent.record_service.toggle_record(True)
        #restart recording

    def OnExecute(self, e):

        text = self.control.GetText()
        #for line in text.split("\n"):
        #    self.console.shell.run(line)
        #self.console.shell.run("\n")
        self.runCommand(text)


    def OnExecuteSelection(self, e):
        text = self.control.GetSelectedTextRaw()
        #for line in text.split("\n"):
        #    self.console.shell.run(line)
        self.runCommand(text)

    def OnExecuteLine(self, e):
        text = self.control.GetSelectedTextRaw()
        if text == "":
            text = self.control.GetLine(self.control.GetCurrentLine())

        #for line in text.split("\n"):
        #    self.console.shell.run(line)
        self.runCommand(text)

    def newKeyPressed(self):
        if self.filename:
            title = "Editing: %s*" % self.filename
            self.setTitle(title)

    def setTitle(self, title):
        Publisher.sendMessage("script.title", title=title)

    def getStyle(self, c='black'):
        """
        Returns a style for a given colour if one exists.  If no style
        exists for the colour, make a new style.

        If we run out of styles, (only 32 allowed here) we go to the top
        of the list and reuse previous styles.

        """
        free = self._free
        if c and isinstance(c, (str, unicode)):
            c = c.lower()
        else:
            c = 'black'

        try:
            style = self._styles.index(c)
            return style

        except ValueError:
            style = free
            self._styles[style] = c
            self.control.StyleSetForeground(style, wx.NamedColour(c))

            free += 1
            if free > 31:
                free = 0
            self._free = free
            return style

    def write(self, text, c=None):
        """
        Add the text to the end of the control using color c which
        should be suitable for feeding directly to wx.NamedColour.

        'text' should be a unicode string or contain only ascii data.
        """
        style = self.getStyle(c)
        lenText = len(text.encode('utf8'))
        end = self.control.GetLength()
        ##        self.control.DocumentEnd()
        self.control.AppendText(text)
        ##        self.control.AddStyledText(text)
        self.control.StartStyling(end, 31)
        self.control.SetStyling(lenText, style)
        self.control.EnsureCaretVisible()
        self.control.onUpdateUI(None)

    __call__ = write