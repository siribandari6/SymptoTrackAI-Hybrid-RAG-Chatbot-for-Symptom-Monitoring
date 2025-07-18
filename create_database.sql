CREATE DATABASE IF NOT EXISTS symptoms;
USE symptoms;

CREATE TABLE IF NOT EXISTS register(
    username VARCHAR(50) PRIMARY KEY,
    password VARCHAR(50),
    contact_no VARCHAR(20),
    email VARCHAR(50), 
    address VARCHAR(80)
);

CREATE TABLE IF NOT EXISTS log(
    username VARCHAR(50),
    symptoms_text VARCHAR(400),
    predicted_advice VARCHAR(60),
    checked_date VARCHAR(40)
);

SHOW TABLES;
