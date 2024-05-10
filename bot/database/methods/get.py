import logging
from ..db_connector import create_connection

async def get_data(table, column, value):
    query = f"SELECT * FROM {table} WHERE {column} = %s"
    async with create_connection() as conn:
        try:
            async with conn.cursor(dictionary=True) as cursor:
                await cursor.execute(query, (value,))
                data = await cursor.fetchone()
                return data
        except Exception as e:
            logging.error(f"Error fetching {table} data from database: {e}")
    return None

async def get_user_data(job_seeker_tgid):
    return await get_data("job_seekers", "job_seeker_tgid", job_seeker_tgid)

async def get_employer_data(employer_tgid):
    return await get_data("employers", "employer_tgid", employer_tgid)

async def get_admin_data(admin_tgid):
    return await get_data("admins", "admin_tgid", admin_tgid)
