CREATE DATABASE ProjectR;
USE ProjectR;

-- Table Creation
CREATE TABLE StoreJSON (
    StoreID INT(11) PRIMARY KEY auto_increment,
    JSONdata JSON NOT NULL
);

CREATE TABLE Stores (
    StoreID INT(11) NOT NULL,
    FOREIGN KEY (StoreID)
        REFERENCES StoreJSON(StoreID),
    StoreName VARCHAR(255) NOT NULL,
    Rating FLOAT(2,1),
    RatingNum INT(11)
);

CREATE TABLE Address (
    StoreID INT(11) NOT NULL,
    FOREIGN KEY (StoreID)
        REFERENCES StoreJSON(StoreID),
    StreetNum VARCHAR(50) NOT NULL,
    StreetName VARCHAR(50) NOT NULL,
    AptNum VARCHAR(50),
    CityName VARCHAR(200) NOT NULL,
    StateName VARCHAR(15) NOT NULL,
    ZipCode INT(5) NOT NULL,
    Country VARCHAR(20) NOT NULL,
    PlusCode char(20)
);

CREATE TABLE Tags (
    TagID INT(4) PRIMARY KEY auto_increment,
    TagName VARCHAR(20) NOT NULL
);

CREATE TABLE Store_Tags (
    StoreID INT(11) NOT NULL,
    FOREIGN KEY (StoreID)
        REFERENCES StoreJSON(StoreID),
    TagID INT(11) NOT NULL,
    FOREIGN KEY (TagID)
        REFERENCES Tags(TagID)
);


-- Load JSON Data
Load Data Local Infile '/home/nathan/restaurants.rsv' INTO TABLE StoreJSON(JSONdata);

INSERT INTO Stores (StoreID, StoreName, Rating, RatingNum)
SELECT StoreID,
       JSON_UNQUOTE(JSON_EXTRACT(JSONdata, '$.name')) AS StoreName,
       JSON_EXTRACT(JSONdata, '$.rating') AS Rating,
       JSON_EXTRACT(JSONdata, '$.user_ratings_total') AS RatingNum
FROM StoreJSON;

INSERT INTO Address (StoreID, StreetNum, StreetName,
                     AptNum, CityName, StateName,
                     ZipCode, Country)
SELECT StoreID,
       JSON_UNQUOTE(JSON_EXTRACT(JSONdata, '$.address[0].street_num')) AS StreetNum,
       JSON_UNQUOTE(JSON_EXTRACT(JSONdata, '$.address[0].street_name')) AS StreetName,
       JSON_UNQUOTE(JSON_EXTRACT(JSONdata, '$.address[0].apt_num')) AS AptNum,
       JSON_UNQUOTE(JSON_EXTRACT(JSONdata, '$.address[0].city_name')) AS CityName,
       JSON_UNQUOTE(JSON_EXTRACT(JSONdata, '$.address[0].state_name')) AS StateName,
       JSON_EXTRACT(JSONdata, '$.address[0].zip_code') AS ZipCode,
       JSON_UNQUOTE(JSON_EXTRACT(JSONdata, '$.address[0].country')) AS Country
FROM StoreJSON;


-- Create Users
CREATE ROLE 'app_developer', 'app_read', 'app_write';
GRANT ALL ON ProjectR.* TO 'app_developer';
GRANT SELECT ON ProjectR.* TO 'app_read';
GRANT INSERT, UPDATE, DELETE ON ProjectR.* TO 'app_write';

CREATE USER
    'nathanki'@'localhost' IDENTIFIED WITH caching_sha2_password
            BY '12345678',
    'saikarum'@'localhost' IDENTIFIED WITH caching_sha2_password
            BY '12345678',
    'sarahmel'@'localhost' IDENTIFIED WITH caching_sha2_password
            BY '12345678'
    PASSWORD EXPIRE INTERVAL 60 DAY
    PASSWORD EXPIRE
    PASSWORD HISTORY 1
    FAILED_LOGIN_ATTEMPTS 3 PASSWORD_LOCK_TIME 1;

GRANT 'app_developer' TO 'nathanki'@'localhost', 'saikarum'@'localhost', 'sarahmel'@'localhost';

-- Before people can start typing commands, they'll need to use the following command to change their password
ALTER USER 'nathanki'@'localhost' IDENTIFIED BY 'new_password';



-- Test code
CREATE DATABASE test;
USE test;
CREATE TABLE jsontest (
    id INT(11) PRIMARY KEY auto_increment,
    first VARCHAR(10),
    last VARCHAR(10),
    age INT(3),
    money FLOAT(12,2),
    jsondata JSON
);

LOAD DATA LOCAL infile '/home/nathan/test.json' INTO TABLE jsontest(jsondata);
UPDATE jsontest SET
    first=(jsondata->>'$.fname'),
    last=(jsondata->>'$.lname'),
    age=(jsondata->>'$.age'),
    money=(jsondata->>'$.money');



CREATE USER
    'nathan'@'localhost' IDENTIFIED WITH caching_sha2_password
            BY 'mdNUgL2a6GMxc9n'
    PASSWORD EXPIRE INTERVAL 60 DAY
    PASSWORD EXPIRE
    PASSWORD HISTORY 1
    FAILED_LOGIN_ATTEMPTS 3 PASSWORD_LOCK_TIME 1;