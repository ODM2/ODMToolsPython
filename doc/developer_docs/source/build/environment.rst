=======================
Creating an environment
=======================

Windows
=======

In order to create an environment on Windows, the easiest way is to use Anaconda_. Conda will create an environment when the command **conda create -n <environment_name> <packages>** is used.


::
    
    conda create -n odmtools python=2.7.9 wxpython matplotlib pandas pyodbc sqlalchemy pip psycopg2

    pip install pymysql

Activate the environment

::

    activate odmtools

Run ODMTools by running the following command

:: 

    python ODMTools.py

Troubleshooting
~~~~~~~~~~~~~~~
.. warning::
    If you are unable to get psycopg2, please go to psycopg2's website_ and download the installer and follow these steps after you activate the environment.

    easy_install psycopg2-2.5.win32-py2.7-pg9.2.4-release.exe

.. _Anaconda: http://continuum.io/downloads
.. _website: http://stickpeople.com/projects/python/win-psycopg/
