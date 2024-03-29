import logging
import mysql.connector
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import TOKEN, DB_CONFIG

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


async def add_user_to_db(user_id, user, user_name):
    conn = await create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (user_id, USER, USER_NAME) VALUES (%s, %s, %s) "
                           "ON DUPLICATE KEY UPDATE USER=VALUES(USER), USER_NAME=VALUES(USER_NAME)",
                           (user_id, user, user_name))
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
            cursor.execute("INSERT INTO users (user_id, NAME, AGE, DESCRIPTION, COMPANY_NAME) VALUES (%s, %s, %s, %s, %s) "
                           "ON DUPLICATE KEY UPDATE NAME=VALUES(NAME), AGE=VALUES(AGE), DESCRIPTION=VALUES(DESCRIPTION), COMPANY_NAME=VALUES(COMPANY_NAME)",
                           (user_id, name, age, description, company_name))
            conn.commit()
            logging.info(f"User info added to the database for user with ID {user_id}")
            cursor.close()
        except mysql.connector.Error as e:
            logging.error(f"Error adding user info to database: {e}")
        finally:
            conn.close()


@dp.message_handler(commands=['start'], state="*")
async def start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user = message.from_user.username
    user_name = message.from_user.first_name if not message.from_user.username else message.from_user.username
    await add_user_to_db(user_id, user, user_name)
    await message.answer("Привет! Пожалуйста, ответь на несколько вопросов в одном сообщении.\n\n"
                         "1. Как тебя зовут?")
    await UserForm.name.set()


@dp.message_handler(state=UserForm.name)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer("2. Сколько тебе лет?")
    await UserForm.next()


@dp.message_handler(state=UserForm.age)
async def process_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['age'] = message.text
    await message.answer("3. Расскажи немного о себе.")
    await UserForm.next()


@dp.message_handler(state=UserForm.description)
async def process_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await message.answer("4. Как называется твоя компания?")
    await UserForm.next()


@dp.message_handler(state=UserForm.company_name)
async def process_company_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['company_name'] = message.text
        user_id = message.from_user.id
        await add_user_info_to_db(user_id, data['name'], data['age'], data['description'], data['company_name'])
    await state.finish()
    await message.answer("Спасибо! Все данные записаны.")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
