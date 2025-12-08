-- Create database (change name if you want)
CREATE DATABASE IF NOT EXISTS client_query_db;
USE client_query_db;

-- Users table for login (Client / Support)
CREATE TABLE IF NOT EXISTS users (
    username VARCHAR(100) PRIMARY KEY,
    hashed_password VARCHAR(255) NOT NULL,
    role ENUM('Client', 'Support') NOT NULL,
    mobile_number VARCHAR(20) NOT NULL
);

-- Queries table
CREATE TABLE IF NOT EXISTS queries (
    query_id varchar(100) PRIMARY KEY,
    client_email VARCHAR(255) NOT NULL,
    client_mobile VARCHAR(20) NOT NULL,
    query_heading VARCHAR(255) NOT NULL,
    query_description TEXT NOT NULL,
    status ENUM('Open', 'Closed') NOT NULL DEFAULT 'Open',
    date_raised DATETIME NOT NULL,
    date_closed DATETIME NULL
);