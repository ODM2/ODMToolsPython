import os, sys, shutil, zipfile
BASE_DIR = os.path.dirname(os.path.realpath(__file__))

WIN_DIR = os.path.join(BASE_DIR, "Windows")
MAC_DIR = os.path.join(BASE_DIR, "Mac")
WORK_DIR = os.path.join(WIN_DIR, "Temp")

ICON_DIR = os.path.join("..", 'odmtools', 'common', "icons")
WIN_ICON_FILE = os.path.join(ICON_DIR, "ODMTools.ico")
MAC_ICON_FILE = os.path.join(ICON_DIR, "ODMTools.icns")
EXE_DIR = os.path.join(WIN_DIR, "ODMTools")

# Location of Windows files
APP_FILE = os.path.join("..", "ODMTools.py")
VERSION_FILE = os.path.join(BASE_DIR, "version.txt")

# Location of Innosetup Installer
INNO_SCRIPT = os.path.join(WIN_DIR, "odmtools_setup.iss")
INNO_EXECUTABLE = '"C:\\Program Files (x86)\\Inno Setup 5\\ISCC.exe"'
ICE_SCRIPT = os.path.join(MAC_DIR, "ODMTools.packproj")
ICE_EXECUTABLE =''

print (BASE_DIR)

def check_if_dirs_exist():
    try:

        if sys.platform == 'win32':
            print "Trying to open WIN_DIR: ",
            assert os.path.exists(WIN_DIR)
            print "Success"
        elif sys.platform =="darwin":
            print "Trying to open MAC_DIR: "
            assert os.path.exists(MAC_DIR)
            print "Success"

        print "Trying to open WORK_DIR: ", 
        assert os.path.exists(WORK_DIR)
        print "Success"

        print "Trying to open ICON_DIR: ", 
        assert os.path.exists(ICON_DIR)
        print "Success"

        print "Trying to open EXE_DIR: ", 
        assert os.path.exists(EXE_DIR)
        print "Success"

    except Exception as e:
        print e

def delete_old_out_dir():
    if os.path.exists(EXE_DIR):
        shutil.rmtree(EXE_DIR)

    if os.path.exists(WORK_DIR):
        shutil.rmtree(WORK_DIR)

def run_pyinstaller():
    try:
        os.system('pyinstaller '
            '--clean '
            '--distpath=%s ' % WIN_DIR +
            '--workpath=%s ' % WORK_DIR +
            '--specpath=%s ' % WIN_DIR +
            '--upx-dir=%s ' % BASE_DIR +
            '--icon=%s ' % WIN_ICON_FILE +
            '--version-file=%s ' % VERSION_FILE +
            # '--windowed '
            '--noconfirm ' + APP_FILE)

        return True
    except Exception as e:
        print (e)
        return False

def mac_pyinstaller():
    try:
        os.system('pyinstaller '
            '--clean '
            '--distpath=%s ' % MAC_DIR +
            '--workpath=%s ' % WORK_DIR +
            '--specpath=%s ' % WIN_DIR +
            '--upx-dir=%s ' % BASE_DIR +
            '--icon_file=%s ' % MAC_ICON_FILE +
            '--version-file=%s ' % VERSION_FILE +
            # '--windowed '
            '--noconfirm ' + APP_FILE)

        return True
    except Exception as e:
        print (e)
        return False


def run_inno():
    os.system(INNO_EXECUTABLE + " " + INNO_SCRIPT)

def run_iceberg():
    pass
    
def main():
    delete_old_out_dir()
    check_if_dirs_exist()

    if sys.platform == 'win32':


        if (run_pyinstaller()):
            run_inno()


    if sys.platform =='darwin':
        if(mac_pyinstaller()):
            run_iceberg()

if __name__ == '__main__':
    main()

# OUT_DIR = os.path.join(BASE_DIR, 'dist')
# GTK_ZIP = os.path.join('tools', 'windows', 'gtk', 'gtk_to_copy.zip')
# INNO_SCRIPT = os.path.join('tools', 'config-inno.iss')
# INNO_EXECUTABLE = '"c:\\Program Files\\Inno Setup 5\\ISCC.exe"'


# class Unzip(object):
#    def __init__(self, from_file, to_dir, verbose = False):
#        """Removed for brevity, you can find a recipe similar to this in the Cook Book"""

# def run_pyinstaller():
#    # A hack really, but remember setup.py will run on import
#    sys.argv.append('py2exe')
#    import setup


# def unzip_gtk():
#    Unzip(GTK_ZIP, OUT_DIR)


# def run_inno():
#    os.system(INNO_EXECUTABLE + " " + INNO_SCRIPT)


# def main():
#   #Clean any mess we previously made
#   delete_old_out_dir()
#   # run py2exe
#   run_py2exe()
#   # put the GTK data files in the dist directory
#   unzip_gtk()
#   # build the single file installer
#   run_inno()
#   # prevent the windows command prompt from just closing
#   raw_input('Done..')

# if __name__ == '__main__':
#   main()
