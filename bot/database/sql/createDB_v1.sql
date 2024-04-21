CREATE DATABASE IF NOT EXISTS JFDataBase;

USE JFDataBase;

CREATE TABLE IF NOT EXISTS `employers` (
  `employer_id` int NOT NULL AUTO_INCREMENT,
  `employer_username` varchar(32) DEFAULT NULL,
  `employer_name` varchar(255) DEFAULT NULL,
  `company_name` varchar(255) DEFAULT NULL,
  `description` text,
  `employer_type` enum('EMPLOYER','USER') DEFAULT NULL,
  `city` varchar(255) DEFAULT NULL,
  `desired_position` varchar(255) DEFAULT NULL,
  `vacancy_title` varchar(255) DEFAULT NULL,
  `company_description` text,
  `responsibilities` text,
  `requirements` text,
  `working_conditions` text,
  `image_path` varchar(255),
  PRIMARY KEY (`employer_id`),
  UNIQUE KEY `employer_username` (`employer_username`)
) ENGINE=InnoDB AUTO_INCREMENT=1202021369 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `vacancies` (
  `vacancy_id` INT NOT NULL AUTO_INCREMENT,
  `vacancy_title` VARCHAR(255) DEFAULT NULL,
  `company_name` VARCHAR(255) DEFAULT NULL,
  `vacancy_url` VARCHAR(255) DEFAULT NULL,
  `created_date` DATE DEFAULT NULL,
  `employment` VARCHAR(255) DEFAULT NULL,
  `working_time_modes` TEXT,
  `experience` VARCHAR(255) DEFAULT NULL,
  `salary_info` VARCHAR(255) DEFAULT NULL,
  `description` TEXT,
  `skills` JSON,
  PRIMARY KEY (`vacancy_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

USE JFDataBase;

CREATE TABLE IF NOT EXISTS `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `user_type` enum('EMPLOYER','USER') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `age` int DEFAULT NULL,
  `description` text,
  `location` varchar(100) DEFAULT NULL,
  `nickname` varchar(32) DEFAULT NULL,
  `user_fullname` varchar(255) DEFAULT NULL,
  `user_dob` date DEFAULT NULL,
  `citizenship` varchar(100) DEFAULT NULL,
  `skills` text,
  `experience` varchar(100) DEFAULT NULL,
  `experience_description` varchar(100) DEFAULT NULL,
  `additional_info` text,
  `photo_path` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `nickname` (`nickname`)
);
ENGINE=InnoDB AUTO_INCREMENT=2092442718 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE IF NOT EXISTS `plug_users` (
  `user_id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `user_username` varchar(255) UNIQUE,
  `user_name` varchar(255)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
