import mysql.connector # type: ignore
import logging
from ..db_connector import create_connection


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
