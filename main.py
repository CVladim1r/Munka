import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot.user_registration import register_job_seeker, register_employer

from database.db_connector import add_user_to_db, get_user_data, user_exists_in_db, update_user_location, add_user_info_to_db, update_user_age, update_user_description, update_user_name

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
    location = State()


@dp.message_handler(commands=['start'], state="*")
async def start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_name = message.from_user.username
    user = message.from_user.first_name if not message.from_user.username else message.from_user.username
    
    if not user_name:
        user_name = str(user_id)

    # Check if the user already exists in the database
    user_data = await get_user_data(user_id)

    if user_data:
        user_type = user_data.get("user_type")
        if user_type == "USER":
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(KeyboardButton("🔍 Искать Вакансии"))
            keyboard.add(KeyboardButton("👤 Личный кабинет"))
            keyboard.add(KeyboardButton("✏️ Редактировать резюме"))
            keyboard.add(KeyboardButton("ℹ️ О боте"))

            await message.answer(f"С возвращением , {user_name}! Прямо сейчас ты можешь начать просмотр вакансий или изменить данные в профиле. Команда /help для помощи", reply_markup=keyboard)
            await message.answer("Выберите действие:", reply_markup=keyboard)
            return

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

        await callback_query.message.answer("Давай создадим резюме. Напиши свой возраст:")
        await UserForm.regStart.set()

    elif user_type == "employer":
        await callback_query.message.answer("Вы выбрали: Работодатель.")
        await register_employer(callback_query.message, callback_query.from_user.id, callback_query.from_user.username, callback_query.from_user.username)

    await UserForm.next()

@dp.message_handler(state=UserForm.age)
async def process_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if not message.text.isdigit():
            await message.answer("Неверный формат возраста. Пожалуйста, введите возраст цифрами.")
            return
        data['age'] = message.text
    await update_user_age(message.from_user.id, data['age'])
    await UserForm.location.set()
    await message.answer("Какой ваш город?")
    # Создаем клавиатуру с кнопками для выбора города
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Санкт-Петербург"))
    keyboard.add(KeyboardButton("Москва"))
    keyboard.add(KeyboardButton("Сочи"))
    keyboard.add(KeyboardButton("Новосибирск"))
    await message.answer("Выберите город из списка:", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text in ["Санкт-Петербург", "Москва", "Сочи", "Новосибирск"], state=UserForm.location)
async def process_location(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['location'] = message.text
    await update_user_location(message.from_user.id, data['location'])
    await UserForm.nickname.set()
    await message.answer("Как к тебе обращаться?")

@dp.message_handler(state=UserForm.nickname)
async def process_nickname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['nickname'] = message.text
    await update_user_name(message.from_user.id, data['nickname'])
    await UserForm.description.set()
    await message.answer("Напиши краткое описание о себе.")

@dp.message_handler(state=UserForm.description)
async def process_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await update_user_description(message.from_user.id, data['description'])
    await add_user_info_to_db(message.from_user.id, data.get('nickname'), data.get('age'), data.get('description'), None)
    await message.answer("Спасибо за регистрацию.")
    await state.finish()


@dp.message_handler(lambda message: message.text == "ℹ️ О боте", state="*")
async def about_bot(message: types.Message):
    about_text = "Данный бот был создан для помощи компаниям в сфере общепита быстрее найти работников."
    await message.answer(about_text)

@dp.message_handler(lambda message: message.text == "👤 Личный кабинет", state="*")
async def personal_cabinet(message: types.Message):
    user_id = message.from_user.id

    # Fetch user data from the database
    user_data = await get_user_data(user_id)

    if user_data:
        name = user_data.get("name")
        age = user_data.get("age")
        description = user_data.get("description")
        location = user_data.get("location")
        user_type = user_data.get("user_type")

        if user_type == "USER":
            status = "Ищущий работу"
        else:
            status = "Работодатель"

        user_info_text = f"Имя: {name}\nВозраст: {age}\nОписание: {description}\nМестоположение: {location}\nСтатус: {status}"

        await message.answer(user_info_text)
    else:
        await message.answer("Информация о пользователе не найдена.")

@dp.message_handler(commands=['help'], state="*")
async def help_command(message: types.Message):
    help_text = "Список доступных команд:\n"
    help_text += "/start - Начать диалог с ботом\n"
    help_text += "/help - Получить список доступных команд\n"
    help_text += "Личный кабинет - Просмотреть информацию о пользователе\n"
    help_text += "Искать Вакансии - Поиск вакансий\n"
    help_text += "Редактировать резюме - Изменить информацию о себе\n"
    help_text += "О боте - Информация о боте\n"

    await message.answer(help_text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
