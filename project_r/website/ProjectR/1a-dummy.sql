CREATE TABLE 'users' (
  'user_id' bigint(20) NOT NULL,
  'user_name' varchar(255) NOT NULL) 
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

ALTER TABLE 'users'
  ADD PRIMARY KEY ('user_id'),
  ADD KEY 'user_name' ('user_name');

ALTER TABLE 'users'
  MODIFY 'user_id' bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

INSERT INTO 'users' ('user_id', 'user_name') VALUES
(1, 'Joe Doe'),
(2, 'Jon Doe'),
(3, 'Joy Doe');

