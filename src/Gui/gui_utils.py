import wx
import sys
import os
import platform

def create_bitmap(xpm):
    bmp = wx.Image(xpm, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
    return bmp 

def resource_path(relative):
    filepath = os.path.realpath(__file__)
    return os.path.join(
        os.path.dirname(filepath), relative
    )

def slash():
	OS = platform.system()
	if OS == 'Darwin' or OS == 'mac':
		return '/'
	elif OS == 'Windows':
		return '\\'