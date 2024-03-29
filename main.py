import logging
import mysql.connector
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import TOKEN, DB_CONFIG

from bot.utils import is_employer


logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


class UserForm(StatesGroup):
    name = State()
    age = State()
    description = State()
    company_name = State()


async def create_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as e:
        logging.error(f"Error connecting to MySQL: {e}")
        return None


@dp.message_handler(commands=['start'], state="*")
async def start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user = message.from_user.username
    user_name = message.from_user.first_name if not message.from_user.username else message.from_user.username
    await add_user_to_db(message, user_id, user, user_name, None)  # Передаем message в функцию add_user_to_db
    await message.answer("Привет! Вы сотрудник компании или работодатель?\n\n"
                         "Для ответа введите 'Соискатель' или 'Работодатель'.")
    await UserForm.next()

async def add_user_to_db(message, user_id, user, user_name, user_type):  # Добавляем message в аргументы функции
    conn = await create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            if message.from_user.first_name:
                user_name = message.from_user.first_name
            cursor.execute("INSERT INTO users (user_id, name, user_name, user_type) VALUES (%s, %s, %s, %s) "
                           "ON DUPLICATE KEY UPDATE name=VALUES(name), user_name=VALUES(user_name), user_type=VALUES(user_type)",
                           (user_id, user, user_name, user_type))
            conn.commit()
            logging.info(f"User with ID {user_id} added to the database")
            cursor.close()
        except mysql.connector.Error as e:
            logging.error(f"Error adding user to database: {e}")
        finally:
            conn.close()




async def add_user_info_to_db(user_id, name, age, description, company_name):
    conn = await create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (user_id, user_type, user_name, name, age, description, company_name) VALUES (%s, %s, %s, %s, %s, %s, %s) "
                           "ON DUPLICATE KEY UPDATE name=VALUES(name), age=VALUES(age), description=VALUES(description), company_name=VALUES(company_name)",
                           (user_id, None, None, name, age, description, company_name))
            conn.commit()
            logging.info(f"User info added to the database for user with ID {user_id}")
            cursor.close()
        except mysql.connector.Error as e:
            logging.error(f"Error adding user info to database: {e}")
        finally:
            conn.close()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
