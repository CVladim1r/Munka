CREATE DATABASE IF NOT EXISTS JFDataBase;

USE JFDataBase;

-- Создание таблицы employers
CREATE TABLE IF NOT EXISTS employers (
  employer_id int NOT NULL AUTO_INCREMENT,
  employer_username varchar(32) DEFAULT NULL,
  employer_fullname varchar(255) DEFAULT NULL,
  employers_company_name varchar(255) DEFAULT NULL,
  employers_description text,
  employer_type enum('EMPLOYER','USER') DEFAULT NULL,
  employers_city varchar(255) DEFAULT NULL,
  employers_desired_position varchar(255) DEFAULT NULL,
  employers_company_description text,
  employers_responsibilities text,
  employers_requirements text,
  employers_working_conditions text,
  employers_image_path varchar(255),
  PRIMARY KEY (employer_id),
  UNIQUE KEY employer_username (employer_username)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Создание таблицы vacancies
CREATE TABLE IF NOT EXISTS vacancies (
  vacancy_id INT NOT NULL AUTO_INCREMENT,
  vacancy_title VARCHAR(255) DEFAULT NULL,
  vacancies_company_name VARCHAR(255) DEFAULT NULL,
  vacancy_url VARCHAR(255) DEFAULT NULL,
  vacancies_created_date DATE DEFAULT NULL,
  vacancies_employment VARCHAR(255) DEFAULT NULL,
  vacancies_working_time_modes TEXT,
  vacancies_experience VARCHAR(255) DEFAULT NULL,
  vacancies_salary_info VARCHAR(255) DEFAULT NULL,
  vacancies_description TEXT,
  vacancies_skills TEXT,
  PRIMARY KEY (vacancy_id)
);

-- Создание таблицы users
CREATE TABLE IF NOT EXISTS users (
  user_id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  user_tgip varchar(255) DEFAULT NULL,
  user_tgid BIGINT,
  user_type enum('EMPLOYER','USER') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  user_tgname varchar(32) DEFAULT NULL,
  user_tgfullname varchar(255) DEFAULT NULL,
  user_age int DEFAULT NULL,
  user_location varchar(255) DEFAULT NULL,
  user_location_text varchar(255) DEFAULT NULL,
  user_dob date DEFAULT NULL,
  user_citizenship varchar(255) DEFAULT NULL,
  user_experience JSON,
  user_additional_info text,
  user_photo_path varchar(255) DEFAULT NULL,
  UNIQUE KEY user_nickname (user_nickname)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Создание таблицы vacancy_applicants
CREATE TABLE IF NOT EXISTS vacancy_applicants (
  vacancy_applicants_id INT AUTO_INCREMENT PRIMARY KEY,
  vacancy_id INT NOT NULL,
  user_id INT NULL,
  FOREIGN KEY (vacancy_id) REFERENCES vacancies (vacancy_id) ON DELETE CASCADE,
  FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
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
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (vacancy_id) REFERENCES vacancies(vacancy_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `plug_users` (
  `user_id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `user_username` varchar(255) UNIQUE,
  `user_name` varchar(255)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;