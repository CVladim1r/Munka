import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot.user_registration import register_job_seeker, register_employer

from database.db_connector import add_user_to_db, add_user_info_to_db, update_user_age, update_user_description, update_user_name

from config import TOKEN

logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())

class UserForm(StatesGroup):
    nickname = State()
    regStart = State()
    age = State()
    description = State()
    company_name = State()

@dp.message_handler(commands=['start'], state="*")
async def start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_name = message.from_user.username
    user = message.from_user.first_name if not message.from_user.username else message.from_user.username
    
    if not user_name:
        user_name = str(user_id)

    await add_user_to_db(message, user_id, user, user_name, None)

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Соискатель", callback_data="job_seeker"))
    keyboard.add(InlineKeyboardButton("Работодатель", callback_data="employer"))

    await message.answer("Привет! Вы соискатель или работодатель?", reply_markup=keyboard)
    await UserForm.next()

@dp.callback_query_handler(lambda c: c.data in ["job_seeker", "employer"], state="*")
async def process_user_type(callback_query: types.CallbackQuery, state: FSMContext):
    user_type = callback_query.data
    await state.update_data(user_type=user_type)

    if user_type == "job_seeker":
        await callback_query.message.answer("Вы выбрали: Соискатель.")
        await register_job_seeker(callback_query.message, callback_query.from_user.id, callback_query.from_user.username, callback_query.from_user.username)

        await callback_query.message.answer("Давайте создадим резюме. Напишите ваш возраст:")
        await UserForm.regStart.set()

    elif user_type == "employer":
        await callback_query.message.answer("Вы выбрали: Работодатель.")
        await register_employer(callback_query.message, callback_query.from_user.id, callback_query.from_user.username, callback_query.from_user.username)

    await UserForm.next()

@dp.message_handler(state=UserForm.regStart)
async def process_name(message: types.Message, state: FSMContext):
    await message.answer("")
    await UserForm.age.set()

@dp.message_handler(state=UserForm.age)
async def process_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if not message.text.isdigit():
            await message.answer("Неверный формат возраста. Пожалуйста, введите возраст цифрами.")
            return
        data['age'] = message.text
    await update_user_age(message.from_user.id, data['age'])
    await UserForm.nickname.set()
    await message.answer("Как к вам обращаться?")

@dp.message_handler(state=UserForm.nickname)
async def process_nickname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['nickname'] = message.text
    await update_user_name(message.from_user.id, data['nickname'])
    await UserForm.description.set()
    await message.answer("Напишите краткое описание о себе.")

@dp.message_handler(state=UserForm.description)
async def process_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await update_user_description(message.from_user.id, data['description'])
    await add_user_info_to_db(message.from_user.id, data.get('nickname'), data.get('age'), data.get('description'), None)
    await message.answer("Спасибо за регистрацию.")
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
