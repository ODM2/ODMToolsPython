# -*- coding: utf-8 -*-
from __future__ import with_statement
import os, sys, shutil, zipfile, platform
from contextlib import closing
from zipfile import ZipFile, ZIP_DEFLATED

#need Windows installer
#windows installer with console
#windows no install( include console)
#mac installer
#mac no installer




## Update odmtools.meta.data whenever creating a release
from odmtools.meta import data

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
SETUP_DIR = os.path.join(BASE_DIR, 'setup')
WIN_DIR = os.path.join(SETUP_DIR, "Windows")
MAC_DIR = os.path.join(SETUP_DIR, "Mac")

MAC_DIST_DIR = os.path.join(MAC_DIR, "Dist")
DIST_DIR = os.path.join(WIN_DIR, 'Dist')


MAC_WORK_DIR = os.path.join(MAC_DIR, "Temp")
WORK_DIR = os.path.join(WIN_DIR, "Temp")

ICON_DIR = os.path.join('odmtools', 'common', "icons")
WIN_ICON_FILE = os.path.join(ICON_DIR, "ODMTools.ico")
MAC_ICON_FILE = os.path.join(ICON_DIR, "ODMTools.icns")

APP_DIR = os.path.join(MAC_DIR, 'Dist', "ODMTools.app")
# Location of Windows files
APP_FILE = os.path.join(BASE_DIR, "ODMTools.py")
MAKE_FILE = os.path.realpath(__file__)
VERSION_FILE = os.path.join(SETUP_DIR, "version.txt")

# Location of Innosetup Installer
INNO_SCRIPT = os.path.join(WIN_DIR, "odmtools_setup.iss")
INNO_EXECUTABLE = '"C:\\Program Files (x86)\\Inno Setup 5\\ISCC.exe"'
ICE_SCRIPT = os.path.join(MAC_DIR, "ODMTools.packproj")
ICE_EXECUTABLE ='freeze'

def check_if_dirs_exist():
    try:
        if sys.platform == 'win32':
            print "Trying to open WIN_DIR: ",
            if not os.path.exists(WIN_DIR):
                os.mkdir(WIN_DIR)
                print "Created: ", WIN_DIR
            print "Success"

            print "Trying to confirm that INNO_SCRIPT exists: ",
            assert os.path.exists(INNO_SCRIPT)
            print "Success: ", INNO_SCRIPT
        elif sys.platform =="darwin":
            print "Trying to open MAC_DIR: "
            assert os.path.exists(MAC_DIR)
            print "Success"

        print "Trying to open WORK_DIR: ",
        if not os.path.exists(WORK_DIR):
            print "Failed... Trying to create the folder...",
            os.mkdir(WORK_DIR)
            print "Created: ", WORK_DIR
        print "Success"


        print "Trying to open DIST_DIR: ",
        if not os.path.exists(DIST_DIR):
            print "Failed... Trying to create the folder...",
            os.mkdir(DIST_DIR)
            print "Created: ", DIST_DIR
        print "Success"

        print "Trying to open ICON_DIR: ",
        assert os.path.exists(ICON_DIR)
        print "Success"

    except Exception as e:
        print e

def zipdir(basedir, archivename):
    assert os.path.isdir(basedir)
    with closing(ZipFile(archivename, "w", ZIP_DEFLATED)) as z:
        for root, dirs, files in os.walk(basedir):
            #NOTE: ignore empty directories
            for fn in files:
                absfn = os.path.join(root, fn)
                zfn = absfn[len(basedir)+len(os.sep):]
                z.write(absfn, zfn)
def printInfo():
    print "============================================================="
    print "=             ODMTools Installer                             "
    print "= Be sure to update odmtools/meta/data with every release    "
    print "= Building release: {version}".format(version=data.version),
    print "\n= Platform: {platform}, {architecture}".format(platform=sys.platform, architecture=platform.architecture()), "\n="
    print "============================================================="
    print "Environment Variables: "
    print ("APP_FILE: ", APP_FILE)
    print ("MAKE_FILE: ", MAKE_FILE)
    print ("BASE_DIR: ", BASE_DIR)
    print ("SETUP_DIR: ", SETUP_DIR)
    print ("DIST_DIR: ", DIST_DIR)

    ## Windows Specific Files/Directories
    print ("WIN_DIR: ", WIN_DIR)
    print ("WIN_ICON_FILE: ", WIN_ICON_FILE)
    print ("WORK_DIR: ", WORK_DIR)
    print ("INNO_SCRIPT: ", INNO_SCRIPT)
    print ("INNO_EXECUTABLE: ", INNO_EXECUTABLE)

    ## OSX Specific Files/Directories
    print ("MAC_DIR: ", MAC_DIR)
    print ("MAC_ICON_FILE: ", MAC_ICON_FILE)
    print ("MAC_WORK_DIR: ", MAC_WORK_DIR)

    print "============================================================="
    print "Checking if the required directories exist"

    check_if_dirs_exist()

