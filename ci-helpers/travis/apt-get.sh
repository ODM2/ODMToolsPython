#!/bin/bash

sudo apt-get install -y python-software-properties
sudo apt-add-repository -y ppa:git-core/ppa
sudo apt-add-repository -y ppa:ubuntugis/ppa
sudo apt-get update -qq
sudo apt-get install unixodbc  unixodbc-dev odbcinst1debian2 odbcinst
sudo apt-get install freetds-dev freetds-bin tdsodbc
sudo apt-get install libc6  e2fsprogs  # mssql driver
sudo apt-get install mysql-client
  # Spatialite
sudo apt-get install -y libproj-dev libgeos-dev libspatialite-dev
sudo ln -s /usr/lib/x86_64-linux-gnu/libspatialite.so /usr/lib/libspatialite.so
#  - sudo apt-get install python-scipy python-matplotlib python-pandas python-sympy python-nose
sudo apt-get install python-matplotlib python-pandas python-nose