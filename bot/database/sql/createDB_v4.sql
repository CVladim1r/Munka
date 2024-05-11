-- Создание базы данных
CREATE DATABASE IF NOT EXISTS ComfiDataBase;

-- Использование базы данных
USE ComfiDataBase;

-- Создание таблицы администраторов
CREATE TABLE IF NOT EXISTS admins (
  admin_id INT NOT NULL AUTO_INCREMENT,
  admin_tgid INT NOT NULL,
  admin_tgname VARCHAR(32) DEFAULT NULL,
  admin_tgfullname VARCHAR(255) DEFAULT NULL,
  PRIMARY KEY (admin_id),
  UNIQUE KEY admin_tgname (admin_tgname)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Создание таблицы пользователей
CREATE TABLE IF NOT EXISTS job_seekers (
  job_seeker_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  job_seeker_tgid BIGINT,
  job_seeker_tgname VARCHAR(32) DEFAULT NULL,
  job_seeker_tgfullname VARCHAR(255) DEFAULT NULL,
  job_seeker_fio VARCHAR(100) DEFAULT NULL,
  job_seeker_age INT DEFAULT NULL,
  job_seeker_employment ENUM('FULL','PARTIAL','ONEDAY','UNCLEAR') DEFAULT NULL,
  job_seeker_location VARCHAR(255) DEFAULT NULL,
  job_seeker_location_text VARCHAR(255) DEFAULT NULL,
  job_seeker_citizenship VARCHAR(255) DEFAULT NULL,
  job_seeker_desired_position VARCHAR(255) DEFAULT NULL,
  job_seeker_employment_type VARCHAR(255) DEFAULT NULL,
  job_seeker_profession VARCHAR(255) DEFAULT NULL,
  job_seeker_desired_salary_level VARCHAR(255) DEFAULT NULL,
  job_seeker_experience JSON,
  job_seeker_additional_info TEXT DEFAULT NULL,
  job_seeker_photo_path VARCHAR(255) DEFAULT NULL,
  job_seeker_language VARCHAR(255) DEFAULT NULL
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Создание таблицы работодателей
CREATE TABLE IF NOT EXISTS employers (
  employer_id INT NOT NULL AUTO_INCREMENT,
  employer_tgid INT NOT NULL,
  employer_tgname VARCHAR(32) DEFAULT NULL,
  employer_tgfullname VARCHAR(255) DEFAULT NULL,
  employer_company_name VARCHAR(255) DEFAULT NULL,
  employer_description TEXT,
  employer_city VARCHAR(255) DEFAULT NULL,
  employer_desired_position VARCHAR(255) DEFAULT NULL,
  employer_company_description TEXT,
  employer_responsibilities TEXT,
  employer_requirements TEXT,
  employer_working_conditions TEXT,
  employer_image_path VARCHAR(255),
  employer_verification BOOLEAN DEFAULT false,
  PRIMARY KEY (employer_id),
  UNIQUE KEY employer_tgname (employer_tgname)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Создание таблицы вакансий
CREATE TABLE IF NOT EXISTS vacancies (
  vacancy_id INT NOT NULL AUTO_INCREMENT,
  employer_id INT NOT NULL,
  vacancy_title VARCHAR(255) DEFAULT NULL,
  vacancy_created_date DATE DEFAULT NULL,
  vacancy_employment VARCHAR(255) DEFAULT NULL,
  vacancy_working_time_modes TEXT DEFAULT NULL,
  vacancy_description TEXT DEFAULT NULL,
  vacancy_photo_path VARCHAR(255) DEFAULT NULL,
  vacancy_views INT DEFAULT 0,
  PRIMARY KEY (vacancy_id),
  FOREIGN KEY (employer_id) REFERENCES employers (employer_id) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Создание таблицы заявок на вакансии
CREATE TABLE IF NOT EXISTS applications (
  application_id INT NOT NULL AUTO_INCREMENT,
  vacancy_id INT NOT NULL,
  job_seeker_id INT NOT NULL,
  applications_status ENUM('PENDING', 'APPROVED', 'REJECTED') DEFAULT 'PENDING',
  application_date DATE DEFAULT NULL,
  PRIMARY KEY (application_id),
  FOREIGN KEY (vacancy_id) REFERENCES vacancies (vacancy_id) ON DELETE CASCADE,
  FOREIGN KEY (job_seeker_id) REFERENCES job_seekers (job_seeker_id) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Создание таблицы статусов сервера
CREATE TABLE IF NOT EXISTS server_status (
  status_id INT NOT NULL AUTO_INCREMENT,
  status VARCHAR(255) NOT NULL,
  PRIMARY KEY (status_id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Вставка статусов сервера
INSERT INTO server_status (status) VALUES ('Running'), ('Stopped'), ('Error');

-- Создание таблицы viewed_vacancies
CREATE TABLE IF NOT EXISTS viewed_vacancies (
  view_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  job_seeker_id INT NOT NULL,
  vacancy_id INT NOT NULL,
  view_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX user_id_index (job_seeker_id),
  INDEX vacancy_id_index (vacancy_id),
  FOREIGN KEY (job_seeker_id) REFERENCES job_seekers(job_seeker_id) ON DELETE CASCADE,
  FOREIGN KEY (vacancy_id) REFERENCES vacancies(vacancy_id) ON DELETE CASCADE
);

-- Создание триггера для обновления даты создания вакансии
DELIMITER //
CREATE TRIGGER trg_update_vacancy_created_date
BEFORE UPDATE ON vacancies
FOR EACH ROW
BEGIN
  IF NEW.vacancy_description != OLD.vacancy_description OR NEW.vacancy_title != OLD.vacancy_title THEN
    SET NEW.vacancy_created_date = NOW();
  END IF;
END//
DELIMITER ;

-- Создание триггера для обновления статуса сервера
DELIMITER //
CREATE TRIGGER trg_update_server_status
AFTER UPDATE ON vacancies
FOR EACH ROW
BEGIN
  DECLARE vacancy_count INT;
  DECLARE server_status VARCHAR(255);

  -- Получаем количество вакансий
  SELECT COUNT(*) INTO vacancy_count FROM vacancies;

  -- Определяем статус сервера
  IF vacancy_count > 0 THEN
    SET server_status = 'Running';
  ELSE
    SET server_status = 'Stopped';
  END IF;

  -- Обновляем статус сервера
  UPDATE server_status SET status = server_status WHERE status_id = 1;
END//
DELIMITER ;

-- Создание индексов для таблицы job_seeker
ALTER TABLE job_seekers ADD INDEX job_seeker_tgid_index (job_seeker_tgid);
ALTER TABLE job_seekers ADD INDEX job_seeker_desired_position_index (job_seeker_desired_position);

-- Создание индексов для таблицы employers
ALTER TABLE employers ADD INDEX employer_tgid_index (employer_tgid);
ALTER TABLE employers ADD INDEX employer_desired_position_index (employer_desired_position);

-- Создание индексов для таблицы vacancies
ALTER TABLE vacancies ADD INDEX employer_id_index (employer_id);
ALTER TABLE vacancies ADD INDEX vacancy_created_date_index (vacancy_created_date);

-- Создание индексов для таблицы applications
ALTER TABLE applications ADD INDEX application_vacancy_id_index (vacancy_id);
ALTER TABLE applications ADD INDEX application_job_seeker_id_index (job_seeker_id);

-- Создание индексов для таблицы viewed_vacancies
ALTER TABLE viewed_vacancies ADD INDEX viewed_vacancies_job_seeker_id_index (job_seeker_id);
ALTER TABLE viewed_vacancies ADD INDEX viewed_vacancies_vacancy_id_index (vacancy_id);