def obtain_exe_filename(console=False):
    if console:
        return "{app}_{version}_{os}_{arch}_{type}".format(app=data.app_name,
        version=data.version, os=sys.platform, arch='x86_64', type= "console")
    else:
        return "{app}_{version}_{os}_{arch}".format(app=data.app_name,
        version=data.version, os=sys.platform, arch='x86_64')

def delete_old_out_dir():
    loc_exists = os.path.exists(DIST_DIR)
    isFile = os.path.isfile(DIST_DIR)
    isDir = os.path.isdir(DIST_DIR)
    if loc_exists and isFile:
        print "Removing file DIST_DIR"
        os.remove(DIST_DIR)
    elif loc_exists and isDir:
        print "Removing directory DIST_DIR"
        shutil.rmtree(DIST_DIR)
    else:
        print "Nothing to remove"


def run_pyinstaller(console=False):
    try:
        if console:
            ## Console Version
            os.system('pyinstaller '
                '--clean '
                '--distpath=%s ' % WIN_DIR +
                '--workpath=%s ' % WORK_DIR +
                '--specpath=%s ' % WIN_DIR +
                '--upx-dir=%s ' % BASE_DIR +
                '--icon=%s ' % WIN_ICON_FILE +
                '--version-file=%s ' % VERSION_FILE +
                # '--onefile '
                '--noconfirm ' + APP_FILE)
        else:
            ## Non Console Version
            val = os.system('pyinstaller '
                '--clean '
                '--distpath=%s ' % WIN_DIR +
                '--workpath=%s ' % WORK_DIR +
                '--specpath=%s ' % WIN_DIR +
                '--upx-dir=%s ' % BASE_DIR +
                '--icon=%s ' % WIN_ICON_FILE +
                # '--onefile '
                '--version-file=%s ' % VERSION_FILE +
                '--noconsole '
                '--noconfirm ' + APP_FILE)

        return True
    except Exception as e:
        print (e)
        return False

def mac_pyinstaller():
    try:
        os.system('pyinstaller '
            '--clean '
            '--distpath=%s ' % MAC_DIST_DIR +
            '--workpath=%s ' % MAC_WORK_DIR +
            '--specpath=%s ' % MAC_DIR +
            '--upx-dir=%s ' % BASE_DIR +
            '--icon=%s ' % MAC_ICON_FILE +
            '--version-file=%s ' % VERSION_FILE +
            '--windowed '#'--onefile '
            '--noconfirm ' + APP_FILE)

        #copy "libwx_osx_cocoau-3.0.0.0.0.dylib"
        os.system("cp /anaconda/envs/odmtools/lib/libwx_osx_cocoau-3.0.0.0.0.dylib %s" % os.path.join(APP_DIR, "Contents/MacOS/"))

        return True
    except Exception as e:
        print (e)
        return False

def move_to_dist(filename):
    assert filename

    if not os.path.isdir(DIST_DIR):
        os.mkdir(DIST_DIR)

    print "Moving {filename} to {dist}".format(filename=os.path.abspath(filename), dist=DIST_DIR),
    try:
        shutil.move(os.path.abspath(filename), DIST_DIR)
        print "Success"
    except shutil.Error as e:
        print (e)


def run_inno(script = None):
    if script is not None:
        os.system(INNO_EXECUTABLE + " " + script)
    else:
        os.system(INNO_EXECUTABLE + " " + INNO_SCRIPT)

def run_no_installer():
    # Need to finish, Not functional
    raise ("Not functional yet")
    filename = obtain_exe_filename()

    zipdir(BASE_DIR, filename)
    move_to_dist(filename)


def run_iceberg():
    os.system(ICE_EXECUTABLE + " "+ ICE_SCRIPT)

def main():
    delete_old_out_dir()
    printInfo()

    if sys.platform == 'win32':

        print "Creating Windows Executable..."
        if run_pyinstaller():
            scriptpath = os.path.join(WIN_DIR, "odmtools_no_console.iss")
            run_inno(script= scriptpath)

        print "Creating Windows Executable Console..."
        if run_pyinstaller(console=True):
            scriptpath = os.path.join(WIN_DIR, "odmtools_console.iss")
            run_inno(scriptpath)

        print "Create No Installer "

        ## Create Shortcut
        ## Create File
        ## Zip Executable


    elif sys.platform =='darwin':
        if(mac_pyinstaller()):
            run_iceberg()

    # elif sys.platform == 'linux2':
    #     ## Testing, not officially supported
    #     run_no_installer()


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
