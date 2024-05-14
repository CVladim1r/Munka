import logging
from ..db_connector import create_connection
import mysql.connector # type: ignore

# JOB SEEKERS
# Создание записи при выборе роли JOB SEEKER
async def create_job_seeker(job_seeker_tgid, job_seeker_tgname, job_seeker_tgfullname, job_seeker_language):
    try:
        conn = await create_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        # Проверяем существует ли запись с заданным job_seeker_tgid
        sql_check = "SELECT COUNT(*) FROM job_seekers WHERE job_seeker_tgid = %s"
        cursor.execute(sql_check, (job_seeker_tgid,))
        result = cursor.fetchone()
        if result[0] > 0:  # Обновляем данные
            sql_update = """
            UPDATE job_seekers
            SET job_seeker_tgname = %s,
                job_seeker_tgfullname = %s,
                job_seeker_language = %s
            WHERE job_seeker_tgid = %s
            """
            cursor.execute(sql_update, (job_seeker_tgname, job_seeker_tgfullname, job_seeker_language, job_seeker_tgid))
        else:
            sql_insert = """
            INSERT INTO job_seekers (job_seeker_tgid, job_seeker_tgname, job_seeker_tgfullname, job_seeker_language)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql_insert, (job_seeker_tgid, job_seeker_tgname, job_seeker_tgfullname, job_seeker_language))
        conn.commit()
        return True
    except mysql.connector.Error as e:
        logging.error(f"Error creating or updating job seeker: {e}")
        return False
    finally:
        cursor.close()
        conn.close()  # Закрытие соединения




# EMPLOYER
# Создание записи при выборе роли EMPLOYER
async def create_employer(employer_tgid, employer_tgname, employer_tgfullname, employer_language):
    try:
        conn = await create_connection()
        if conn is None:
            return False

        cursor = conn.cursor()
        sql_check = "SELECT COUNT(*) FROM employers WHERE employer_tgid = %s"
        cursor.execute(sql_check, (employer_tgid,))
        result = cursor.fetchone()
        if result[0] > 0:
            sql_update = """
            UPDATE employers
            SET employer_tgname = %s,
                employer_tgfullname = %s,
                employer_language = %s
            WHERE employer_tgid = %s
            """
            cursor.execute(sql_update, (employer_tgname, employer_tgfullname, employer_language, employer_tgid))
        else:
            sql_insert = """
            INSERT INTO employers (employer_tgid, employer_tgname, employer_tgfullname, employer_language)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql_insert, (employer_tgid, employer_tgname, employer_tgfullname, employer_language))
        conn.commit()
        return True
    except mysql.connector.Error as e:
        logging.error(f"Error creating or updating employer: {e}")
        return False
    finally:
        cursor.close()
        conn.close()
