ODMToolsPython
==============

ODMTools is a python application for managing observational data using the Observations Data Model. ODMTools allows you to query, visualize, and edit data stored in an Observations Data Model (ODM) database. ODMTools was originally developed as part of the CUAHSI Hydrologic Information System.

<p align="center"><img src="https://github.com/UCHIC/ODMToolsPython/raw/master/doc/images/ODMToolsScreenShot.jpg"></p>

Sponsors
---------
This project is receiving or has received support from a number of agencies and complementary efforts including:

![iUTAH](/doc/images/iutah_eu_horz_sm.png)    ![CUAHSI](/doc/images/cuahsi_logo_sm.gif)    ![NSF](/doc/images/nsf.gif)

This material is based on work supported by the National Science Foundation Grant EPS 1208732 awarded to Utah State University.  Additional support was previously provided by National Science Foundation grant EAR 0622374.  Any opinions, findings, and conclusions or recommendations expressed are those of the author(s) and do not necessarily reflect the views of the National Science Foundation.

Running From Source on Windows
-------------------
Install the following software/libraries. Unfortunately this is currently a manual process. 

+	[Python-2.7 32 bit](http://www.python.org/download/releases/2.7.3/)
+	[Wxpython-2.9.4](http://www.wxpython.org/download.php)
+	[Sqlalchemy-7.9](http://pypi.python.org/pypi/SQLAlchemy/0.7.9)
+   [Pyodbc-3.0.6](http://code.google.com/p/pyodbc/downloads/list) 
+	[PyMySQL](https://github.com/petehunt/PyMySQL/)
+	[Matplotlib-1.1.1](https://github.com/matplotlib/matplotlib/downloads)
+	[Numpy-1.6.2](http://www.scipy.org/Download)
+	[Object List Viewer-1.2](http://sourceforge.net/projects/objectlistview/files/objectlistview-python/)

Once you have all the dependencies installed, run the main application by doing 
    
    python src/Gui/frmODMToolsMain.py

Please let us know if you have any problems!

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


