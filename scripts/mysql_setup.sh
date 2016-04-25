ls -al /etc/mysql
sudo service mysql stop
# lower-case-table-names = 1 leaving lower_case_table_names=1 since that is what the docs say
 echo "[mysqld]" > $HOME/.my.cnf
 echo "lower-case-table-names = 1" >> $HOME/.my.cnf
# echo "lower_case_table_names=1" >> $HOME/.my.cnf
cat $HOME/.my.cnf # be sure it registered
service --status-all
#  this should have worked.
sudo sed -i '/\[mysqld\]/a lower_case_table_names = 1 ' /etc/mysql/my.cnf
cat /etc/mysql/my.cnf
sudo service mysql start
mysql --verbose -e  "show variables like 'lower%';" --user=root

#strace mysql 2>&1 | grep cnf # will tell you what files are being used
mysql --verbose -e "CREATE USER 'ODM'@'localhost' IDENTIFIED BY 'odm';GRANT ALL PRIVILEGES ON *.* TO 'ODM'@'localhost';" --user=root
mysql --verbose -e "CREATE USER 'ODM'@'127.0.0.1' IDENTIFIED BY 'odm';GRANT ALL PRIVILEGES ON *.* TO 'ODM'@'127.0.0.1';" --user=root
mysql --verbose -e "CREATE USER 'ODM'@'%' IDENTIFIED BY 'odm';GRANT ALL PRIVILEGES ON *.* TO 'ODM'@'%';" --user=root
mysql  --verbose  -e "create database IF NOT EXISTS odm2;" --user=root
mysql -e "create database IF NOT EXISTS odm2test;" --user=root
#####
# install
#####
ls -al  ./tests/usecasesql/littlebearriver/sampledatabases/odm2_mysql/LBR_MySQL_SmallExample.sql ./tests/usecasesql/marchantariats/marchantariats.sql
mysql --user=ODM --password=odm  odm2 < ./tests/usecasesql/littlebearriver/sampledatabases/odm2_mysql/LBR_MySQL_SmallExample.sql
mysql --user=root  -e  "show databases;"
mysql --user=root -e   "GRANT ALL PRIVILEGES ON odm2.* TO 'ODM'@'localhost';FLUSH PRIVILEGES;"
# these should produce results, if they don't the lower_case_table_names failed
# should make them grep or sed for some keywords
mysql --user=ODM --password=odm odm2 -e "use odm2; Select * from Variables;"
mysql --user=ODM --password=odm odm2 -e "Select * from odm2.Variables;"
mysql --user=ODM --password=odm  -e "Select * from odm2.Variables;"