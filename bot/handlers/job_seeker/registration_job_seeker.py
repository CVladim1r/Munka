import asyncio
import json
import os
import aiogram
from aiogram import Router, F, Bot, types
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.base import (
    BaseEventIsolation,
    BaseStorage,
    StateType,
    StorageKey,
)
from bot.cities import CITIES
from bot.utils import format_vacancy
from bot.config_reader import config
from bot.keyboards import *
from bot.utils.states import *
from bot.database.methods import *

from bot.handlers.bot_messages import *



async def register_job_seeker(user_tgid, user_tgname, user_fullname, state: FSMContext):
    """
    Регистрация соискателя.
    :param user_tgid: Telegram ID пользователя
    :param user_tgname: Telegram username пользователя
    :param user_fullname: Полное имя пользователя
    """
    # Здесь код для регистрации соискателя в базе данных:
    # await db.save_user(user_tgid, user_tgname, user_fullname, user_type="JOB_SEEKER")

    # Вместо прямого вызова функций proc_age и process_location будем устанавливать состояния FSM
    await state.set_state(UserForm.fio)

# Поиск города для сохранения в normalize_location
async def normalize_city(city_name):
    print(f"Searching for city: {city_name}")
    for key, variants in CITIES.items():
        for variant in variants:
            if city_name.lower() in variant:
                print(f"Found city: {key}")
                return key
    return None

# Вопрос про ФИО для соискателя
@router.message(UserForm.fio)
async def process_fio(msg: Message, state: FSMContext):
    await state.update_data(fio=msg.text)
    data = await state.get_data()
    new_name = data.get('fio')

    # Обновление ФИО в базе данных
    await update_fio(msg.from_user.id, new_name)

    # Продолжаем диалог
    await state.set_state(UserForm.age)

    await msg.answer("Сколько тебе полных лет?\nНапример: 21", reply_markup=None)

# Вопрос про возраст для соискателя
@router.message(UserForm.age)
async def process_age(msg: Message, state: FSMContext):
    if int(msg.text) >= 14:
        if not msg.text.isdigit() or not (0 < int(msg.text) < 99):
            await msg.answer("Неверный формат возраста. Пожалуйста, введите возраст цифрами. Пример: 18", reply_markup=rmk)
            return
    elif msg.text == "писят два":
        await msg.answer("Отсылочка )))\nЛадно, давай повторим..", reply_markup=rmk)
        await state.set_state(UserForm.age)

        await msg.answer("Сколько тебе полных лет?\nНапример: 21", reply_markup=rmk)
        return
    else:
        await msg.answer('''К сожалению, в России можно работать только с 14 лет.
Но время летит быстро!
Мы будем тебя ждать ❤️''', reply_markup=rmk)
        await msg.answer("Но если ты просто ошибся с возрастом, то ты можешь его изменить", reply_markup=await get_change_age())
        return
    
    await state.update_data(age=msg.text)
    dats = await state.get_data()
    data = dats.get('age')
    await update_user_age(msg.from_user.id, data)
    await state.update_data(age=msg.text)
    
    await msg.answer("В каком городе планируешь работать?", reply_markup=await get_location_keyboard())
    await state.set_state(UserForm.location)

