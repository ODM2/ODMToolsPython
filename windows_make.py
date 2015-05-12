import os, sys, shutil, zipfile

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

# Location of Windows files
WIN_DIR = os.path.join(BASE_DIR, 'setup', "Windows")

# Location of Innosetup Installer
INSTALLER_DIR = os.path.join(BASE_DIR, "setup", "Output")
EXE_DIR = os.path.join(WIN_DIR, "ODMTools")

INNO_SCRIPT = os.path.join("setup", "odmtools_setup_build_updated.iss")
INNO_EXECUTABLE = '"C:\\Program Files (x86)\\Inno Setup 5\\ISCC.exe"'
print (BASE_DIR)


def delete_old_out_dir():
   if os.path.exists(EXE_DIR):
     shutil.rmtree(EXE_DIR)

def run_pyinstaller():
    try:
        os.system('pyinstaller '
            '--clean '
            '--distpath="setup\Windows" '
            '--workpath="setup\Windows\work" '
            '--hidden-import=pyodbc '
            '--upx-dir="setup\Windows" '
            '--noconfirm '
            'ODMTools.py')
        return True
    except Exception as e:
        print (e)
        return False


def run_inno():
    os.system(INNO_EXECUTABLE + " " + INNO_SCRIPT)
    
def main():
    delete_old_out_dir()

    if (run_pyinstaller()):
        run_inno()

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
