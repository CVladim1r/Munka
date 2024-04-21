from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
import asyncio
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from database.db_connector import *
from database.db_connector import get_random_vacancy_for_user
from user_registration import *
from cities import CITIES
from bot.utils.format_data import format_vacancy
from config_reader import config
from keyboards.inline import *
from keyboards.reply import *
from utils.states import *

router = Router()
bot = Bot(config.bot_token.get_secret_value(), parse_mode='HTML')

async def main_menu_user(user_id, message_id):
    main_text = "Искать вакансии\n"
    main_text += "Личный кабинет\n"
    main_text += "Редактировать резюме\n"
    main_text += "О боте\n"
    await bot.send_message(user_id, main_text, reply_markup=await get_choose_menu_user_buttons(), disable_notification=True)

async def main_menu_employer(user_id, message_id):
    main_text = "Искать вакансии:\n"
    main_text += "Личный кабинет\n"
    main_text += "Редактировать резюме\n"
    main_text += "О боте\n"
    await bot.send_message(user_id, main_text, reply_markup=await get_choose_menu_employer_buttons(), disable_notification=True)

async def normalize_city(city_name):
    print(f"Searching for city: {city_name}")
    for key, variants in CITIES.items():
        for variant in variants:
            if city_name.lower() in variant:
                print(f"Found city: {key}")
                return key
    return None




@router.message(CommandStart())
async def start(msg: Message, state: FSMContext):
    user_tgid = msg.from_user.id
    
    await state.set_state(UserForm.user_tgid)
    await state.update_data(user_tgid=user_tgid)
    
    user_data = await get_user_data(user_tgid)
    employer_data = await get_employer_data(user_tgid)

    if employer_data:
        await main_menu_employer(user_tgid, msg.chat.id)
        return
    
    elif user_data:
        user_type = user_data.get("user_type")
        if user_type == "USER":
            await main_menu_user(user_tgid, msg.chat.id)
            return

    await state.set_state(UserForm.user_fullname)
    user_tgname = msg.from_user.full_name
    await state.update_data(user_fullname=user_tgname)
    
    await state.set_state(UserForm.user_tgname)
    userName = msg.from_user.username
    await state.update_data(user_tgname=userName)
    
    if not user_tgname:
        user_tgname = str(user_tgid)


    await bot.send_message(msg.chat.id, '''Привет я кот Миша.\nЯ выполняю здесь самую главную функцию: помогаю соискателям и работодателям найти друг друга. Представь, у каждого есть работа, а в мире царит гармония – мяу, красота. Для этого я здесь.''', reply_markup=None)

    # Позже надо реализовать не через asyncio.sleep
    await asyncio.sleep(4)
    await msg.answer("Давай теперь познакомимся поближе. Кто ты?", reply_markup=await get_choose_rule())


@router.callback_query(lambda c: c.data in ["job_seeker", "employer"])
async def process_user_type(callback_query: CallbackQuery, state: FSMContext):
    user_type = callback_query.data

    data = await state.get_data()
    user_tgid = data.get('user_tgid')
    user_fullname = data.get('user_fullname')
    user_tgname = data.get('user_tgname')
    
    if user_type == "job_seeker":
        await register_job_seeker(user_tgid, user_tgname, user_fullname)
        await callback_query.message.answer("Хорошо, давай теперь познакомимся. Напиши свой возраст:", reply_markup=None)
        await state.set_state(UserForm.age)

    elif user_type == "employer":
        await register_employer(callback_query.message, user_tgid, user_fullname, user_tgname)
        
@router.message(UserForm.age)
async def proc_age(msg: Message, state: FSMContext):
    if int(msg.text) >= 16:
        if not msg.text.isdigit() or not (0 < int(msg.text) < 99):
            await msg.answer("Неверный формат возраста. Пожалуйста, введите возраст цифрами. Пример: 18", reply_markup=None)
            return
        
    else:
        await msg.answer('''Извините, но для использования этого сервиса вам должно быть 16 лет или старше. 
                                 Тем не менее, обратите внимание, что многие работодатели предпочитают нанимать людей старше 16 лет из-за 
                                 их более широкого опыта и профессионализма.''', reply_markup=None)
        return
    await state.update_data(age=msg.text)
    dats = await state.get_data()
    data = dats.get('age')
    await update_user_age(msg.from_user.id, data)
    await state.update_data(age=msg.text)
    await state.set_state(UserForm.location)
    await msg.answer("Из какого ты города?\nВыбери из списка или напиши свой вариант:", reply_markup=await get_location_keyboard())
    
    
