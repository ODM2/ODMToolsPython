import logging

import wx
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar
from matplotlib.widgets import Lasso
from matplotlib import path
from matplotlib import dates

# from odmtools.common.logger import LoggerTool
from odmtools.common.icons.plotToolbar import back, filesave, select, scroll_right, \
    scroll_left, zoom_data, zoom_to_rect, subplots, forward, home, move



# tools = LoggerTool()
# logger = tools.setupLogger(__name__, __name__ + '.log', 'w', logging.DEBUG)
logger =logging.getLogger('main')


def bind(actor,event,action,id=None):
        if id is not None:
            event(actor, id, action)
        else:
            event(actor,action)



class MyCustomToolbar(NavigationToolbar):
    '''ON_CUSTOM_LEFT = wx.NewId()
    ON_CUSTOM_RIGHT = wx.NewId()
    ON_CUSTOM_SEL = wx.NewId()
    ON_LASSO_SELECT = wx.NewId()
    ON_ZOOM_DATA_SELECT = wx.NewId()'''

    toolitems = (
        ('Home', 'Reset original view', home, 'home'),
        ('Zoom to Data', 'Zoom to data without NoDataValues', zoom_data, 'on_toggle_zoom_data_tool'),

        ('Back', 'Back to  previous view', back, 'back'),
        ('Forward', 'Forward to next view', forward, 'forward'),
        (None, None, None, None),
        ('Pan', 'Pan axes with left mouse, zoom with right', move, 'pan'),
        ('Zoom', 'Zoom to rectangle', zoom_to_rect, 'zoom'),
        (None, None, None, None),
        ('Subplots', 'Configure subplots', subplots, 'configure_subplots'),
        ('PanLeft', 'Pan graph to the left', scroll_left, '_on_custom_pan_left'),
        ('PanRight', 'Pan graph to the right', scroll_right, '_on_custom_pan_right'),
        ('Save', 'Save the figure', filesave, 'save_figure'),
        ('Select', 'Select datavalues from the graph', select, 'on_toggle_lasso_tool'),
      )




    # rather than copy and edit the whole (rather large) init function, we run
    # the super-classes init function as usual, then go back and delete the
    # buttons we don't want
    def _init_toolbar(self):

        self._parent = self.canvas.GetParent()


        self.wx_ids = {}
        for text, tooltip_text, image_file, callback in self.toolitems:
            if text is None:
                self.AddSeparator()
                continue
            self.wx_ids[text] = wx.NewId()
            if text in ['Pan', 'Zoom', 'Select']:
               self.AddCheckTool(self.wx_ids[text], image_file.GetBitmap(),
                                 shortHelp=text, longHelp=tooltip_text)
            else:
               self.AddSimpleTool(self.wx_ids[text], image_file.GetBitmap(),
                                  text, tooltip_text)
            bind(self, wx.EVT_TOOL, getattr(self, callback), id=self.wx_ids[text])

        self.Realize()




    def __init__(self, plotCanvas, multPlots=False, allowselect=False):
        NavigationToolbar.__init__(self, plotCanvas)
        #self.ClearTools()


        # delete the toolbar button we don't want
        if (not multPlots):
            CONFIGURE_SUBPLOTS_TOOLBAR_BTN_POSITION = 8
            self.DeleteToolByPos(CONFIGURE_SUBPLOTS_TOOLBAR_BTN_POSITION)

        #self.AddSimpleTool(self.ON_CUSTOM_LEFT, scroll_left.GetBitmap(), ' Pan to the left', 'Pan graph to the left')
        #self.AddSimpleTool(self.ON_CUSTOM_RIGHT, scroll_right.GetBitmap(), 'Pan to the right', 'Pan graph to the right')

        #wx.EVT_TOOL(self, self.ON_CUSTOM_LEFT, self._on_custom_pan_left)
        #wx.EVT_TOOL(self, self.ON_CUSTOM_RIGHT, self._on_custom_pan_right)

        if allowselect:
            """self.select_tool = self.AddSimpleTool(self.ON_LASSO_SELECT, select.GetBitmap(), 'Lasso Select',
                                                  'Select datavalues from the graph', isToggle=True)

            self.zoom_to_data = self.AddSimpleTool(self.ON_ZOOM_DATA_SELECT, zoom_data.GetBitmap(), 'Zoom to Data',
                                                  'Zoom to data without NoDataValues')

            wx.EVT_TOOL(self, self.ON_LASSO_SELECT, self.on_toggle_lasso_tool)
            wx.EVT_TOOL(self, self.ON_ZOOM_DATA_SELECT, self.on_toggle_zoom_data_tool)"""

            # Get the ids for the existing tools
            self.pan_tool = self.FindById(self.wx_ids['Pan'])
            self.zoom_tool = self.FindById(self.wx_ids['Zoom'])
            self.select_tool=self.FindById(self.wx_ids['Select'])
            self.zoom_to_data = self.FindById(self.wx_ids['Zoom to Data'])

            wx.EVT_TOOL(self, self.zoom_tool.Id, self.on_toggle_pan_zoom)
            wx.EVT_TOOL(self, self.pan_tool.Id, self.on_toggle_pan_zoom)
            self.lassoAction = None
            self.select_tool.Enable(False)
            self.zoom_to_data.Enable(False)

        else:
            ZOOM_DATA_BTN_POSITION = 1
            SELECT_DATA_BTN_POSTITION = self.ToolsCount-1
            self.DeleteToolByPos(SELECT_DATA_BTN_POSTITION)
            self.DeleteToolByPos(ZOOM_DATA_BTN_POSITION)


        self.SetToolBitmapSize(wx.Size(16, 16))

        #msg = wx.StaticText(self, -1, '|')
        #msg.SetForegroundColour((108, 123, 139))

        #self.AddControl(msg)
        self.AddSeparator()

        self.msg = wx.StaticText(self, -1, "")
        self.AddControl(self.msg)

        self.Realize()

    def editSeries(self, xys, edit):
        # enable select button
        self.xys = xys
        self.editCurve = edit
        self.select_tool.Enable(True)
        self.zoom_to_data.Enable(True)
        self.Realize()

    def stopEdit(self):

        self.canvas.mpl_disconnect(self.lassoAction)
        self.xys = None
        self.editCurve = None
        self.lassoAction = None
        # untoggle select button
        self.ToggleTool(self.select_tool.Id, False)
        # disable select button
        self.select_tool.Enable(False)
        self.zoom_to_data.Enable(False)
        self.Realize()
        #untoggle lasso button
        #self.ToggleTool(self.select_tool.Id, False)


    # pan the graph to the left
    def _on_custom_pan_left(self, evt):
        ONE_SCREEN = 7  # we default to 1 week
        axes = self.canvas.figure.axes[0]
        x1, x2 = axes.get_xlim()
        ONE_SCREEN = (x2 - x1) / 2
        axes.set_xlim(x1 - ONE_SCREEN, x2 - ONE_SCREEN)
        self.canvas.draw()


    # pan the graph to the right
    def _on_custom_pan_right(self, evt):
        ONE_SCREEN = 7  # we default to 1 week
        axes = self.canvas.figure.axes[0]
        x1, x2 = axes.get_xlim()
        ONE_SCREEN = (x2 - x1) / 2
        axes.set_xlim(x1 + ONE_SCREEN, x2 + ONE_SCREEN)
        self.canvas.draw()


    def _onPress(self, event):
        self.myEvent = event
        if event.inaxes is None:
            return
        self.lasso = Lasso(event.inaxes, (event.xdata, event.ydata), self.callback)
        # acquire a lock on the widget drawing
        #self.canvas.widgetlock(self.lasso)

    def callback(self, verts):
        p = path.Path(verts)
        ind = p.contains_points(self.xys)

        df = self.editCurve.dataTable
        #selected_datetime_list = df[ind].LocalDateTime.tolist()
        filtered_datetime_dataframe = df[ind]
        self._parent.lassoChangeSelection(filtered_datetime=filtered_datetime_dataframe)
        #self._parent.lassoChangeSelection(datetime_list=selected_datetime_list)
        self.canvas.draw_idle()
        del self.lasso



    def untoggle_mpl_tools(self):
        """
            This function needs to be called whenever any user-defined tool is clicked e.g. Lasso
        """
        if self.pan_tool.IsToggled():
            wx.PostEvent(self.GetEventHandler(), wx.CommandEvent(wx.EVT_TOOL.typeId, self.pan_tool.Id))
            self.ToggleTool(self.pan_tool.Id, False)
        elif self.zoom_tool.IsToggled():
            wx.PostEvent(self.GetEventHandler(), wx.CommandEvent(wx.EVT_TOOL.typeId, self.zoom_tool.Id))
            self.ToggleTool(self.zoom_tool.Id, False)

    def on_toggle_lasso_tool(self, event):
        """
            Lasso Tool Handler
            event -- button_press_event
        """

        if event.Checked():
            self.untoggle_mpl_tools()
            self.lassoAction = self.canvas.mpl_connect('button_press_event', self._onPress)
        else:
            self.canvas.mpl_disconnect(self.lassoAction)
            self.lassoAction = None

    def on_toggle_pan_zoom(self, event):
        #reset the extents to exclude any no data values
        if event.Checked():

            self.ToggleTool(self.select_tool.Id, False)
            self.canvas.mpl_disconnect(self.lassoAction)
            self.lassoAction = None
        # Make sure the regular pan/zoom handlers get the event
        event.Skip()

    def on_toggle_zoom_data_tool(self, event):
        if self._views.empty():
            self.push_current()
        nodvvals= self.editCurve.dataTable[self.editCurve.dataTable["DataValue"] != self.editCurve.noDataValue]
        #dvs = [x["DataValue"] for x in  if x[0] != self.editCurve.noDataValue]
        #date= [x[1] for x in self.editCurve.dataTable if x[0] != self.editCurve.noDataValue]

        axes = self.canvas.figure.axes[0]
        axes.set_ylim(min(nodvvals["DataValue"]), max(nodvvals["DataValue"]))
        axes.set_xlim(dates.date2num([min(nodvvals.index), max(nodvvals.index)]))

        self.push_current()
        self.canvas.draw()


#must add these methods for mac functionality
    def release_zoom(self, event):
        super(self.__class__, self).release_zoom(event)
        self.canvas.draw()
    def press_pan(self, event):
        super(self.__class__, self).press_pan(event)
        self.canvas.draw()
    def back(self, event):
        super(self.__class__, self).back(event)
        self.canvas.draw()
    def forward(self, event):
        super(self.__class__, self).forward(event)
        self.canvas.draw()
    def home(self, event):
        super(self.__class__, self).home(event)
        self.canvas.draw()
