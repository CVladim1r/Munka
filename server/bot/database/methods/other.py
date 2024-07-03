import mysql.connector
import logging
from ..db_connector import create_connection

async def job_seeker_exists_in_db(job_seeker_tgid):
    conn = await create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM job_seekers WHERE job_seeker_tgid = %s", (job_seeker_tgid,))
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