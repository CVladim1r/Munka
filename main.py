import logging
import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import aiogram
from bot.user_registration import register_job_seeker, register_employer

from database.db_connector import get_user_data, get_employer_data, update_user_location, add_user_info_to_db, update_user_age, update_user_description, update_user_name
from database.db_connector import add_user_to_db_type_user, add_user_to_db_type_employer
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
    name = ""
    user = message.from_user.first_name if not message.from_user.username else message.from_user.username
    
    if not user_name:
        user_name = str(user_id)
        
    user_data = await get_user_data(user_id)
    employer_data = await get_employer_data(user_id)

    if employer_data:
        name = employer_data.get("name")
        await main_menu_employer(message.from_user.id, message.message_id)

        return
    elif user_data:
        name = user_data.get("name")
        user_type = user_data.get("user_type")
        if user_type == "USER":
            await main_menu_user(message.from_user.id, message.message_id)
            return
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Соискатель", callback_data="job_seeker"))
    keyboard.add(InlineKeyboardButton("Работодатель", callback_data="employer"))
    await bot.send_message(message.chat.id, '''Привет я кот Миша.\n
Я выполняю здесь самую главную функцию: помогаю соискателям и работодателям найти друг друга. 
Представь, у каждого есть работа, а в мире царит гармония – мяу, красота. Для этого я здесь.''')
    await asyncio.sleep(5)
    await message.answer("Давай теперь познакомимся поближе. Кто ты?", reply_markup=keyboard)
    await UserForm.next()


async def main_menu_user(user_id, message_id):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("🔍 Искать Вакансии"))
    keyboard.add(KeyboardButton("👤 Личный кабинет"))
    keyboard.add(KeyboardButton("✏️ Редактировать резюме"))
    keyboard.add(KeyboardButton("ℹ️ О боте"))

    main_text = "Искать вакансии:\n"
    main_text += "Личный кабинет\n"
    main_text += "Редактировать резюме\n"
    main_text += "О боте\n"

    await bot.send_message(user_id, main_text, reply_markup=keyboard)


async def main_menu_employer(user_id):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("🔍 Опубликовать вакансию"))
    keyboard.add(KeyboardButton("👤 Информация о компании"))
    keyboard.add(KeyboardButton("ℹ️ О боте"))

    main_text = "Искать вакансии:\n"
    main_text += "Личный кабинет\n"
    main_text += "Редактировать резюме\n"
    main_text += "О боте\n"

    await bot.send_message(user_id, f"{main_text}", reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data in ["job_seeker", "employer"], state="*")
async def process_user_type(callback_query: types.CallbackQuery, state: FSMContext):
    user_type = callback_query.data
    user_id = callback_query.from_user.id
    
    employer_id = callback_query.from_user.id
    employer_username = callback_query.from_user.username

    user = callback_query.from_user.first_name if not callback_query.from_user.full_name else callback_query.from_user.username
    user_name = callback_query.from_user.username
    
    await state.update_data(user_type=user_type)

    if user_type == "job_seeker":
        await add_user_to_db_type_user(callback_query.message, user_id, user, user_name, None)

        await callback_query.message.answer("Давай создадим резюме. Напиши свой возраст:")
        await UserForm.regStart.set()

    elif user_type == "employer":
        await add_user_to_db_type_employer(callback_query.message, employer_id, employer_username, user, None)
        await register_employer(callback_query.message, callback_query.from_user.id, callback_query.from_user.username, callback_query.from_user.username)
        await callback_query.message.answer("Спасибо за регистрацию.")
        await main_menu_employer(callback_query.message.from_user.id, callback_query.message.message_id)
        

    await UserForm.next()





@dp.message_handler(state=UserForm.age)
async def process_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if not message.text.isdigit() or not (0 < int(message.text) < 99):
            await message.answer("Неверный формат возраста. Пожалуйста, введите возраст цифрами. Пример: 18")
            return
        data['age'] = message.text
    await update_user_age(message.from_user.id, data['age'])
    await UserForm.location.set()
    await message.answer("Какой ваш город?")

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
    await add_user_info_to_db(message.from_user.id, data.get('nickname'), data.get('age'), data.get('description'))
    await message.answer("Спасибо за регистрацию.")
    await main_menu_user(message.from_user.id, message.message_id)
    await state.finish()






@dp.message_handler(lambda message: message.text == "ℹ️ О боте", state="*")
async def about_bot(message: types.Message):
    about_text = "Данный бот был создан для помощи компаниям в сфере общепита быстрее найти работников."
    await message.answer(about_text)

@dp.message_handler(lambda message: message.text == "👤 Личный кабинет", state="*")
async def personal_cabinet(message: types.Message):
    user_id = message.from_user.id

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

        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(KeyboardButton("Заполнить анкету заново"))
        keyboard.add(KeyboardButton("Изменить описание"))
        keyboard.add(KeyboardButton("Смотреть вакансии"))
        keyboard.add(KeyboardButton("Назад"))

        await message.answer(user_info_text, reply_markup=keyboard)
    else:
        await message.answer("Информация о пользователе не найдена.")

@dp.message_handler(lambda message: message.text == "Назад", state="*")
async def back_to_main_menu(message: types.Message):
    user_id = message.from_user.id

    user_data = await get_user_data(user_id)

    if user_data:
        name = user_data.get("name")
        await main_menu_user(user_id, name)
    else:
        await message.answer("Информация о пользователе не найдена. Пройдите регистрацию нажав на команду /start")








# Команды доступные для любого типа пользователя

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
