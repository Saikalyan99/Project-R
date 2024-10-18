##  Setup Server  ##
sudo apt install mysql-server
sudo apt install mysql-client

sudo mysqld_safe --skip-grant-tables &
sudo mysql -u root

# SQL instructions
FLUSH PRIVILEGES;
USE mysql;
ALTER USER 'root'@'localhost' IDENTIFIED BY 'Pr0jectR';
SET GLOBAL local_infile=1;
FLUSH PRIVILIGES;
QUIT
# End SQL

sudo service mysql stop
sudo service mysql start

mysql -u root -h 127.0.0.1 -p


##  Export Database  ##
mysqldump -u root database_name -p > database_dump.sql
# Where "database_name" is the name of the database and "database_dump.sql" is the name of your file


##  Import Database  ##
mysql -u root -h 127.0.0.1 -p

CREATE DATABASE database_name;
exit

mysql -u root database_name -p < database_dump.sql
# Where "database_name" is the name of the database and "database_dump.sql" is the name of your file


##  Create New User  ##
mysql -u root -h 127.0.0.1 -p

CREATE USER 'username'@'host'
  IDENTIFIED BY 'password';
  
GRANT CREATE, ALTER, DROP, INSERT, UPDATE, DELETE, SELECT, REFERENCES, RELOAD on *.* TO 'sammy'@'localhost' WITH GRANT OPTION;
# 'WITH GRANT OPTION' allows 'sammy' to GRANT any permissions they have to other users on the system.
GRANT ALL PRIVILEGES ON *.* TO 'sammy'@'localhost' WITH GRANT OPTION;
# '*.*' is permission on any database and any table


##  Websites for connecting database to website  ##
# https://www.sitepoint.com/mysql-data-web/
# https://code-boxx.com/connect-database-javascript/