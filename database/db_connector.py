import mysql.connector
import logging
from config import DB_CONFIG

logging.basicConfig(level=logging.INFO)

async def create_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as e:
        logging.error(f"Error connecting to MySQL: {e}")
        return None

async def add_user_to_db(message, user_id, user, user_name, user_type):
    conn = await create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            if message.from_user.username:
                # Проверяем, существует ли уже nickname для данного пользователя
                cursor.execute("SELECT nickname FROM users WHERE user_id = %s", (user_id,))
                result = cursor.fetchone()
                if result and result[0]:
                    # Если nickname уже существует и не пустой, используем его
                    user_name = result[0]
                else:
                    # Иначе используем username из сообщения и добавляем символ '@'
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

async def add_user_info_to_db(user_id, name, age, description, company_name):
    conn = await create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (user_id, name, age, description, company_name) VALUES (%s, %s, %s, %s, %s) "
                           "ON DUPLICATE KEY UPDATE name=VALUES(name), age=VALUES(age), description=VALUES(description), company_name=VALUES(company_name)",
                           (user_id, name, age, description, company_name))
            conn.commit()
            logging.info(f"User info added to the database for user with ID {user_id}")
            cursor.close()
        except mysql.connector.Error as e:
            logging.error(f"Error adding user info to database: {e}")
        finally:
            conn.close()

async def update_user_in_db(user_id, name, age, description, company_name):
    conn = await create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET name = %s, age = %s, description = %s, company_name = %s WHERE user_id = %s",
                           (name, age, description, company_name, user_id))
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

