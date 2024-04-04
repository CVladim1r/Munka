import mysql.connector # type: ignore
import logging
from config import DB_CONFIG
import json

logging.basicConfig(level=logging.INFO)

# Соединение с БД

async def create_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as e:
        logging.error(f"Error connecting to MySQL: {e}")
        return None

# ЗАПРОСЫ

# ТОЛЬКО ДЛЯ ТИПА USER

async def add_user_to_db_type_user(message, user_id, user, user_name, user_type):
    conn = await create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            if message.from_user.username:
                # Проверяем, существует ли уже nickname для данного пользователя
                cursor.execute("SELECT nickname FROM users WHERE user_id = %s", (user_id,))
                result = cursor.fetchone()
                if result and result[0]:
                    user_name = result[0]
                else:
                    user_name = f"@{message.from_user.username}"
            cursor.execute("INSERT INTO users (user_id, name, nickname, user_type) VALUES (%s, %s, %s, %s) "
                           "ON DUPLICATE KEY UPDATE name=VALUES(name), user_type=VALUES(user_type), nickname=IF(VALUES(nickname) <> '', VALUES(nickname), nickname)",
                           (user_id, user, user_name, user_type))
            conn.commit()
            logging.info(f"User with ID {user_id} added to the database")
            cursor.close()
        except mysql.connector.Error as e:
            logging.error(f"Error adding user to database: {e}")
        finally:
            conn.close()

async def add_user_info_to_db(user_id, name, age, description):
    conn = await create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (user_id, name, age, description) VALUES (%s, %s, %s, %s) "
                        "ON DUPLICATE KEY UPDATE name=VALUES(name), age=VALUES(age), description=VALUES(description)",
                        (user_id, name, age, description))

            conn.commit()
            logging.info(f"User info added to the database for user with ID {user_id}")
            cursor.close()
        except mysql.connector.Error as e:
            logging.error(f"Error adding user info to database: {e}")
        finally:
            conn.close()

async def user_exists_in_db(user_id):
    conn = await create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users WHERE user_id = %s", (user_id,))
            result = cursor.fetchone()
            cursor.close()
            if result and result[0] > 0:
                return True
            else:
                return False
        except mysql.connector.Error as e:
            logging.error(f"Error checking if user exists in database: {e}")
        finally:
            conn.close()
    return False

async def get_user_data(user_id):
    conn = await create_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
            user_data = cursor.fetchone()
            cursor.close()
            return user_data
        except mysql.connector.Error as e:
            logging.error(f"Error fetching user data from database: {e}")
        finally:
            conn.close()
    return None

# ОБНОВЛЕНИЕ ДАННЫХ ТОЛЬКО ДЛЯ ТИПА USER

async def update_user_in_db(user_id, name, age, description):
    conn = await create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET name = %s, age = %s, description = %s, WHERE user_id = %s",
                           (name, age, description, user_id))
            conn.commit()
            logging.info(f"User info updated in the database for user with ID {user_id}")
            cursor.close()
        except mysql.connector.Error as e:
            logging.error(f"Error updating user info in database: {e}")
        finally:
            conn.close()

async def update_user_type(user_id, new_user_type):
    conn = await create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET user_type = %s WHERE user_id = %s",
                           (new_user_type, user_id))
            conn.commit()
            logging.info(f"User with ID {user_id} updated with new user type: {new_user_type}")
            cursor.close()
        except mysql.connector.Error as e:
            logging.error(f"Error updating user type in database: {e}")
        finally:
            conn.close()

async def update_user_location(user_id, new_location):
    conn = await create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET location = %s WHERE user_id = %s",
                           (new_location, user_id))
            conn.commit()
            logging.info(f"User with ID {user_id} updated with new location: {new_location}")
            cursor.close()
        except mysql.connector.Error as e:
            logging.error(f"Error updating user location in database: {e}")
        finally:
            conn.close()

async def update_user_age(user_id, new_age):
    conn = await create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET age = %s WHERE user_id = %s",
                           (new_age, user_id))
            conn.commit()
            logging.info(f"User with ID {user_id} updated with new age: {new_age}")
            cursor.close()
        except mysql.connector.Error as e:
            logging.error(f"Error updating user age in database: {e}")
        finally:
            conn.close()

async def update_user_description(user_id, new_description):
    conn = await create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET description = %s WHERE user_id = %s",
                           (new_description, user_id))
            conn.commit()
            logging.info(f"User with ID {user_id} updated with new description: {new_description}")
            cursor.close()
        except mysql.connector.Error as e:
            logging.error(f"Error updating user description in database: {e}")
        finally:
            conn.close()

