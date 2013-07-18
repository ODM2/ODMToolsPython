import wx
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar

def CreateBitmap(xpm):
    bmp = wx.Image(xpm, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
    return bmp  


class MyCustomToolbar(NavigationToolbar): 

    ON_CUSTOM_LEFT  = wx.NewId()
    ON_CUSTOM_RIGHT = wx.NewId()
    ON_CUSTOM_SEL   = wx.NewId()

    # rather than copy and edit the whole (rather large) init function, we run
    # the super-classes init function as usual, then go back and delete the
    # button we don't want
    def __init__(self, plotCanvas, multPlots= False, allowselect = False):
        
        NavigationToolbar.__init__(self, plotCanvas)        
        # delete the toolbar button we don't want
        if (not multPlots):
            CONFIGURE_SUBPLOTS_TOOLBAR_BTN_POSITION = 7
            self.DeleteToolByPos(CONFIGURE_SUBPLOTS_TOOLBAR_BTN_POSITION)
            
        # add the new toolbar buttons that we do want
        # if allowselect:
        #     self.selectbutton= self.AddSimpleTool(self.ON_CUSTOM_SEL, CreateBitmap("images\\select.png"),
        #                    'Select Points', 'Select Points')
        #     wx.EVT_TOOL(self, self.ON_CUSTOM_SEL, self._on_custom_sel_point)
        #     self.selectbutton.Enable(False)
            
        self.AddSimpleTool(self.ON_CUSTOM_LEFT, CreateBitmap("images\\scroll_left.png"),
                           'Pan to the left', 'Pan graph to the left')
        wx.EVT_TOOL(self, self.ON_CUSTOM_LEFT, self._on_custom_pan_left)
        self.AddSimpleTool(self.ON_CUSTOM_RIGHT, CreateBitmap("images\\scroll_right.png"),
                           'Pan to the right', 'Pan graph to the right')
        wx.EVT_TOOL(self, self.ON_CUSTOM_RIGHT, self._on_custom_pan_right)
        

        self.SetToolBitmapSize(wx.Size(16, 16))        
        self.Realize()
    def editSeries(self):
        #enable select button
        # self.selectbutton.Enable(True)
        self.Realize()

    def stopEdit(self):
       #disable select button
        # self.selectbutton.Enable(False)
        self.Realize()

    # in theory this should never get called, because we delete the toolbar
    #  button that calls it. but in case it does get called (e.g. if there
    # is a keyboard shortcut I don't know about) then we override the method
    # that gets called - to protect against the exceptions that it throws
    # def configure_subplot(self, evt):
    #     if (not multPlots):
    #         print 'ERROR: This application does not support subplots'

    # pan the graph to the left    
    def _on_custom_pan_left(self, evt):
        ONE_SCREEN = 7   # we default to 1 week
        axes = self.canvas.figure.axes[0]
        x1,x2 = axes.get_xlim()
        ONE_SCREEN = (x2 - x1)/2
        axes.set_xlim(x1 - ONE_SCREEN, x2 - ONE_SCREEN)
        self.canvas.draw()

    # pan the graph to the right
    def _on_custom_pan_right(self, evt):
        ONE_SCREEN = 7   # we default to 1 week
        axes = self.canvas.figure.axes[0]
        x1,x2 = axes.get_xlim()
        ONE_SCREEN = (x2 - x1)/2
        axes.set_xlim(x1 + ONE_SCREEN, x2 + ONE_SCREEN)
        self.canvas.draw()

    def _on_custom_sel_point(self, evt):
        print "select points button"
        # self.canvas.mpl_connect('button_press_event', onclick)
        pass



    