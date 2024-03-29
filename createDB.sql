CREATE DATABASE IF NOT EXISTS JFDataBase;

USE JFDataBase;

CREATE TABLE IF NOT EXISTS USERS (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_type ENUM('EMPLOYER', 'USER') NOT NULL,
    user_name VARCHAR(255) UNIQUE,
    name VARCHAR(255),
    age INT,
    description TEXT,
    company_name VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS VACANCIES (
    id INT AUTO_INCREMENT PRIMARY KEY,
    description TEXT,
    name VARCHAR(255),
    user_name VARCHAR(255),
    age_for_vacancies INT,
);