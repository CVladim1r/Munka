import mysql.connector # type: ignore
import logging
from ..db_connector import create_connection
import json

async def add_user_to_db_type_user(user_tgid, user_tgname, user_fullname, user_type):
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

            cursor.execute("INSERT INTO users (user_tgid, user_fullname, user_tgname, user_type) "
                           "VALUES (%s, %s, %s, %s) "
                           "ON DUPLICATE KEY UPDATE "
                           "user_fullname=VALUES(user_fullname), user_type=VALUES(user_type), "
                           "user_tgname=IF(VALUES(user_tgname) <> '', VALUES(user_tgname), user_tgname)",
                           (user_tgid, user_fullname, user_tgname, user_type))
            conn.commit()
            logging.info(f"User with ID {user_tgid} added/updated in the database")
        except mysql.connector.Error as e:
            logging.error(f"Error adding/updating user to the database: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        logging.error("Failed to connect to the database")




async def add_user_info_to_db(user_tgid, user_fullname, user_age, user_description):
    conn = await create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (user_tgid, user_fullname, user_age, user_description) "
                            "VALUES (%s, %s, %s, %s) "
                            "ON DUPLICATE KEY UPDATE user_fullname=VALUES(user_fullname), "
                            "user_age=VALUES(user_age), user_description=VALUES(user_description)",
                            (user_tgid, user_fullname, user_age, user_description))

            conn.commit()
            logging.info(f"User info added to the database for user with ID {user_tgid}")
            cursor.close()
        except mysql.connector.Error as e:
            logging.error(f"Error adding user info to database: {e}")
        finally:
            conn.close()




async def send_resume(user_tgid, resume):
    conn = await create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET user_desired_position = %s, user_experience = %s, "
                           "user_experience_description = %s, user_additional_info = %s, user_skills = %s, "
                           "user_citizenship = %s, user_what_is_your_name = %s WHERE user_tgid = %s",
                           (resume['user_desired_position'], json.dumps(resume['user_experience']), resume['user_experience_description'],
                            resume['user_additional_info'], resume['user_skills'], resume['user_citizenship'],
                            resume['user_what_is_your_name'], user_tgid))
            conn.commit()
            logging.info(f"Resume sent for user with ID {user_tgid}")
            cursor.close()
        except mysql.connector.Error as e:
            logging.error(f"Error sending resume for user in database: {e}")
        finally:
            conn.close()



# ТОЛЬКО ДЛЯ ТИПА EMPLOYER
async def add_user_to_db_type_employer(employer_id, employer_username, employer_name, employer_type):
    conn = await create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO employers (employer_id, employer_name, employer_username, employer_type) VALUES (%s, %s, %s, %s) "
                           "ON DUPLICATE KEY UPDATE employer_name=VALUES(employer_name), employer_type=VALUES(employer_type), employer_username=IF(VALUES(employer_username) <> '', VALUES(employer_username), employer_username)",
                           (employer_id, employer_name, employer_username, employer_type))
            conn.commit()
            logging.info(f"User with ID {employer_id} added to the database")
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