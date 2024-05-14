import mysql.connector 
import logging
from ..config_reader import Settings

logging.basicConfig(level=logging.INFO)

# Соединение с БД
async def create_connection():
    try:
        conn = mysql.connector.connect(**Settings.DB_CONFIG)
        return conn
    except mysql.connector.Error as e:
        logging.error(f"Error connecting to MySQL: {e}")
        return None