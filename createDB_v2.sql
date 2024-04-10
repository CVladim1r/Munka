CREATE DATABASE IF NOT EXISTS JFDataBasev1;

USE JFDataBasev1;

-- Создание таблицы employers
CREATE TABLE IF NOT EXISTS `employers` (
  `employer_id` int NOT NULL AUTO_INCREMENT,
  `employer_username` varchar(32) DEFAULT NULL,
  `employer_name` varchar(255) DEFAULT NULL,
  `employer_company_name` varchar(255) DEFAULT NULL,
  `employer_description` text,
  `employer_type` enum('EMPLOYER','USER') DEFAULT NULL,
  `employer_city` varchar(255) DEFAULT NULL,
  `employer_desired_position` varchar(255) DEFAULT NULL,
  `employer_vacancy_title` varchar(255) DEFAULT NULL,
  `employer_company_description` text,
  `employer_responsibilities` text,
  `employer_requirements` text,
  `employer_working_conditions` text,
  `employer_image_path` varchar(255),
  PRIMARY KEY (`employer_id`),
  UNIQUE KEY `employer_username` (`employer_username`)
) ENGINE=InnoDB AUTO_INCREMENT=1202021369 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Создание таблицы vacancies
CREATE TABLE IF NOT EXISTS `vacancies` (
  `vacancy_id` INT NOT NULL AUTO_INCREMENT,
  `vacancy_title` VARCHAR(255) DEFAULT NULL,
  `vacancy_company_name` VARCHAR(255) DEFAULT NULL,
  `vacancy_url` VARCHAR(255) DEFAULT NULL,
  `vacancy_created_date` DATE DEFAULT NULL,
  `vacancy_employment` VARCHAR(255) DEFAULT NULL,
  `vacancy_working_time_modes` TEXT,
  `vacancy_experience` VARCHAR(255) DEFAULT NULL,
  `vacancy_salary_info` VARCHAR(255) DEFAULT NULL,
  `vacancy_description` TEXT,
  `vacancy_skills` TEXT,
  PRIMARY KEY (`vacancy_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Создание таблицы users
CREATE TABLE IF NOT EXISTS `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `user_tgid` int NOT NULL,
  `user_tgname` varchar(255) DEFAULT NULL,
  `user_fullname` varchar(255) DEFAULT NULL,
  `user_fio` varchar(255) DEFAULT NULL,
  `user_type` enum('EMPLOYER','USER') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `user_age` int DEFAULT NULL,
  `user_description` text,
  `user_location` varchar(100) DEFAULT NULL,
  `user_dob` date DEFAULT NULL,
  `user_citizenship` varchar(100) DEFAULT NULL,
  `user_skills` text,
  `user_desired_position` text,
  `user_experience` varchar(100) DEFAULT NULL,
  `user_experience_description` varchar(100) DEFAULT NULL,
  `user_additional_info` text,
  `user_photo_path` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `user_tgname` (`user_tgname`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- Создание таблицы vacancy_applicants
CREATE TABLE IF NOT EXISTS `vacancy_applicants` (
  `vacancy_applicants_id` INT AUTO_INCREMENT PRIMARY KEY,
  `vacancy_id` INT NOT NULL,
  `user_id` INT NULL,
  FOREIGN KEY (`vacancy_id`) REFERENCES `vacancies` (`vacancy_id`) ON DELETE CASCADE,
  FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Создание триггера для автоматической вставки записей в таблицу vacancy_applicants
CREATE TRIGGER trg_after_insert_vacancies
AFTER INSERT ON vacancies
FOR EACH ROW
    INSERT INTO vacancy_applicants (vacancy_id)
    VALUES (NEW.vacancy_id);

CREATE TABLE IF NOT EXISTS viewed_vacancies (
    user_id INT NOT NULL,
    vacancy_id INT NOT NULL,
    PRIMARY KEY (user_id, vacancy_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (vacancy_id) REFERENCES vacancies(vacancy_id) ON DELETE CASCADE
);

-- Триггер для обновления viewed_vacancies при изменении данных в таблице users
DELIMITER //
CREATE TRIGGER trg_update_viewed_vacancies_users
AFTER INSERT, DELETE, UPDATE ON users
FOR EACH ROW
BEGIN
    -- Если добавлен или удален пользователь, обновляем viewed_vacancies для всех пользователей
    DELETE FROM viewed_vacancies;
    -- Добавление новых записей в viewed_vacancies для всех пользователей
    INSERT INTO viewed_vacancies (user_id, vacancy_id)
    SELECT user_id, vacancy_id
    FROM vacancies;
END;
//
DELIMITER ;
