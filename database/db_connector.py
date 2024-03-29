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
            if message.from_user.first_name:
                user_name = message.from_user.first_name
            cursor.execute("INSERT INTO users (user_id, name, user_name, user_type) VALUES (%s, %s, %s, %s) "
                           "ON DUPLICATE KEY UPDATE name=VALUES(name), user_name=VALUES(user_name), user_type=VALUES(user_type)",
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
            cursor.execute("INSERT INTO users (user_id, user_type, user_name, name, age, description, company_name) VALUES (%s, %s, %s, %s, %s, %s, %s) "
                           "ON DUPLICATE KEY UPDATE name=VALUES(name), age=VALUES(age), description=VALUES(description), company_name=VALUES(company_name)",
                           (user_id, None, None, name, age, description, company_name))
            conn.commit()
            logging.info(f"User info added to the database for user with ID {user_id}")
            cursor.close()
        except mysql.connector.Error as e:
            logging.error(f"Error adding user info to database: {e}")
        finally:
            conn.close()
