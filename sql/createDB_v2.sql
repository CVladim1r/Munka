CREATE DATABASE IF NOT EXISTS JFDataBase;

USE JFDataBase;

-- Создание таблицы employers
CREATE TABLE IF NOT EXISTS `employers` (
  `employer_id` int NOT NULL AUTO_INCREMENT,
  `employer_username` varchar(32) DEFAULT NULL,
  `employer_name` varchar(255) DEFAULT NULL,
  `company_name` varchar(255) DEFAULT NULL,
  `description` text,
  `employer_type` enum('EMPLOYER','USER') DEFAULT NULL,
  `city` varchar(255) DEFAULT NULL,
  `desired_position` varchar(255) DEFAULT NULL,
  `company_description` text,
  `responsibilities` text,
  `requirements` text,
  `working_conditions` text,
  `image_path` varchar(255),
  PRIMARY KEY (`employer_id`),
  UNIQUE KEY `employer_username` (`employer_username`)
) ENGINE=InnoDB AUTO_INCREMENT=1202021369 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Создание таблицы vacancies
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
  `skills` TEXT,
  PRIMARY KEY (`vacancy_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1202021369 DEFAULT CHA RSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Создание таблицы users
CREATE TABLE IF NOT EXISTS `users` (
  `id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `user_id` INT AUTO_INCREMENT,
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
  PRIMARY KEY (`id`),
  UNIQUE KEY `nickname` (`nickname`)
) ENGINE=InnoDB AUTO_INCREMENT=2092442718 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Создание таблицы vacancy_applicants
CREATE TABLE IF NOT EXISTS `vacancy_applicants` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `vacancy_id` INT NOT NULL,
  `user_id` INT NULL,
  FOREIGN KEY (`vacancy_id`) REFERENCES `vacancies` (`vacancy_id`) ON DELETE CASCADE,
  FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Создание триггера для автоматической вставки записей в таблицу vacancy_applicants
CREATE TRIGGER trg_after_insert_vacancies
AFTER INSERT ON vacancies
FOR EACH ROW
    INSERT INTO vacancy_applicants (vacancy_id)
    VALUES (NEW.vacancy_id);

-- Создание таблицы viewed_vacancies
CREATE TABLE IF NOT EXISTS viewed_vacancies (
    user_id INT NOT NULL,
    vacancy_id INT NOT NULL,
    PRIMARY KEY (user_id, vacancy_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (vacancy_id) REFERENCES vacancies(vacancy_id) ON DELETE CASCADE
);

-- Триггер для обновления viewed_vacancies при изменении данных в таблице users
DELIMITER //

CREATE TRIGGER trg_update_viewed_vacancies_users_insert
AFTER INSERT ON users
FOR EACH ROW
BEGIN
    -- Если добавлен пользователь, обновляем viewed_vacancies для всех пользователей
    DELETE FROM viewed_vacancies;
    INSERT INTO viewed_vacancies (user_id, vacancy_id)
    SELECT user_id, vacancy_id
    FROM vacancies;
END;
//

CREATE TRIGGER trg_update_viewed_vacancies_users_delete
AFTER DELETE ON users
FOR EACH ROW
BEGIN
    -- Если удален пользователь, обновляем viewed_vacancies для всех пользователей
    DELETE FROM viewed_vacancies;
    INSERT INTO viewed_vacancies (user_id, vacancy_id)
    SELECT user_id, vacancy_id
    FROM vacancies;
END;
//

CREATE TRIGGER trg_update_viewed_vacancies_users_update
AFTER UPDATE ON users
FOR EACH ROW
BEGIN
    -- Если обновлен пользователь, обновляем viewed_vacancies для всех пользователей
    DELETE FROM viewed_vacancies;
    INSERT INTO viewed_vacancies (user_id, vacancy_id)
    SELECT user_id, vacancy_id
    FROM vacancies;
END;
//

DELIMITER ;