async def update_user_name(user_id, new_name):
    conn = await create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET name = %s WHERE user_id = %s",
                           (new_name, user_id))
            conn.commit()
            logging.info(f"User with ID {user_id} updated with new name: {new_name}")
            cursor.close()
        except mysql.connector.Error as e:
            logging.error(f"Error updating user name in database: {e}")
        finally:
            conn.close()

async def update_user_citizenship(user_id, new_citizenship):
    conn = await create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET citizenship = %s WHERE user_id = %s",
                           (new_citizenship, user_id))
            conn.commit()
            logging.info(f"User with ID {user_id} updated with new citizenship: {new_citizenship}")
            cursor.close()
        except mysql.connector.Error as e:
            logging.error(f"Error updating user citizenship in database: {e}")
        finally:
            conn.close()

async def update_user_skills(user_id, new_skills):
    conn = await create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET skills = %s WHERE user_id = %s",
                           (new_skills, user_id))
            conn.commit()
            logging.info(f"User with ID {user_id} updated with new skills: {new_skills}")
            cursor.close()
        except mysql.connector.Error as e:
            logging.error(f"Error updating user skills in database: {e}")
        finally:
            conn.close()


async def send_resume(user_id, resume):
    conn = await create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET desired_position = %s, experience = %s, "
                           "experience_description = %s, additional_info = %s, skills = %s, "
                           "citizenship = %s, user_fullname = %s WHERE user_id = %s",
                           (resume['desired_position'], json.dumps(resume['experience']), resume['experience_description'],
                            resume['additional_info'], resume['skills'], resume['citizenship'],
                            resume['user_fullname'], user_id))
            conn.commit()
            logging.info(f"Resume sent for user with ID {user_id}")
            cursor.close()
        except mysql.connector.Error as e:
            logging.error(f"Error sending resume for user in database: {e}")
        finally:
            conn.close()


async def update_user_experience(user_id, new_experience):
    conn = await create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET experience = %s WHERE user_id = %s",
                           (json.dumps(new_experience), user_id))
            conn.commit()
            logging.info(f"User with ID {user_id} updated with new experience: {new_experience}")
            cursor.close()
        except mysql.connector.Error as e:
            logging.error(f"Error updating user experience in database: {e}")
        finally:
            conn.close()
async def update_user_fullname(user_id, new_fullname):
    conn = await create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET fullname = %s WHERE user_id = %s",
                           (new_fullname, user_id))
            conn.commit()
            logging.info(f"User with ID {user_id} updated with new fullname: {new_fullname}")
            cursor.close()
        except mysql.connector.Error as e:
            logging.error(f"Error updating user fullname in database: {e}")
        finally:
            conn.close()

async def update_user_desired_position(user_id, new_desired_position):
    conn = await create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET desired_position = %s WHERE user_id = %s",
                           (new_desired_position, user_id))
            conn.commit()
            logging.info(f"User with ID {user_id} updated with new desired position: {new_desired_position}")
            cursor.close()
        except mysql.connector.Error as e:
            logging.error(f"Error updating user desired position in database: {e}")
        finally:
            conn.close()

# ТОЛЬКО ДЛЯ ТИПА EMPLOYER

async def add_user_to_db_type_employer(message, employer_id, employer_username, employer_name, employer_type):
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

async def update_employer_type(employer_id, new_employer_type):
    conn = await create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE employers SET employer_type = %s WHERE employer_id = %s",
                           (new_employer_type, employer_id))
            conn.commit()
            logging.info(f"User with ID {employer_id} updated with new user type: {new_employer_type}")
            cursor.close()
        except mysql.connector.Error as e:
            logging.error(f"Error updating user type in database: {e}")
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

async def get_employer_data(employer_id):
    conn = await create_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM employers WHERE employer_id = %s", (employer_id,))
            user_data = cursor.fetchone()
            cursor.close()
            return user_data
        except mysql.connector.Error as e:
            logging.error(f"Error fetching user data from database: {e}")
        finally:
            conn.close()
    return None


# Бот затычка (PLUG_BOT)

async def add_user_to_db_plug_bot(message, user_id, user_name, user_username):
    conn = await create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            if message.from_user.username:
                cursor.execute("SELECT user_name FROM plug_users WHERE user_id = %s", (user_id,))
                result = cursor.fetchone()
                if result and result[0]:
                    user_name = result[0]
                else:
                    user_name = f"@{message.from_user.username}"
            cursor.execute("INSERT INTO plug_users (user_id, user_name, user_username) VALUES (%s, %s, %s) "
                           "ON DUPLICATE KEY UPDATE user_name=VALUES(user_name), user_username=VALUES(user_username)",
                           (user_id, user_name, user_username))
            conn.commit()
            logging.info(f"User with ID {user_id} added to the database")
            cursor.close()
        except mysql.connector.Error as e:
            logging.error(f"Error adding user to database: {e}")
        finally:
            conn.close()
