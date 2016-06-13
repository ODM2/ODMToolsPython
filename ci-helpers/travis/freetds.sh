#!/bin/bash
ls /usr/lib/x86_64-linux-gnu/odbc/
echo "[FreeTDS]"> .odbcinst.ini
echo "Description = v0.91 with protocol v7.2">> .odbcinst.ini
echo "Driver = /usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so">> .odbcinst.ini
sudo odbcinst -i -d -f .odbcinst.ini
echo "[azure]" > azure.odbc
echo "Server = nrb8xkgxaj.database.windows.net" >> azure.odbc
echo "Driver      = FreeTDS" >> azure.odbc
echo "Database = odm2" >> azure.odbc
sudo odbcinst -i -s -l -f azure.odbc
echo "[moonstone]" > moonstone.odbc
echo "Server = moonstone.sdsc.edu" >> moonstone.odbc
echo "Driver      = FreeTDS" >> moonstone.odbc
echo "Database = odm2" >> moonstone.odbc
sudo odbcinst -i -s -l -f moonstone.odbc
  # free tds
sudo echo "[FreeTDS]" >> odbcinst.ini
sudo echo "Description = v0.91 with protocol v7.2" >> odbcinst.ini
sudo echo "Driver = /usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so " >> odbcinst.ini
#sudo echo "Setup = $HOME/oob/client/libesoobsetup.so >> odbcinst.ini
#sudo echo "FileUsage = 1" >> odbcinst.ini
  # - ls -al /etc/odbcinst.ini /etc/odbc.ini
cat /etc/odbcinst.ini
cat  /etc/odbc.ini
 # - ls /etc/ODBCDataSources
 # - cat  .odbc.ini #not found
  #
echo "[global]" > .freetds.conf
echo "tds version = 4.2" >> .freetds.conf
echo "[kyle]" >> .freetds.conf
echo "host = nrb8xkgxaj.database.windows.net" >> .freetds.conf
echo "port = 1433" >> .freetds.conf
echo "database=odm2" >> .freetds.conf
echo "[moonstone]">> .freetds.conf
echo "host = moonstone.sdsc.edu">> .freetds.conf
echo "port = 1433">> .freetds.conf
echo "database=odm2" >> .freetds.conf
cat .freetds.conf