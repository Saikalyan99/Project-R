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

mysql -u root -p