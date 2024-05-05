import mysql.connector # type: ignore
import logging
from ..db_connector import create_connection

# Запрос на получение данных с базы
async def get_user_data(user_tgid):
    conn = await create_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE user_tgid = %s", (user_tgid,))
            user_data = cursor.fetchone()
            cursor.close()
            print("User data:", user_data) 
            return user_data
        except mysql.connector.Error as e:
            logging.error(f"Error fetching user data from database: {e}")
        finally:
            conn.close()
    return None

# FIX IT PLS
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

# FIX IT PLS
async def get_admin_data(admin_id):
    conn = await create_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM admins WHERE admin_id = %s", (admin_id,))
            user_data = cursor.fetchone()
            cursor.close()
            return user_data
        except mysql.connector.Error as e:
            logging.error(f"Error fetching admins data from database: {e}")
        finally:
            conn.close()
    return None