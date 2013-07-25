import wx
import sys

def create_bitmap(xpm):
    bmp = wx.Image(xpm, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
    return bmp 

def get_base_dir():
	if getattr(sys, 'frozen', None):
	    basedir = sys._MEIPASS + '\images'
	else:
	    basedir = "images"
	return basedir