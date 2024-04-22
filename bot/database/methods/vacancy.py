import mysql.connector # type: ignore
import logging
from ..db_connector import create_connection
import json



# PS - я не определился...
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

