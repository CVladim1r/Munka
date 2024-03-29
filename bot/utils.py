import mysql.connector
from config import DB_CONFIG

async def create_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as e:
        logging.error(f"Error connecting to MySQL: {e}")
        return None

async def is_employer(user_id):
    conn = await create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT user_type FROM users WHERE user_id = %s", (user_id,))
            result = cursor.fetchone()
            if result:
                user_type = result[0]
                return user_type == 'EMPLOYER'
            else:
                return None
        except mysql.connector.Error as e:
            logging.error(f"Error checking user type: {e}")
        finally:
            conn.close()
    return None
