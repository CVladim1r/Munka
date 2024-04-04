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

from bot.user_registration import register_job_seeker, register_employer
from bot.keyboards import get_position_keyboard, get_yes_no_keyboard, get_save_restart_keyboard, get_choose_rule, get_choose_menu_employer_buttons, get_choose_menu_user_buttons, get_location_keyboard, get_resume_button, get_citizenship_keyboard

from database.db_connector import update_user_citizenship, update_user_experience_details, update_user_fullname, update_user_desired_position, update_user_experience, update_user_skills, send_resume, update_user_citizenship, get_user_data, get_employer_data, update_user_location, add_user_info_to_db, update_user_age, update_user_description, update_user_name
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
    fullname = State() 
    citizenship = State()
    desired_position = State()
    work_experience = State()
    experience_details = State()
    experience_another = State()
    resume_check = State()
    resume_confirmation = State()
    resume_start = State()
    skills = State()
    resume_edit = State()

class CommandState(StatesGroup):
    COMMAND_PROCESSING = State()

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
        
    await bot.send_message(message.chat.id, '''Привет я кот Миша.\n
Я выполняю здесь самую главную функцию: помогаю соискателям и работодателям найти друг друга. 
Представь, у каждого есть работа, а в мире царит гармония – мяу, красота. Для этого я здесь.''', reply_markup=None)
    await asyncio.sleep(4)
    await message.answer("Давай теперь познакомимся поближе. Кто ты?", reply_markup=await get_choose_rule())
    await UserForm.next()

async def main_menu_user(user_id, message_id):
    main_text = "Искать вакансии:\n"
    main_text += "Личный кабинет\n"
    main_text += "Редактировать резюме\n"
    main_text += "О боте\n"
    await bot.send_message(user_id, main_text, reply_markup=await get_choose_menu_user_buttons())

async def main_menu_employer(user_id, message_id):
    main_text = "Искать вакансии:\n"
    main_text += "Личный кабинет\n"
    main_text += "Редактировать резюме\n"
    main_text += "О боте\n"
    await bot.send_message(user_id, main_text, reply_markup=await get_choose_menu_employer_buttons())

@dp.callback_query_handler(lambda c: c.data in ["job_seeker", "employer"], state="*")
async def process_user_type(callback_query: types.CallbackQuery, state: FSMContext):
    await CommandState.COMMAND_PROCESSING.set()

    user_type = callback_query.data
    user_id = callback_query.from_user.id
    
    employer_id = callback_query.from_user.id
    employer_username = callback_query.from_user.username

    user = callback_query.from_user.first_name if not callback_query.from_user.full_name else callback_query.from_user.username
    user_name = callback_query.from_user.username
    
    await state.update_data(user_type=user_type)

    if user_type == "job_seeker":
        await add_user_to_db_type_user(callback_query.message, user_id, user, user_name, None)
        await register_job_seeker(callback_query.message, callback_query.from_user.id, callback_query.from_user.username, callback_query.from_user.username)
        await callback_query.message.answer("Давай создадим резюме. Напиши свой возраст:", reply_markup=None)
        await UserForm.regStart.set()

    elif user_type == "employer":
        await add_user_to_db_type_employer(callback_query.message, employer_id, employer_username, user, None)
        await register_employer(callback_query.message, callback_query.from_user.id, callback_query.from_user.username, callback_query.from_user.username)
    await UserForm.next()


@dp.message_handler(state=UserForm.age)
async def process_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if not message.text.isdigit() or not (0 < int(message.text) < 99):
            await message.answer("Неверный формат возраста. Пожалуйста, введите возраст цифрами. Пример: 18", reply_markup=None)
            return
        data['age'] = message.text
    await update_user_age(message.from_user.id, data['age'])
    await UserForm.location.set()
    await message.answer("Какой ваш город?")
    await message.answer("Выберите город из списка:", reply_markup=await get_location_keyboard())

@dp.callback_query_handler(lambda query: query.data.startswith('location_'), state=UserForm.location)
async def process_location(callback_query: types.CallbackQuery, state: FSMContext):
    location = callback_query.data.split('_')[1]  # Разбиваем и в базу записывается только spb / moscow / sochi
    async with state.proxy() as data:
        data['location'] = location
    await update_user_location(callback_query.from_user.id, location)
    await UserForm.nickname.set()
    await callback_query.message.answer("Как к тебе обращаться? (Эта информация скрыта от остальных пользователей)", reply_markup=None)

@dp.message_handler(state=UserForm.nickname)
async def process_nickname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['nickname'] = message.text
    await update_user_name(message.from_user.id, data['nickname'])
    await UserForm.description.set()
    await message.answer("Напиши краткое описание о себе.", reply_markup=None)

@dp.message_handler(state=UserForm.description)
async def process_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await update_user_description(message.from_user.id, data['description'])
    await add_user_info_to_db(message.from_user.id, data.get('nickname'), data.get('age'), data.get('description'))
    await message.answer("Отлично! Давай теперь заполним твое резюме. Если вдруг у тебя имеется личное резюме, ты сможешь его прикрепить после в личном кабинете.", reply_markup=None)
    await message.answer("Напиши ФИО. (Пример: Константин Гурий Павлович)")
    await UserForm.resume_start.set()
    await UserForm.fullname.set()

