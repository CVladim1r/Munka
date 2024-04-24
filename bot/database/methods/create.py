import mysql.connector # type: ignore
import logging
from ..db_connector import create_connection
import json



# Запрос на добавление пользовтаеля в базу данных
async def add_user_to_db_type_user( user_tgid, user_tgname, user_tgfullname, user_language, user_type ):
    conn = await create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT user_tgname FROM users WHERE user_tgid = %s", (user_tgid,))
            result = cursor.fetchone()
            if result and result[0]:
                user_tgname = result[0]
            else:
                logging.info(f"Using username as user_tgname: {user_tgname}")
            if not user_tgname.startswith('@'):
                user_tgname = '@' + user_tgname

            cursor.execute("INSERT INTO users (user_tgid, user_tgfullname, user_tgname, user_type, user_language) "
                           "VALUES (%s, %s, %s, %s, %s) "
                           "ON DUPLICATE KEY UPDATE "
                           "user_tgfullname=VALUES(user_tgfullname), user_type=VALUES(user_type), user_language=VALUES(user_language),"
                           "user_tgname=IF(VALUES(user_tgname) <> '', VALUES(user_tgname), user_tgname)",
                           (user_tgid, user_tgfullname, user_tgname, user_type, user_language))
            conn.commit()
            logging.info(f"User with ID {user_tgid} added/updated in the database")
        except mysql.connector.Error as e:
            logging.error(f"Error adding/updating user to the database: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        logging.error("Failed to connect to the database")


# Запрос на добавление пользовтаеля в базу данных
async def add_user_info_to_db(user_tgid, user_tgfullname, user_age):
    conn = await create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (user_tgid, user_tgfullname, user_age) "
                            "VALUES (%s, %s, %s) "
                            "ON DUPLICATE KEY UPDATE user_tgfullname=VALUES(user_tgfullname), "
                            "user_age=VALUES(user_age))",
                            (user_tgid, user_tgfullname, user_age, ))

            conn.commit()
            logging.info(f"User info added to the database for user with ID {user_tgid}")
            cursor.close()
        except mysql.connector.Error as e:
            logging.error(f"Error adding user info to database: {e}")
        finally:
            conn.close()


# Запрос на отправку резюме соискателя в базу
async def send_resume(user_tgid, resume_data):
    conn = await create_connection()
    if conn:
        try:
            cursor = conn.cursor()

            desired_position = resume_data.get('desired_position', 'Не указано')
            fio = resume_data.get('fio', 'Не указано')
            age = resume_data.get('age', 'Не указано')
            location = resume_data.get('location_text', 'Не указано')
            citizenship = resume_data.get('citizenship', 'Не указано')
            desired_salary_level = resume_data.get('user_desired_salary_level', 'Не указано')
            user_employment_type = resume_data.get('user_employment_type', 'Не указано')

            experience = json.dumps(resume_data.get('user_experience', []))
            additional_info = resume_data.get('user_additional_info', 'Не указано')

            cursor.execute("UPDATE users SET user_desired_position = %s, user_fio = %s, user_age = %s"
                           "user_location_text = %s, user_citizenship = %s, user_employment_type = %s, user_experience = %s,"
                           "user_additional_info = %s, user_desired_salary_level = %s WHERE user_tgid = %s",
                           (desired_position, fio, age, location, citizenship, user_employment_type, experience, additional_info,  
                            desired_salary_level, user_tgid))
            conn.commit()
            logging.info(f"Resume sent for user with ID {user_tgid}")
            cursor.close()
        except mysql.connector.Error as e:
            logging.error(f"Error sending resume for user in database: {e}")
        finally:
            conn.close()







# ТОЛЬКО ДЛЯ ТИПА EMPLOYER
async def add_user_to_db_type_employer(employer_tgid, employer_username, employer_name, employer_type):
    conn = await create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO employers (employer_id, employer_name, employer_username, employer_type) VALUES (%s, %s, %s, %s) "
                           "ON DUPLICATE KEY UPDATE employer_name=VALUES(employer_name), employer_type=VALUES(employer_type), employer_username=IF(VALUES(employer_username) <> '', VALUES(employer_username), employer_username)",
                           (employer_tgid, employer_name, employer_username, employer_type))
            conn.commit()
            logging.info(f"User with ID {employer_tgid} added to the database")
            cursor.close()
        except mysql.connector.Error as e:
            logging.error(f"Error adding user to database: {e}")
        finally:
            conn.close()


async def add_employer_to_db(message, employer_id, employer_username, employer_name, employer_type):
    conn = await create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            if message.from_user.username:
                cursor.execute("SELECT employer_username FROM employers WHERE employer_id = %s", (employer_id,))
                result = cursor.fetchone()
                if result and result[0]:
                    user_name = result[0]
                else:
                    user_name = f"@{message.from_user.username}"
            cursor.execute("INSERT INTO employers (employer_id, employer_name, employer_username, employer_type) VALUES (%s, %s, %s, %s) "
                           "ON DUPLICATE KEY UPDATE employer_name=VALUES(employer_name), employer_type=VALUES(employer_type), employer_username=IF(VALUES(employer_username) <> '', VALUES(employer_username), employer_username)",
                           (employer_id, employer_username, employer_name, employer_type))
            conn.commit()
            logging.info(f"User with ID {employer_id} added to the database")
            cursor.close()
        except mysql.connector.Error as e:
            logging.error(f"Error adding user to database: {e}")
        finally:
            conn.close()