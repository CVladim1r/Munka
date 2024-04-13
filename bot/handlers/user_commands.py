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
from format_data import format_vacancy
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
        await main_menu_employer(user_tgid, msg.msg_id)
        return
    
    elif user_data:
        user_type = user_data.get("user_type")
        if user_type == "USER":
            await main_menu_user(user_tgid, msg.msg_id)
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
        await state.set_state(UserForm.regStart)

    elif user_type == "employer":
        await register_employer(callback_query.message, user_tgid, user_fullname, user_tgname)
        
@router.message(UserForm.age)
async def proc_age(msg: Message, state: FSMContext):
    async with state.proxy() as data:
        if int(msg.text) >= 16:
            if not msg.text.isdigit() or not (0 < int(msg.text) < 99):
                await msg.answer("Неверный формат возраста. Пожалуйста, введите возраст цифрами. Пример: 18", reply_markup=None)
                return
            data['age'] = msg.text
        else:
            await msg.answer('''Извините, но для использования этого сервиса вам должно быть 16 лет или старше. 
                                 Тем не менее, обратите внимание, что многие работодатели предпочитают нанимать людей старше 16 лет из-за 
                                 их более широкого опыта и профессионализма.''', reply_markup=None)
            return
    await update_user_age(msg.from_user.id, data['age'])
    await state.update_data(age=msg.text)
    await state.set_state(UserForm.location)
    await msg.answer("Из какого ты города?\nВыбери из списка или напиши свой вариант:", reply_markup=await get_location_keyboard())
    
    
@router.message(UserForm.location)
async def process_location(callback_query: CallbackQuery, state: FSMContext):
    location = callback_query.data.split('_')[1]
    normalized_location = await normalize_city(location)

    if normalized_location:
        async with state.proxy() as data:
            data['location'] = normalized_location

        if normalized_location in CITIES:
            async with state.proxy() as data:
                data['location_short'] = normalized_location

        await update_user_location(callback_query.from_user.id, normalized_location)
        await state.set_state(UserForm.user_what_is_your_name)
        await callback_query.message.answer("Как к тебе обращаться? (Эта информация скрыта от остальных пользователей)", reply_markup=None)
    else:
        await callback_query.message.answer("Указанный город не найден в списке доступных городов.", reply_markup=None)

@router.message(UserForm.user_what_is_your_name)
async def procName(msg: Message, state: FSMContext):
    await state.update_data(user_what_is_your_name=msg.text)
    await state.set_state(UserForm.fullname)
    await msg.answer("Отлично! Давай теперь заполним твое резюме.\nНапиши ФИО. (Пример: Константин Гурий Павлович)")
    
@router.message(UserForm.fullname)
async def procFull(msg: Message, state: FSMContext):
    async with state.proxy() as data:
        data['fio'] = msg.text
    await update_user_fullname(msg.from_user.id, data['fio'])
    await state.update_data(fullname=msg.text)
    await msg.answer("Откуда ты? (Напиши текстом если среди вариантов ниже нет твоего)", reply_markup=await get_citizenship_keyboard())
    await state.set_state(UserForm.citizenship)
    
@router.message(UserForm.citizenship)
async def procFull(msg: Message, state: FSMContext):
    async with state.proxy() as data:
        data['citizenship'] = msg.text
    await update_user_citizenship(msg.from_user.id, data['citizenship'])
    await state.update_data(citizenship=msg.text)
    await msg.answer("Кем бы вы хотели работать? (Напиши текстом если среди вариантов ниже нет твоего)", reply_markup=await get_position_keyboard())
    await state.set_state(UserForm.desired_position)