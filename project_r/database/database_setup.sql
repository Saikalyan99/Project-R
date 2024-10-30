CREATE DATABASE IF NOT EXISTS ProjectR;
USE ProjectR;

-- Table Creation (now done by Python)
-- I left it here for a quick understanding of
-- the tables' setup

CREATE TABLE stores (
    id INT(11) PRIMARY KEY auto_increment,
    name VARCHAR(255) NOT NULL,
    rating FLOAT(2,1),
    numrating INT(11),
    streetnum VARCHAR(50) NOT NULL,
    streetname VARCHAR(50) NOT NULL,
    aptnum VARCHAR(50),
    city VARCHAR(200) NOT NULL,
    state VARCHAR(15) NOT NULL,
    zip INT(5) NOT NULL,
    country VARCHAR(20) NOT NULL,
    pluscode CHAR(20)
);

CREATE TABLE tags (
    id INT(4) PRIMARY KEY auto_increment,
    name VARCHAR(20) NOT NULL
);

CREATE TABLE store_tags (
    storeid INT(11) NOT NULL,
    FOREIGN KEY (storeid)
        REFERENCES stores(id),
    tagid INT(4) NOT NULL,
    FOREIGN KEY (tagid)
        REFERENCES tags(id)
);



-- Get a list of all the stores in ID order with each tag they have
SELECT S.name AS Store, T.name AS Tag
FROM stores S
JOIN store_tags ST ON S.id = ST.storeid
JOIN tags T ON T.id = ST.tagid
ORDER BY S.id;

-- Create Users
CREATE ROLE 'app_developer',
            'app_read',
            'app_write';
GRANT ALL
    ON ProjectR.* TO 'app_developer';
GRANT SELECT
    ON ProjectR.* TO 'app_read';
GRANT INSERT,
      UPDATE,
      DELETE
    ON ProjectR.* TO 'app_write';

CREATE USER
    'nathanki' IDENTIFIED WITH caching_sha2_password
            BY '12345678',
    'saikarum' IDENTIFIED WITH caching_sha2_password
            BY '12345678',
    'sarahmel' IDENTIFIED WITH caching_sha2_password
            BY '12345678'
    PASSWORD EXPIRE INTERVAL 60 DAY
    PASSWORD EXPIRE
    PASSWORD HISTORY 1
    FAILED_LOGIN_ATTEMPTS 3 PASSWORD_LOCK_TIME 1;

GRANT 'app_developer' TO 'nathanki', 'saikarum', 'sarahmel';
SET DEFAULT ROLE 'app_developer' TO 'nathanki', 'saikarum', 'sarahmel';

-- Before people can start typing commands, they'll need to use the following command to change their password
-- ALTER USER 'nathanki' IDENTIFIED BY 'new_password';

    
-- DROP USER 'nathanki', 'saikarum', 'sarahmel';
-- DROP ROLE 'app_developer', 'app_read', 'app_write';