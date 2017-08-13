Example ODM Databases
=====================

This folder contains two example databases for use in testing ODM Tools Python. Each database contains a subset of continuous sensor data collected in the Little Bear River of northern Utah, USA. If you need help connecting to one of these example databases, refer to the appropriate [documentationn](https://github.com/ODM2/ODMToolsPython/blob/master/doc/MarkdownFiles/DatabaseConnections.md).

### LittleBear_ODM_1.1.1_MSSQL.zip ###
This zip file contains a Microsoft SQL Server database. It was created in Microsoft SQL Server 2005, but should be compatible with SQL Server 2008 and 2012. To use it, do the following:

1. Extract the contents of the zip file to the Microsoft SQL Server data directory
2. Attach the database to your SQL Server instance (the Express version will work)
3. Create an appropriate SQL server user that has access to the database so you can connect using ODM Tools 

### LittleBear_ODM_1.1.1_MySQL.sql ###

This zipped file contains a MySQL dump file to create the testing database in MySQL. To use it, do the following:

1. Extract the zipped file to a location on your hard drive. 
2. Using MySQL workbench or some other tool, create a new schema in MySQL
3. Execute the MySQL dump file (the SQL script) on the new schema you created
4. Create an appropriate MySQL user that has access to the database so you can connect using ODM Tools

