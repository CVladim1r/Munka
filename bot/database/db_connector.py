import mysql.connector # type: ignore
import logging
import json

logging.basicConfig(level=logging.INFO)


DB_CONFIG={
        'host': '127.0.0.1',
        'user': 'root',
        'password': 'q1q1q1q1',
        'database': 'jfdatabase'
}

# Соединение с БД

async def create_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as e:
        logging.error(f"Error connecting to MySQL: {e}")
        return None

'''
ЗАПРОСЫ
ТОЛЬКО ДЛЯ ТИПА USER
'''

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



# ОБНОВЛЕНИЕ ДАННЫХ ТОЛЬКО ДЛЯ ТИПА USER

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

async def update_user_description(user_tgid, new_description):
    conn = await create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET user_description = %s WHERE user_tgid = %s",
                           (new_description, user_tgid))
            conn.commit()
            logging.info(f"User with ID {user_tgid} updated with new user_description: {new_description}")
            cursor.close()
        except mysql.connector.Error as e:
            logging.error(f"Error updating user user_description in database: {e}")
        finally:
            conn.close()

async def update_user_name(user_tgid, new_name):
    conn = await create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET user_what_is_your_name = %s WHERE user_tgid = %s",
                           (new_name, user_tgid))
            conn.commit()
            logging.info(f"User with ID {user_tgid} updated with new user_what_is_your_name: {new_name}")
            cursor.close()
        except mysql.connector.Error as e:
            logging.error(f"Error updating user user_what_is_your_name in database: {e}")
        finally:
            conn.close()

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

async def update_user_skills(user_tgid, new_skills):
    conn = await create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET user_skills = %s WHERE user_tgid = %s",
                           (new_skills, user_tgid))
            conn.commit()
            logging.info(f"User with ID {user_tgid} updated with new user_skills: {new_skills}")
            cursor.close()
        except mysql.connector.Error as e:
            logging.error(f"Error updating user user_skills in database: {e}")
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



# ВАКАНСИИ
async def mark_vacancy_as_viewed(user_tgid, vacancy_id):
    conn = await create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO viewed_vacancies (user_tgid, vacancy_id) VALUES (%s, %s)", (user_tgid, vacancy_id))
            conn.commit()
        except mysql.connector.Error as e:
            logging.error(f"Error marking vacancy as viewed: {e}")
        finally:
            conn.close()

async def is_vacancy_viewed_by_user(user_tgid, vacancy_id):
    conn = await create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM viewed_vacancies WHERE user_tgid = %s AND vacancy_id = %s", (user_tgid, vacancy_id))
            result = cursor.fetchone()
            cursor.close()
            return result[0] > 0
        except mysql.connector.Error as e:
            logging.error(f"Error checking if vacancy is viewed by user: {e}")
        finally:
            conn.close()
    return False

async def get_random_vacancy_for_user(user_tgid):
    while True:
        random_vacancy = await get_random_vacancy()
        if not await is_vacancy_viewed_by_user(user_tgid, random_vacancy['vacancy_id']):
            return random_vacancy

async def get_random_vacancy():
    conn = await create_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM vacancies ORDER BY RAND() LIMIT 1")
            random_vacancy = cursor.fetchone()
            cursor.close()
            return random_vacancy
        except mysql.connector.Error as e:
            logging.error(f"Error fetching random vacancy: {e}")
        finally:
            conn.close()
    return None

async def view_vacancy(user_tgid, vacancy_id):
    if not await is_vacancy_viewed_by_user(user_tgid, vacancy_id):
        await mark_vacancy_as_viewed(user_tgid, vacancy_id)
        print("Vacancy viewed successfully!")
    else:
        print("Vacancy already viewed by user.")



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
