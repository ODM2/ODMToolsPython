import os

import wx
import logging
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar
from matplotlib.widgets import Lasso
from matplotlib import path
from common.logger import LoggerTool

import gui_utils as g_util

tools = LoggerTool()
logger = tools.setupLogger(__name__, __name__ + '.log', 'w', logging.DEBUG)

class MyCustomToolbar(NavigationToolbar):
    ON_CUSTOM_LEFT = wx.NewId()
    ON_CUSTOM_RIGHT = wx.NewId()
    ON_CUSTOM_SEL = wx.NewId()
    ON_LASSO_SELECT = wx.NewId()

    # rather than copy and edit the whole (rather large) init function, we run
    # the super-classes init function as usual, then go back and delete the
    # button we don't want
    def __init__(self, plotCanvas, multPlots=False, allowselect=False):

        NavigationToolbar.__init__(self, plotCanvas)
        # delete the toolbar button we don't want
        if (not multPlots):
            CONFIGURE_SUBPLOTS_TOOLBAR_BTN_POSITION = 7
            self.DeleteToolByPos(CONFIGURE_SUBPLOTS_TOOLBAR_BTN_POSITION)

        self.AddSimpleTool(self.ON_CUSTOM_LEFT,
                           wx.Bitmap(os.path.join(g_util.resource_path("images"), "scroll_left.png")),
                           ' Pan to the left', 'Pan graph to the left')
        self.AddSimpleTool(self.ON_CUSTOM_RIGHT,
                           wx.Bitmap(g_util.resource_path("images" + g_util.slash() + "scroll_right.png")),
                           'Pan to the right', 'Pan graph to the right')



        wx.EVT_TOOL(self, self.ON_CUSTOM_LEFT, self._on_custom_pan_left)
        wx.EVT_TOOL(self, self.ON_CUSTOM_RIGHT, self._on_custom_pan_right)

        if allowselect:
            self.select_tool = self.AddSimpleTool(self.ON_LASSO_SELECT,
                                                   wx.Bitmap(
                                                       g_util.resource_path("images" + g_util.slash() + "select.png")),
                                                   'Lasso Select', 'Select datavalues from the graph', isToggle=True)

            wx.EVT_TOOL(self, self.ON_LASSO_SELECT, self.on_toggle_lasso_tool)
            # Get the ids for the existing tools
            self.pan_tool = self.FindById(self.wx_ids['Pan'])
            self.zoom_tool = self.FindById(self.wx_ids['Zoom'])
            wx.EVT_TOOL(self, self.zoom_tool.Id, self.on_toggle_pan_zoom)
            wx.EVT_TOOL(self, self.pan_tool.Id, self.on_toggle_pan_zoom)
            self.lassoAction = None
            self.select_tool.Enable(False)

        self.SetToolBitmapSize(wx.Size(16, 16))

        self.Realize()

    def editSeries(self, xys, edit):
        #enable select button
        self.xys = xys
        self.editCurve = edit
        self.select_tool.Enable(True)
        self.Realize()

    def stopEdit(self):

        self.canvas.mpl_disconnect(self.lassoAction)
        self.xys = None
        self.editCurve = None
        self.lassoAction = None
        #disable select button
        self.select_tool.Enable(False)
        self.Realize()
        #untoggle lasso button
        self.ToggleTool(self.select_tool.Id, False)


    # in theory this should never get called, because we delete the toolbar
    #  button that calls it. but in case it does get called (e.g. if there
    # is a keyboard shortcut I don't know about) then we override the method
    # that gets called - to protect against the exceptions that it throws
    # def configure_subplot(self, evt):
    #     if (not multPlots):
    #         print 'ERROR: This application does not support subplots'

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

    def _on_custom_sel_point(self, evt):
        print "select points button"
        # self.canvas.mpl_connect('button_press_event', onclick)
        pass

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

        seldatetimes = []
        for i in range(len(ind)):
            if ind[i]:
                seldatetimes.append(self.editCurve.dataTable[i][1])
                # print seldatetimes

        self._parent.changeSelection(sellist=[], datetime_list=seldatetimes)

        self.canvas.draw_idle()
        #self.canvas.widgetlock.release(self.lasso)
        del self.lasso

    def untoggle_mpl_tools(self):
        """
            This function needs to be called whenever any user-defined tool is clicked e.g. Lasso
        """
        if self.pan_tool.IsToggled():
            wx.PostEvent(
                self.GetEventHandler(),
                wx.CommandEvent(wx.EVT_TOOL.typeId, self.pan_tool.Id)
            )
            self.ToggleTool(self.pan_tool.Id, False)
        elif self.zoom_tool.IsToggled():
            wx.PostEvent(
                self.GetEventHandler(),
                wx.CommandEvent(wx.EVT_TOOL.typeId, self.zoom_tool.Id)
            )
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
        """
        Called when pan or zoom is toggled.
            Toggles off Lasso and disconnects it from the canvas
        event -- button_press_event
        """
        if event.Checked():
            self.ToggleTool(self.ON_LASSO_SELECT, False)
            self.canvas.mpl_disconnect(self.lassoAction)
            self.lassoAction = None
        # Make sure the regular pan/zoom handlers get the event
        event.Skip()
