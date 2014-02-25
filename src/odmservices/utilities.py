import sys
import os


def resource_path(relative):
    APPNAME = "ODMTools"
    if sys.platform == 'darwin':
        # TODO mac stuff
        pass
    elif 'win' in sys.platform:
        appdata = os.path.join(os.environ['APPDATA'], APPNAME)
    else:
        appdata = os.path.expanduser(path.join("~", "." + APPNAME))

    return os.path.join(appdata, relative)


def slash():
    OS = platform.system()
    if OS == 'Darwin' or OS == 'mac':
        return '/'
    elif OS == 'Windows':
        return '\\'