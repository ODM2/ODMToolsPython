import sys, os


def resource_path(relative=None):
    APPNAME = "ODMTools"
    if sys.platform.lower() == 'darwin':
    # TODO mac stuff
    #     #appdata = os.path.expanduser("~")+slash()+'Library'+slash()+'Preferences'+slash()+"ODMToolsPython"
    #     appdata = os.path.join(os.path.expanduser("~"),'/.local/share/'+APPNAME)
        appdata = os.path.expanduser(os.path.join("~", "." + APPNAME))
    elif 'win' in sys.platform:
        appdata = os.path.join(os.environ['APPDATA'], APPNAME)
    else:
        appdata = os.path.expanduser(os.path.join("~", "." + APPNAME))

    if not os.path.exists(appdata):
        os.mkdir(appdata)

    return os.path.join(appdata, relative)


def slash():
    if sys.platform.lower() == 'Darwin' or sys.platform.lower() == 'mac':
        return '/'
    elif 'win' in sys.platform:
        return '\\'