@router.message(UserForm.location)
async def process_location(msg: Message, state: FSMContext):
    location = msg.text
    normalized_location = await normalize_city(location)
    data = await state.get_data()
    await state.update_data(location=location)
    await update_user_location(msg.from_user.id, normalized_location)
    await state.update_data(location=normalized_location)
    await state.set_state(UserForm.user_what_is_your_name)
    await msg.answer("Как к тебе обращаться? (Эта информация скрыта от остальных пользователей)", reply_markup=None)



@router.message(UserForm.user_what_is_your_name)
async def procName(msg: Message, state: FSMContext):
    await state.update_data(user_what_is_your_name=msg.text)
    data = await state.get_data()
    data['user_what_is_your_name'] = msg.text
    await update_user_name(msg.from_user.id, msg.text)
    await state.set_state(UserForm.resume_start)
    await state.set_state(UserForm.fullname)
    await msg.answer("Отлично! Давай теперь заполним твое резюме.\nНапиши ФИО. (Пример: Константин Гурий Павлович)")
    
    
@router.message(UserForm.fullname)
async def resume_start(msg: Message, state: FSMContext):
    await state.update_data(fullname=msg.text)
    data = await state.get_data()
    await update_user_fullname(msg.from_user.id, data.get('fullname'))
    await msg.answer("Откуда ты? (Напиши текстом если среди вариантов ниже нет твоего)", reply_markup=await get_citizenship_keyboard())
    await state.set_state(UserForm.citizenship)
    
    
@router.message(UserForm.citizenship)
async def procFull(msg: Message, state: FSMContext):
    await state.update_data(citizenship=msg.text)
    data = await state.get_data()
    await update_user_citizenship(msg.from_user.id, data['citizenship'])
    await msg.answer("Кем бы вы хотели работать? (Напиши текстом если среди вариантов ниже нет твоего)", reply_markup=await get_position_keyboard())
    await state.set_state(UserForm.desired_position)
    
    
@router.message(UserForm.desired_position)
async def process_desired_position(msg: Message, state: FSMContext):
    await state.update_data(desired_position=msg.text)
    data = await state.get_data()
    await update_user_desired_position(msg.from_user.id, data['desired_position'])
    await state.set_state(UserForm.work_experience)
    await msg.answer("У вас есть опыт работы?", reply_markup=await get_yes_no_keyboard())

@router.message(UserForm.work_experience)
async def proc_expirenece_yes(msg: Message, state: FSMContext):
    if msg.text.lower() == 'да':
        dt = await state.get_data()
        data = dt.get('experience')
        data = []
        await state.set_state(UserForm.experience_details)
        await msg.answer("Отлично! Расскажите о своем опыте работы. Напишите название предыдущего места работы.", reply_markup=None)
    elif msg.text.lower() == 'нет':
        await state.update_data(work_experience="Нет опыта работы")
        await state.set_state(UserForm.skills)
        await msg.answer("Какими навыками вы обладаете?", reply_markup=rmk)
    
@router.message(UserForm.experience_details)
async def process_experience_details(msg: Message, state: FSMContext):
    data = []
    data.append({
        'company_name': msg.text,
        'description': None
    })
    await state.update_data(experience_details=data)
    await state.set_state(UserForm.experience_description)
    await msg.answer("Опишите вашу работу в данной компании.", reply_markup=rmk)  # Убрать клавиатуру
    
@router.message(UserForm.experience_description)
async def process_experience_description(msg: Message, state: FSMContext):
    data = await state.get_data()
    await state.update_data(experience_description=msg.text)
    data['experience_details']['description'] = None
    await state.set_state(UserForm.experience_another)