@dp.message_handler(state=UserForm.fullname)
async def resume_start(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['fullname'] = message.text
    await update_user_fullname(message.from_user.id, data['fullname'])
    await message.answer("Какое у тебя гражданство?", reply_markup=await get_citizenship_keyboard())
    await UserForm.citizenship.set()

# Шаг 3: Ответ на вопрос о национальности
@dp.message_handler(state=UserForm.citizenship)
async def citizenship(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['citizenship'] = message.text
    await update_user_citizenship(message.from_user.id, data['citizenship'])
    await message.answer("Кем бы вы хотели работать?", reply_markup=await get_position_keyboard())
    await UserForm.desired_position.set()

# Шаг 6: Выбор желаемой позиции
@dp.message_handler(state=UserForm.desired_position)
async def process_desired_position(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['desired_position'] = message.text
    await update_user_desired_position(message.from_user.id, data['desired_position'])
    await UserForm.work_experience.set()
    await message.answer("У вас есть опыт работы?", reply_markup=await get_yes_no_keyboard())

# Шаг 6.1: Если есть опыт работы
@dp.message_handler(lambda message: message.text.lower() == 'да', state=UserForm.work_experience)
async def process_experience_yes(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['experience'] = []
    await UserForm.experience_details.set()
    await message.answer("Отлично! Расскажите о своем опыте работы. Напишите название предыдущего места работы.", reply_markup=None)
    
# Шаг 6.2: Если нет опыта работы
@dp.message_handler(lambda message: message.text.lower() == 'нет', state=UserForm.work_experience)
async def process_experience_no(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['experience'] = "Нет опыта работы"
    await update_user_experience(message.from_user.id, data['experience'])
    await UserForm.skills.set()
    await message.answer("Какими навыками вы обладаете?", reply_markup=None)

# Продолжение для описания опыта работы
@dp.message_handler(state=UserForm.experience_details)
async def process_experience_details(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['experience'].append(message.text)
    await message.answer("Есть ли еще места работы, о которых вы хотите рассказать?", reply_markup=await get_yes_no_keyboard())
    await UserForm.experience_another.set()

# Повторяющиеся вопросы, если есть другой опыт работы
@dp.message_handler(lambda message: message.text.lower() == 'да', state=UserForm.experience_another)
async def process_experience_another_yes(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['experience_details'] = []
    await UserForm.experience_details.set()
    await message.answer("Как называлось ваше предыдущее место работы?", reply_markup=None)

@dp.message_handler(lambda message: message.text.lower() == 'нет', state=UserForm.experience_another)
async def process_experience_another_no(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['experience'] = '\n'.join(data['experience'])
    await update_user_experience_details(message.from_user.id, data['experience'])
    await UserForm.skills.set()
    await message.answer("Какими навыками вы обладаете?", reply_markup=None)
    
@dp.message_handler(state=UserForm.skills)
async def process_skills(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['skills'] = message.text
    await update_user_skills(message.from_user.id, data['skills'])
    await state.update_data(experience=data.get('experience'), skills=data.get('skills'))
    await UserForm.resume_check.set()
    await process_resume_check(message, state)

# Проверка резюме и возможность перезаполнения
@dp.message_handler(state=UserForm.resume_check)
async def process_resume_check(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text.lower() in ['да', 'save_resume', 'сохранить', '/save_resume', 'Сохранить']:
            resume = f"Имя: {data['fullname']}\n" \
                     f"Гражданство: {data['citizenship']}\n" \
                     f"Желаемая позиция: {data['desired_position']}\n" \
                     f"Опыт работы: {data.get('experience')}\n" \
                     f"Навыки: {data.get('skills')}"
            await message.answer(f"Ваше резюме:\n{resume}", reply_markup=None)
            await UserForm.resume_confirmation.set()
            await message.answer("Спасибо за регистрацию.")
        else:
            await message.answer("Желаете что-нибудь подправить или начать заново?", reply_markup=await get_save_restart_keyboard())
    await state.finish()

# Отправка резюме
@dp.message_handler(state=UserForm.resume_confirmation)
async def process_resume_confirmation(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text.lower() == 'да':
            await send_resume(message.from_user.id, data)
            await message.answer("Резюме успешно отправлено!")
            await main_menu_user(message.from_user.id, message.message_id)
        else:
            await message.answer("Хорошо, давайте перезаполним резюме.")
            await resume_start(message=message, state=state)
    await state.finish()

@dp.message_handler(lambda message: message.text == "👤 Личный кабинет", state="*")
async def personal_cabinet(message: types.Message):
    user_id = message.from_user.id

    user_data = await get_user_data(user_id)

    if user_data:
        fullname = user_data.get("fullname")
        age = user_data.get("age")
        description = user_data.get("description")
        location = user_data.get("location")
        status = "Ищу работу"
        skills = user_data.get("skills")
        user_info_text = f"ФИО: {fullname}\nВозраст: {age}\nОписание: {description}\nМестоположение: {location}\nНавыки: {skills}\nСтатус: {status}"

        await message.answer(f'Вот так будет видеть твою анкету работодатель:\n\n{user_info_text}', reply_markup=await get_resume_button())
    else:
        await message.answer("Информация о пользователе не найдена.", reply_markup=None)

@dp.message_handler(lambda message: message.text == "Назад", state="*")
async def back_to_main_menu(message: types.Message):
    user_id = message.from_user.id
    user_data = await get_user_data(user_id)
    if user_data:
        name = user_data.get("name")
        await main_menu_user(user_id, name)
    else:
        await message.answer("Информация о пользователе не найдена. Пройдите регистрацию нажав на команду /start", reply_markup=None)

@dp.message_handler(lambda message: message.text == "ℹ️ О боте", state="*")
async def about_bot(message: types.Message):
    about_text = "Данный бот был создан для помощи компаниям в сфере общепита быстрее найти работников."
    await message.answer(about_text)

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

    await message.answer(help_text, reply_markup=None)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
