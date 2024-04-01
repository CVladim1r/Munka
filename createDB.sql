CREATE DATABASE IF NOT EXISTS JFDataBase;

USE JFDataBase;

CREATE TABLE IF NOT EXISTS `employers` (
  `employer_id` int NOT NULL AUTO_INCREMENT,
  `employer_username` varchar(32) DEFAULT NULL,
  `employer_name` varchar(255) DEFAULT NULL,
  `company_name` varchar(255) DEFAULT NULL,
  `description` text,
  `employer_type` enum('EMPLOYER','USER') DEFAULT NULL,
  PRIMARY KEY (`employer_id`),
  UNIQUE KEY `employer_username` (`employer_username`)
) ENGINE=InnoDB AUTO_INCREMENT=1202021369 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `vacancies` (
  `id` int NOT NULL AUTO_INCREMENT,
  `description` text,
  `name` varchar(255) DEFAULT NULL,
  `user_name` varchar(255) DEFAULT NULL,
  `age_for_vacancies` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

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
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `nickname` (`nickname`),
  UNIQUE KEY `nickname_2` (`nickname`)
) ENGINE=InnoDB AUTO_INCREMENT=2092442718 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `plug_users` (
  `user_id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `user_username` varchar(255) UNIQUE,
  `user_name` varchar(255)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
