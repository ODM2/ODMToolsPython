ODMToolsPython
==============

Get started by visiting the [ODM Tools Documentation] (https://github.com/ODM2/ODMToolsPython/wiki/ODMTools-Python-Documentation) page.

ODMTools is a python application for managing observational data using the Observations Data Model. ODMTools allows you to query, visualize, and edit data stored in an Observations Data Model (ODM) database. ODMTools was originally developed as part of the CUAHSI Hydrologic Information System.

<p align="center"><img src="https://github.com/ODM2/ODMToolsPython/raw/master/doc/images/ODMToolsScreenShot.jpg"></p>

If you want to try ODM Tools, we have created a couple of [testing databases](https://github.com/ODM2/ODMToolsPython/tree/master/examples) that you can use.

## ODM Compatibility

ODM Tools Python is currenlty fully compatible with ODM Version 1.1.1. We are working on ODM2 compatibility, and should have it worked out this winter.

## Releases

To make running ODMTools easier we have included installers. Please select the one that is appropriate for your operating system

#### Windows
Recommended Release:
+   [Window v1.2.8-beta](https://github.com/ODM2/ODMToolsPython/releases/download/v1.2.8_beta/ODMTools_v1.2.8-beta_Installer.exe)

#### Mac
+   [Mac v1.2.8-beta](https://github.com/ODM2/ODMToolsPython/releases/download/v1.2.8_beta/ODMTools_v1.2.8-beta_Mac_installer.pkg.zip)

#### Linux
+   *Please run from source*

Running From Source
-------------------

+	[Matplotlib](https://github.com/matplotlib/matplotlib/releases/)
+	[Pandas](https://github.com/pydata/pandas/releases)
+	[Pip](http://docs.python-guide.org/en/latest/starting/install/win.html)
+	[PyMySQL](https://github.com/petehunt/PyMySQL/)
+	[Pyodbc](https://code.google.com/p/pyodbc/downloads/)
+	[Python-2.7.9 x64/x32](http://www.python.org/download/releases/2.7.9/) (Python 3 version isn't available)
+	[Psycopg2](http://initd.org/psycopg/docs/install.html)
+	[Sqlalchemy] (http://pypi.python.org/pypi/SQLAlchemy/)
+	[wxpython](http://www.wxpython.org/download.php)
+	[Numpy](http://www.scipy.org/scipylib/download.html)
+	[Scipy](https://www.scipy.org/scipylib/download.html)

Install the following software/libraries.
It is recommended to create an environment using 'Conda'.
'Conda' comes prepackaged in the Python Scientific Package Suite [Anaconda](http://continuum.io/downloads) (Available for Windows, OSX, Linux)

Example environment creation:

+   conda create -n odmtools python=2.7.8 wxpython matplotlib pandas numpy scipy pyodbc sqlalchemy pip psycopg2

+   pip install pymysql


if psycopg2 isn't found, download it manually and follow these [directions](https://stackoverflow.com/questions/5420789/how-to-install-psycopg2-with-pip-on-python)

Once you have downloaded the source code and all the dependencies installed, run the main application:

    python ODMTools.py

if installing pyodbc onto a Mac machine please follow these instructions:

pyodbc Configuration
Download the source code ​[here](https://code.google.com/p/pyodbc/downloads/detail?name=pyodbc-3.0.7.zip&can=2&q=)​.
Unzip the directory where ever you want.
Edit ​setup.py​ within the pyodbc directory.
Look for the line that says “OS/X now ships with iODBC.” Right underneath that, remove the letter i from the statement:

    settings[‘libraries’].append(‘iodbc’)

so that it reads:

    settings[‘libraries’].append(‘odbc’)

Now that the setup.py file is configured correctly, pyodbc is ready to be installed. From your virtual environment, do a pip install of pyodbc and use the modified package.

    pip install -e PATH_TO_PYODBC


Sponsors
---------
This project is receiving or has received support from a number of agencies and complementary efforts including:

![iUTAH](/doc/images/iutah_eu_horz_sm.png)    ![CUAHSI](/doc/images/cuahsi_logo_sm.gif)    ![NSF](/doc/images/nsf.gif)

This material is based on work supported by the National Science Foundation Grants [IIA-1208732](http://www.nsf.gov/awardsearch/showAward?AWD_ID=1208732), [ACI-1339834](http://www.nsf.gov/awardsearch/showAward?AWD_ID=1339834), and [EAR-1224638](http://www.nsf.gov/awardsearch/showAward?AWD_ID=1224638).  Additional support was previously provided by National Science Foundation grant [EAR-0622374](http://www.nsf.gov/awardsearch/showAward?AWD_ID=0622374).  Any opinions, findings, and conclusions or recommendations expressed are those of the author(s) and do not necessarily reflect the views of the National Science Foundation.
