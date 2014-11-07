ODMToolsPython
==============

Get started by visiting the [ODM Tools Documentation] (https://github.com/UCHIC/ODMToolsPython/wiki/ODMTools-Python-Documentation) page.

ODMTools is a python application for managing observational data using the Observations Data Model. ODMTools allows you to query, visualize, and edit data stored in an Observations Data Model (ODM) database. ODMTools was originally developed as part of the CUAHSI Hydrologic Information System.

<p align="center"><img src="https://github.com/UCHIC/ODMToolsPython/raw/master/doc/images/ODMToolsScreenShot.jpg"></p>

##Releases

To make running ODMTools easier we have included installers. Please select the one that is appropriate for your operating system

####Windows
Recommended Release: 
+   [Beta v1.0 ] (https://github.com/UCHIC/ODMToolsPython/releases/tag/v1.0-beta)

Developmental Release:
+	[Developmental v0.1](https://github.com/UCHIC/ODMToolsPython/releases/tag/win_v0.1_exp)

####Mac
+   *Coming Soon*

####Linux
+   *Please run from source*

Running From Source
-------------------

+	[Matplotlib-1.3.1](https://github.com/matplotlib/matplotlib/releases/tag/v1.3.1)
+	[Pandas-0.15.0](https://github.com/pydata/pandas/releases)
+	[Pip](http://docs.python-guide.org/en/latest/starting/install/win.html)
+	[PyMySQL] (https://github.com/petehunt/PyMySQL/)
+	[Pyodbc-3.0.7](https://code.google.com/p/pyodbc/downloads/detail?name=pyodbc-3.0.7.win-amd64-py2.7.exe)
+	[Python-2.7.8 x64/x32](http://www.python.org/download/releases/2.7.3/) (Python 3 version isn't available)
+	[Psycopg2-2.4.6](http://initd.org/psycopg/docs/install.html)
+	[Sqlalchemy-0.9.7] (http://pypi.python.org/pypi/SQLAlchemy/0.9.7)
+	[wxpython-3.0.0](http://www.wxpython.org/download.php)

Install the following software/libraries. 
It is recommended to create an environment using 'Conda'. 
'Conda' comes prepackaged in the Python Scientific Package Suite [Anaconda](http://continuum.io/downloads) (Available for Windows, OSX, Linux)

Example environment creation:

+   conda create -n odmtools python=2.7.8 wxpython matplotlib pandas pyodbc sqlalchemy pip psycopg2

+   pip install pymysql


if psycopg2 isn't found, download it manually and follow these [directions](https://stackoverflow.com/questions/5420789/how-to-install-psycopg2-with-pip-on-python)

Once you have downloaded the source code and all the dependencies installed, run the main application:
    
    python odmtools/ODMToolsPython.py

Sponsors
---------
This project is receiving or has received support from a number of agencies and complementary efforts including:

![iUTAH](/doc/images/iutah_eu_horz_sm.png)    ![CUAHSI](/doc/images/cuahsi_logo_sm.gif)    ![NSF](/doc/images/nsf.gif)

This material is based on work supported by the National Science Foundation Grant EPS 1208732 awarded to Utah State University.  Additional support was previously provided by National Science Foundation grant EAR 0622374.  Any opinions, findings, and conclusions or recommendations expressed are those of the author(s) and do not necessarily reflect the views of the National Science Foundation.

Copying and License
----------------------------

This material is copyright (c) 2013 Utah State University.

It is open and licensed under the New Berkeley Software Distribution (BSD) License.  Full text of the license follows.

Copyright (c) 2013, Utah State University. All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

*  Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
*  Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
*  Neither the name of Utah State University nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE. 


