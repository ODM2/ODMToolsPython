import wx
import sys
import os
import platform

def create_bitmap(xpm):
    bmp = wx.Image(xpm, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
    return bmp 

def resource_path(relative):
    OS = platform.system()
    if OS =='Darwin' and os.environ.get('RESOURCEPATH'):
        return os.path.join(os.environ.get('RESOURCEPATH'), relative)
    filepath = os.path.realpath(__file__)
    return os.path.join(
        os.path.dirname(os.path.dirname(filepath)), relative
    )

def slash():
	OS = platform.system()
	if OS == 'Darwin' or OS == 'mac':
		return '/'
	elif OS == 'Windows':
		return '\\'


def imgpath(imgname):
    
    return resource_path( "images" + slash() + imgname)


#print os.environ['HOME']

 # using get will return `none` if key is not present rather than raise a `KeyError`
#print os.environ.get('RESOURCEPATH')

 # os.getenv is equivalent, and can also give a default value instead of None
#print os.getenv('KEY_THAT_MIGHT_EXIST', default_value)


