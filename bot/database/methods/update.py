import mysql.connector # type: ignore
import logging
from ..db_connector import create_connection
import json


# Обновление типа пользователя
async def update_user_type(user_tgid, new_user_type):
    conn = await create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET user_type = %s WHERE user_tgid = %s",
                           (new_user_type, user_tgid))
            conn.commit()
            logging.info(f"User with ID {user_tgid} updated with new user type: {new_user_type}")
            cursor.close()
        except mysql.connector.Error as e:
            logging.error(f"Error updating user type in database: {e}")
        finally:
            conn.close()
            
# Обновление локации (города) пользователя
async def update_user_location(user_tgid, new_location):
    conn = await create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET user_location = %s WHERE user_tgid = %s",
                           (new_location, user_tgid))
            conn.commit()
            logging.info(f"User with ID {user_tgid} updated with new user_location: {new_location}")
            cursor.close()
        except mysql.connector.Error as e:
            logging.error(f"Error updating user user_location in database: {e}")
        finally:
            conn.close()

# Обновление возраста пользователя
async def update_user_age(user_tgid, new_age):
    conn = await create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET user_age = %s WHERE user_tgid = %s",
                           (new_age, user_tgid))
            conn.commit()
            logging.info(f"User with ID {user_tgid} updated with new user_age: {new_age}")
            cursor.close()
        except mysql.connector.Error as e:
            logging.error(f"Error updating user user_age in database: {e}")
        finally:
            conn.close()

# Обновление ФИО пользователя
async def update_fio(user_tgid, new_name):
    conn = await create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET user_fio = %s WHERE user_tgid = %s",
                           (new_name, user_tgid))
            conn.commit()
            logging.info(f"User with ID {user_tgid} updated with new user_fio: {new_name}")
            cursor.close()
        except mysql.connector.Error as e:
            logging.error(f"Error updating user user_fio in database: {e}")
        finally:
            conn.close()

# Обновление страны/национальности пользователя
async def update_user_citizenship(user_tgid, new_citizenship):
    conn = await create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET user_citizenship = %s WHERE user_tgid = %s",
                           (new_citizenship, user_tgid))
            conn.commit()
            logging.info(f"User with ID {user_tgid} updated with new user_citizenship: {new_citizenship}")
            cursor.close()
        except mysql.connector.Error as e:
            logging.error(f"Error updating user user_citizenship in database: {e}")
        finally:
            conn.close()



# ОБНОВЛЕНИЕ ДАННЫХ ТОЛЬКО ДЛЯ ТИПА USER

async def update_user_experience(user_tgid, new_experience):
    conn = await create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET user_experience = %s WHERE user_tgid = %s",
                           (json.dumps(new_experience), user_tgid))
            conn.commit()
            logging.info(f"User with ID {user_tgid} updated with new user_experience: {new_experience}")
            cursor.close()
        except mysql.connector.Error as e:
            logging.error(f"Error updating user user_experience in database: {e}")
        finally:
            conn.close()

async def update_user_fullname(user_tgid, new_fullname):
    conn = await create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET user_fio = %s WHERE user_tgid = %s",
                           (new_fullname, user_tgid))
            conn.commit()
            logging.info(f"User with ID {user_tgid} updated with new user_fio: {new_fullname}")
            cursor.close()
        except mysql.connector.Error as e:
            logging.error(f"Error updating user user_fio in database: {e}")
        finally:
            conn.close()

async def update_user_desired_position(user_tgid, new_desired_position):
    conn = await create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET user_desired_position = %s WHERE user_tgid = %s",
                           (new_desired_position, user_tgid))
            conn.commit()
            logging.info(f"User with ID {user_tgid} updated with new desired position: {new_desired_position}")
            cursor.close()
        except mysql.connector.Error as e:
            logging.error(f"Error updating user desired position in database: {e}")
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