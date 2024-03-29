import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import TOKEN
from database.db_connector import add_user_to_db, add_user_info_to_db

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

class UserForm(StatesGroup):
    name = State()
    age = State()
    description = State()
    company_name = State()

@dp.message_handler(commands=['start'], state="*")
async def start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user = message.from_user.username
    user_name = message.from_user.first_name if not message.from_user.username else message.from_user.username
    await add_user_to_db(message, user_id, user, user_name, None)

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Соискатель", callback_data="job_seeker"))
    keyboard.add(InlineKeyboardButton("Работодатель", callback_data="employer"))

    await message.answer("Привет! Вы сотрудник компании или работодатель?", reply_markup=keyboard)
    await UserForm.next()

@dp.callback_query_handler(lambda c: c.data in ["job_seeker", "employer"], state="*")
async def process_user_type(callback_query: types.CallbackQuery, state: FSMContext):
    user_type = callback_query.data
    await state.update_data(user_type=user_type)

    if user_type == "job_seeker":
        await callback_query.message.answer("Вы выбрали: Соискатель.")
    elif user_type == "employer":
        await callback_query.message.answer("Вы выбрали: Работодатель.")

    await UserForm.next()

@dp.message_handler(state=UserForm.description)
async def process_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text

    await UserForm.next()
    await message.answer("Завершено! Спасибо за регистрацию.")

    async with state.proxy() as data:
        user_id = message.from_user.id
        await add_user_info_to_db(user_id, data['name'], data['age'], data['description'], data.get('company_name'))

    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