@router.message(UserForm.experience_another)
async def process_experience_another(msg: Message, state: FSMContext):
    if msg.text.lower() == 'да':
        new_experience = {
            'company_name': msg.text,
            'description': None
        }
        data = await state.get_data()
        data['experience'].append(new_experience)
        await state.set_state(UserForm.experience_details)
        await msg.answer("Опишите вашу работу в данной компании.", reply_markup=rmk)
    elif msg.text.lower() == 'нет':
        data = await state.get_data()
        experience_json = json.dumps(data['experience'])
        await update_user_experience(msg.from_user.id, experience_json)
        await state.set_state(UserForm.skills)
        await msg.answer("Какими навыками вы обладаете?", reply_markup=rmk)
    
    
@router.message(UserForm.skills)
async def process_skills(msg: Message, state: FSMContext):
    await state.update_data(skills=msg.text)
    dt = await state.get_data()
    data = dt.get('skills')
    await update_user_skills(msg.from_user.id, data)
    await state.set_state(UserForm.resume_check)
    await msg.answer("Подтвердите окончание регистрации", reply_markup=finReg)
    
@router.message(UserForm.resume_check)
async def process_resume_check(msg: Message, state: FSMContext):
    await state.update_data(resume_check=msg.text)
    data = await state.get_data()
    resume = f"Имя: {data['fullname']}\n" \
             f"Гражданство: {data['citizenship']}\n" \
             f"Желаемая позиция: {data['desired_position']}\n" \
             f"Опыт работы:\n"
    for experience in data.get('experience', []):
        resume += f"- {experience['company_name']}: {experience['description']}\n"
    resume += f"Навыки: {data.get('skills')}"
    await msg.answer(f"Ваше резюме: {resume}\n\n Желаете что-нибудь подправить или начать заново?", reply_markup=await get_save_restart_keyboard())


@router.callback_query()
async def proc_con(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.data == 'save resume' or callback_query.message.text.lower() in ['да', 'save_resume', 'сохранить', '/save_resume', 'Сохранить']:
        await state.set_state(UserForm.resume_confirmation)
        await send_resume(callback_query.from_user.id, await state.get_data())
        await state.update_data(resume_confirmation="Отправлено")
        await callback_query.message.answer("Резюме успешно отправлено!")
        await main_menu_user(callback_query.from_user.id, callback_query.message.message_id)
    elif callback_query.data == 'restart_resume' or callback_query.message.text.lower() in ['нет', 'restart_resume', 'отмена', '/restart_resume', 'Отмена']:
        await restart_resume(callback_query.message, state)
    else: 
        await process_resume_confirmation(callback_query.message, state)
    await state.clear()


async def restart_resume(msg: Message, state: FSMContext):
    await state.reset_state()
    await msg.answer("Процесс заполнения резюме начат заново.")
    await resume_start(msg=msg, state=state)
    await UserForm.fullname.set()
    
@router.message(UserForm.resume_confirmation)
async def process_resume_confirmation(msg: Message, state: FSMContext):
    data = await state.get_data()
    if msg.text.lower()=='да':
        await send_resume(msg.from_user.id, data)
        await msg.answer("Резюме успешно отправлено!")
        await main_menu_user(msg.from_user.id, msg.message_id)
    else: 
        await msg.answer("Хорошо, давайте перезаполним резюме.")
        await resume_start(msg=msg, state=state)
    await state.clear()
    

@router.message(Command('help'))
async def help_command(msg: Message):
    help_text = "Список доступных команд:\n" \
                "/start - Начать диалог с ботом\n" \
                "/help - Получить список доступных команд\n" \
                "Личный кабинет - Просмотреть информацию о пользователе\n" \
                "Искать Вакансии - Поиск вакансий\n" \
                "Редактировать резюме - Изменить информацию о себе\n" \
                "О боте - Информация о боте\n"

    await msg.answer(help_text, reply_markup=None)
    
@router.message(Command('about'))
async def about_command(msg: Message):
    user_id = msg.from_user.id
    user_data = await get_user_data(user_id)

    if user_data:
        await main_menu_user(msg.from_user.id, msg.message_id)
    else:
        await msg.answer('SuckMyDickBROOO', reply_markup=None)