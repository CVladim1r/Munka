import mysql.connector # type: ignore
import logging
from ..config_reader import Settings
import json

logging.basicConfig(level=logging.INFO)


# Соединение с БД
async def create_connection():
    try:
        conn = mysql.connector.connect(**Settings.DB_CONFIG)
        return conn
    except mysql.connector.Error as e:
        logging.error(f"Error connecting to MySQL: {e}")
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
