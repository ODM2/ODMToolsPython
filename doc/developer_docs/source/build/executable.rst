====================================
Building an ODMTools Executable
====================================

Windows
=======

Requirements for creating an executable in Windows Python 2.7 x32

.. Note::
        Please be sure to have a fully working ODMTools environment to proceed

Installing py2exe
#################

    Ensure that you have pyzmq and py2exe installed:

    ::

        pip install -U pyzmq

    Install py2exe for python 2.7 32x from the SourceForge_ page

    ::

        easy_install py2exe-0.6.9.win32-py2.7.exe


Installing using pyinstaller
############################

    Use the development version of pyinstaller. This fixes a lot of issues that the official release doesn't address yet.

    .. Note::
            While pyinstaller is a very promising alternative to py2exe/py2app, it isn't available for python 3 just yet.

    ::

        git clone https://github.com/pyinstaller/pyinstaller.git



    Install pywin32 if you are using Python 2.6+

        Install pywin32 from `here <http://sourceforge.net/projects/pywin32/>`_

        ::

            easy_install pywin32-219.win-amd64-py2.7.exe

    Install Microsoft C++ Redistributable either 2008 or 2010 x86/x64 from https://www.microsoft.com/en-us/download/details.aspx?id=29
        Install it to your system

    See the `Example <https://mborgerson.com/creating-an-executable-from-a-python-script/>`_ to see how a simple wxpython application can be built with pyinstaller

    .. Note::
            I have only had success using Python 32x/86x for creating applications.

    .. Warning::
            Prepare to do a lot of googling as there are a lot of features that aren't clear

    .. Warning::
            Make sure that you close command prompt and reopen it if you installed any of these packages/software

    Here is an example of building a program. There isn't a messy setup.py needed unlike py2exe. These are automatically generated when a user runs the command

    ::

        pyinstaller <path_to_file>


Building an Executable for ODMTools in Windows
##############################################

    If you're planning on building an executable, it is best to have a virtualenv already setup.

    Unfortunately running the '--onefile' argument doesn't work just yet. So, you'll have to navigate through the long list of included files to find the executable.

    Here is the working command while trying to build ODMTools in Windows 8.1

    ::

        pyinstaller --distpath="setup/Windows" --workpath="setup/Windows/work" --hidden-import=pyodbc ODMTools.py


    The pyodbc module needs to be manually added into this command because the installer won't be able to determine whether this import is needed or not.











.. _SourceForge: http://sourceforge.net/projects/py2exe/files/?source=navbar