# Если вдруг пользователь ошибся
@router.callback_query(lambda c: c.data == 'change_age')
async def change_age(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer("Давайте попробуем еще раз")
    await callback_query.message.answer("Сколько тебе полных лет?\nНапример: 21", reply_markup=rmk)
    await state.set_state(UserForm.age)

# Наши Солевые и Московские друзья :)
@router.callback_query(lambda c: c.data == 'msk' or c.data == 'spb')
async def process_location_msk_spb(callback_query: CallbackQuery, state: FSMContext):
    location = callback_query.data 
    if callback_query.data == 'msk':  
        location = 'msk'
    else:
        location = 'spb'

    data = await state.get_data()
    data['location_text'] = location
    data['location'] = location
    await state.update_data(location=location)
    await update_user_location(callback_query.from_user.id, location)
    await state.update_data(location=location)
    await state.set_state(UserForm.user_what_is_your_name)
    await callback_query.message.answer("Ты гражданин какой страны?", reply_markup=await get_citizenship_keyboard())

# Наши не Солевые и Московские друзья :(
@router.callback_query(lambda c: c.data == 'other_location')
async def change_location_other(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await callback_query.message.answer("Напиши город:", reply_markup=rmk)
    await state.set_state(UserForm.location_retry)

# Наши не Солевые и Московские друзья и их добавление в бд :(
@router.message(UserForm.location_retry)
async def process_location(msg: Message, state: FSMContext):
    location = msg.text
    normalized_location = await normalize_city(location)

    if normalized_location is None:
        await msg.answer("К сожалению, мы не можем разобрать, что это за город. Пожалуйста, введи его снова.")
        return
    
    data = await state.get_data()
    data['location_text'] = location
    data['location'] = normalized_location
    await state.update_data(location=location)
    await update_user_location(msg.from_user.id, normalized_location)
    await state.update_data(location=normalized_location)
    await msg.answer("Ты гражданин какой страны?", reply_markup=await get_citizenship_keyboard())
# Варик без расчленения
'''
@router.message(UserForm.location)
async def process_location(msg: Message, state: FSMContext):
    location = msg.text
    normalized_location = await normalize_city(location)
    data = await state.get_data()
    data['location_text'] = msg.text

    await state.update_data(location=location)
    await update_user_location(msg.from_user.id, normalized_location)
    await state.update_data(location=normalized_location)
    await state.set_state(UserForm.user_what_is_your_name)
    await msg.answer("Как к тебе обращаться? (Эта информация скрыта от остальных пользователей)", reply_markup=rmk)
'''


# Скипаем вопрос "Как обращаться к тебе?" 
'''
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
'''
    

# Наши Солевые и Московские друзья :)
@router.callback_query(lambda c: c.data == 'citizen_Russian_Federation')
async def process_citizen_Russian_Federation(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await callback_query.message.answer("Выбери желаемую должность:", reply_markup=await get_position_keyboard())

    data = await state.get_data()
    data['citizenship'] = "rus"
    await state.update_data(citizenship="rus")  # Update the state data
    await update_user_citizenship(callback_query.from_user.id, data['citizenship'])
    await state.set_state(UserForm.desired_position)  # Set the next state directly

# Наши не Солевые и Московские друзья :(
@router.callback_query(lambda c: c.data == 'other_citizen')
async def change_other_citizen(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await callback_query.message.answer("Гражданином какой страны ты являешься?\nНапример: Казахстан", reply_markup=rmk)
    data = await state.get_data()
    data['citizenship'] = callback_query.message.text
    await state.set_state(UserForm.citizenship)

@router.message(UserForm.citizenship)
async def process_citizenship(msg: Message, state: FSMContext):
    data = await state.get_data()
    await update_user_citizenship(msg.from_user.id, data['citizenship'])
    await msg.answer("Выбери желаемую должность:", reply_markup=await get_position_keyboard())
    await state.set_state(UserForm.desired_position)


@router.message(UserForm.desired_position)
async def process_desired_position(msg: Message, state: FSMContext):
    await state.update_data(desired_position=msg.text)
    data = await state.get_data()
    await update_user_desired_position(msg.from_user.id, data['desired_position'])
    await state.set_state(UserForm.user_desired_salary_level)
    await msg.answer("Какую зарплату ты бы хотел получать?\nНапример: 50 000", reply_markup=rmk)


@router.message(UserForm.user_desired_salary_level)
async def process_user_desired_salary_level(msg: Message, state: FSMContext):
    await state.update_data(user_desired_salary_level=msg.text)
    data = await state.get_data()
    await update_user_desired_salary_level(msg.from_user.id, data['user_desired_salary_level'])
    await msg.answer("Какая занятость тебя интересует ?", reply_markup=await get_employment_keyboard())

@router.callback_query(lambda c: c.data == 'full_employment' or c.data == 'part-time_employment')
async def process_desired_position(callback_query: CallbackQuery, state: FSMContext):
    message = callback_query.message
    if callback_query.data == 'full_employment':
        employment = 'full_employment'
    else:
        employment = 'part-time_employment'

    # Update the state data with the desired position
    await state.update_data(desired_position=message.text)

    # Update the user's desired position
    await update_user_desired_position(callback_query.from_user.id, employment)

    # Set the next state and send a message
    await state.set_state(UserForm.work_experience)
    await message.answer("Был ли у тебя опыт работы?", reply_markup=await get_position_keyboard())







@router.message(UserForm.work_experience)
async def proc_experience(msg: Message, state: FSMContext):
    if msg.text.lower() == 'да':
        await state.set_state(UserForm.experience_details)
        await msg.answer("Отлично! Расскажите о своем опыте работы. Напишите название предыдущего места работы.", reply_markup=rmk)
    elif msg.text.lower() == 'нет':
        await state.update_data(work_experience="Нет опыта работы")
        await state.set_state(UserForm.resume_check)
        await msg.answer("Вот и подошла регистрация к концу :)", reply_markup=rmk)
    else:
        await msg.answer("Пожалуйста, ответьте 'да' или 'нет'.", reply_markup=rmk)

@router.message(UserForm.experience_details)
async def process_experience_details(msg: Message, state: FSMContext):
    await state.update_data(company_name=msg.text)
    await state.set_state(UserForm.experience_period)
    await msg.answer("Введите период работы в формате: 11.2020-09.2022", reply_markup=rmk)

@router.message(UserForm.experience_period)
async def process_experience_period(msg: Message, state: FSMContext):
    await state.update_data(experience_period=msg.text)
    await state.set_state(UserForm.experience_position)
    await msg.answer("Какую должность ты занимал?", reply_markup=rmk)

@router.message(UserForm.experience_position)
async def process_experience_position(msg: Message, state: FSMContext):
    await state.update_data(experience_position=msg.text)
    await state.set_state(UserForm.experience_duties)
    await msg.answer("Расскажи, какие у тебя были обязанности на этой работе? Старайся отвечать на этот вопрос максимально кратко и лаконично, при этом не упуская главной сути", reply_markup=rmk)
    await msg.answer("Например: Я варил для моих посетителей – котиков, самое лучшее молоко, с пенкой. А в конце смены, я подметал полы от следов лапок, и вел учет, сколько кошачьей мяты поступило в кассу, а сколько было потрачено", reply_markup=rmk)


@router.message(UserForm.experience_duties)
async def process_experience_duties(msg: Message, state: FSMContext):
    await state.update_data(experience_duties=msg.text)
    await state.set_state(UserForm.experience_another)
    await msg.answer("Был ли у вас другой опыт работы?", reply_markup=await get_yes_no_keyboard())

@router.message(UserForm.experience_another)
async def process_experience_another(msg: Message, state: FSMContext):
    if msg.text.lower() == 'да':
        await state.set_state(UserForm.experience_details)
        await msg.answer("Отлично! Напишите название предыдущего места работы.", reply_markup=rmk)
    elif msg.text.lower() == 'нет':
        data = await state.get_data()
        experience_data = {
            "company_name": data.get("company_name"),
            "experience_period": data.get("experience_period"),
            "experience_position": data.get("experience_position"),
            "experience_duties": data.get("experience_duties")
        }
        # Сохранение опыта работы
        await update_user_experience(msg.from_user.id, experience_data)
        await state.set_state(UserForm.additional_info)
        await msg.answer("Есть навыки? Напиши их!", reply_markup=finReg)
    else:
        await msg.answer("Пожалуйста, ответьте 'да' или 'нет'.", reply_markup=await get_yes_no_keyboard())



@router.message(UserForm.additional_info)
async def process_additional_info(msg: Message, state: FSMContext):
    if msg.text.lower() == 'да':
        await state.set_state(UserForm.additional_info_details)
        await msg.answer("Здесь ты можешь рассказать о своих навыках и умениях", reply_markup=rmk)
    elif msg.text.lower() == 'нет':
        await state.set_state(UserForm.photo_upload)
        await msg.answer("Чего-то не хватает. Соли? Перца? Фотографии! Ждем твое фото 🔥", reply_markup=rmk)
    else:
        await msg.answer("Пожалуйста, ответьте 'да' или 'нет'.", reply_markup=await get_yes_no_keyboard())


@router.message(UserForm.additional_info_details)
async def process_additional_info_details(msg: Message, state: FSMContext):
    additional_info = msg.text
    await state.update_data(additional_info=additional_info)
    await state.set_state(UserForm.photo_upload)
    await msg.answer("Чего-то не хватает. Соли? Перца? Фотографии! Ждем твое фото 🔥", reply_markup=rmk)





@router.message(UserForm.photo_upload)
async def photo_upload(message: types.Message, state: FSMContext):
    if message.photo:
        try:
            file_info = await bot.get_file(message.photo[-1].file_id)
            file_path = file_info.file_path
            file_name = file_path.split('/')[-1]
            await bot.download_file(file_path, file_name)
            await state.update_data(photo_path=file_name)
            await message.answer("Фотография успешно загружена!")
        except aiogram.client.errors.TelegramAPIError as e:
            if e.error_code == 404:
                await message.answer("Файл не найден. Пожалуйста, попробуйте загрузить его еще раз.")
                return
            else:
                raise e
    else:
        await message.answer("Пожалуйста, загрузите фотографию.")





@router.message(UserForm.resume_check)
async def process_resume_check(msg: Message, state: FSMContext):
    await state.update_data(resume_check=msg.text)
    data = await state.get_data()
    
    resume = f"ФИО: {data['fio']}\n" \
             f"Гражданство: {data['citizenship']}\n" \
             f"Желаемая позиция: {data['desired_position']}\n" \
             f"Опыт работы:\n"
    experience_data = {
            "company_name": data.get("company_name"),\
            "experience_period": data.get("experience_period"),\
            "experience_position": data.get("experience_position"),\
            "experience_duties": data.get("experience_duties")\
        }
    resume += str(experience_data)
    
    desired_salary = data.get('user_desired_salary_level', 'Не указано')
    employment_type = data.get('user_employment_type', 'Не указано')
    
    resume += f"Желаемая зарплата: {desired_salary}\n" \
              f"Желаемая занятость: {employment_type}\n"
    
    # Добавляем путь к фотографии в текст резюме, если он есть
    photo_path = data.get("photo_path")
    if photo_path:
        resume += f"Фото: {photo_path}\n"
    
    await msg.answer(f"Ваше резюме:\n\n{resume}\n\nЖелаете что-нибудь подправить или начать заново?", 
                     reply_markup=await get_save_restart_keyboard())


@router.callback_query()
async def proc_con(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.data == 'save_resume' or callback_query.message.text.lower() in ['да', 'save_resume', 'сохранить', '/save_resume', 'Сохранить']:
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
    await process_fio(msg=msg, state=state)
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
        await process_fio(msg=msg, state=state)
    await state.clear()