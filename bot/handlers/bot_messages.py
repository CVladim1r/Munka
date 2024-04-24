from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
import asyncio
import json
import os
import aiogram
from aiogram import Router, F, Bot, types
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram.methods.send_photo import SendPhoto


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

from aiogram.types.input_file import InputFile
from bot.utils.states import *

from bot.keyboards.inline import *
from bot.keyboards.reply import *

from bot.database.db_connector import *
from bot.database.methods import *

from bot.utils.format_data import *

from bot.config_reader import config


router = Router()
bot = Bot(config.bot_token.get_secret_value(), parse_mode='HTML')


async def main_menu_user(user_id, message_id):
    main_text = "Искать вакансии\n"
    main_text += "Личный кабинет\n"
    main_text += "Редактировать резюме\n"
    main_text += "О боте\n"
    await bot.send_message(user_id, main_text, reply_markup=await get_choose_menu_user_buttons(), disable_notification=True)

@router.message(F.text=='🔍 Искать Вакансии')
async def seacrh_vacancies(msg: Message):
    user_id = msg.from_user.id
    user_data = await get_user_data(user_id)
    
    if user_data:
        random_vacancy = await get_random_vacancy_for_user(user_id)
        
        if random_vacancy:
            formatted_vacancy = await format_vacancy(random_vacancy)
            await msg.answer(
                formatted_vacancy,
                parse_mode="HTML",
                reply_markup=await get_send_or_dislike_resume_keyboard()
            )
        else:
            await msg.answer(
                "К сожалению, не удалось найти вакансии. Попробуйте еще раз позже.",
                reply_markup=None
            )

    else: 
        await msg.answer(
            "Похоже что ты не зарегистрирован в системе. Самое время пройти регистраицю! /start",
            reply_markup=None
        )
        
@router.message(F.text=="👎")
async def dislike_resume(msg: Message):
    user_id = msg.from_user.id
    user_data = await get_user_data(user_id)

    if user_data:
        random_vacancy = await get_random_vacancy_for_user(user_id)

        if random_vacancy:
            formatted_vacancy = await format_vacancy(random_vacancy)
            await msg.answer(
                formatted_vacancy,
                parse_mode="HTML",
                reply_markup=await get_send_or_dislike_resume_keyboard()
            )
        else:
            await msg.answer(
                "К сожалению, не удалось найти вакансии. Попробуйте еще раз позже.",
                reply_markup=None
            )

@router.message(F.text=="✉")
async def send_resume_vacancy(msg: Message):
    user_id = msg.from_user.id
    user_data = await get_user_data(user_id)

    if user_data:
        await msg.answer("Резюме отправлено!\n\nТеперь можно перейти к просмотру анкет дальше!")
        await seacrh_vacancies(msg)

@router.message(F.text == '😴')
async def personal_sleep(msg: Message):
    await msg.answer("Отлично! Самое время сделать перерв 😁", reply_markup=await get_choose_menu_user_buttons()) 

@router.message(F.text == '👤 Личный кабинет')
async def personal_cabinet(msg: Message):
    user_id = msg.from_user.id

    user_data = await get_user_data(user_id)

    path_to_photo = f'img/{msg.from_user.username}\\photo.jpg'


    await msg.answer("Вот как выглядит твое резюме:")
    data = await get_user_data(user_id)


    resume = f"ФИО: {data['user_fio']}\n" \
            f"Гражданство: {data['user_citizenship']}\n" \
            f"Желаемая позиция: {data['user_desired_position']}\n" \
            f"Опыт работы:\n"
    experience_data = {
            "company_name": data.get("user_company_name"),\
            "experience_period": data.get("experience_period"),\
            "experience_position": data.get("experience_position"),\
            "experience_duties": data.get("experience_duties")\
        }
    resume += str(experience_data)
    desired_salary = data.get('user_desired_salary_level', 'Не указано')
    employment_type = data.get('user_employment_type', 'Не указано')
    resume += f"Желаемая зарплата: {desired_salary}\n" \
            f"Желаемая занятость: {employment_type}\n"

    await bot.send_photo(msg.chat.id, photo=types.FSInputFile(path_to_photo), caption=resume, reply_markup=await get_save_restart_keyboard())



@router.message(F.text== '↩️ Назад')
async def back_to_main_menu(msg: Message):
    user_id = msg.from_user.id
    user_data = await get_user_data(user_id)
    if user_data:
        name = user_data.get("name")
        await main_menu_user(user_id, name)
    else:
        await msg.answer("Информация о пользователе не найдена. Пройдите регистрацию нажав на команду /start", reply_markup=None)

@router.message(F.text=='ℹ️ О боте')
async def about_bot(msg: Message):
    about_text = "Данный бот был создан для помощи компаниям в сфере общепита быстрее найти работников."
    await msg.answer(about_text)
    
@router.message(F.text=='✏️ Редактировать резюме')
async def red_resume(msg: Message):
    await msg.answer("Желаете что-нибудь подправить или начать заново?", reply_markup=await get_save_restart_keyboard())