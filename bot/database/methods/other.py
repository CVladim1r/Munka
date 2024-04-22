import mysql.connector # type: ignore
import logging
from ..db_connector import create_connection



# Проверка на наличие пользователя в базе
async def user_exists_in_db(user_tgid):
    conn = await create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users WHERE user_tgid = %s", (user_tgid,))
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