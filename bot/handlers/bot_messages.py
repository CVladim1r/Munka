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
from bot.keyboards import *
from bot.database.methods import *

from bot.handlers.bot_messages import *

from bot.utils.states import *
from bot.utils.format_data import *
from bot.utils.states import *
from bot.utils import format_vacancy

from bot.keyboards.inline import *
from bot.keyboards.reply import *

from bot.database.db_connector import *
from bot.database.methods import *

from bot.config_reader import config


router = Router()
bot = Bot(config.bot_token.get_secret_value(), parse_mode='HTML')


router = Router()

async def main_menu_user(user_id, message_id):
    main_text = "Искать вакансии\n"
    main_text += "Личный кабинет\n"
    main_text += "Редактировать резюме\n"
    main_text += "О боте\n"
    await bot.send_message(user_id, main_text, reply_markup=await get_choose_menu_user_buttons(), disable_notification=True)
@router.message(F.text == '👤 Личный кабинет')
async def personal_cabinet(msg: Message):
    user_id = msg.from_user.id

    path_to_photo = f'img/{msg.from_user.username}\\photo.jpg'

    await msg.answer("Вот как выглядит твое резюме:")
    data = await get_user_data(user_id)
    
    resume = f"<b>{data['user_desired_position']}</b>\n" \
             f"<u>{data['user_fio']}</u>\n" \
             f"Возраст: {data['user_age']}\n" \
             f"Город: {data['user_location_text']}\n" \
             f"Гражданство: {data['user_citizenship']}\n" \
             f"Желаемый уровень з/п: {data['user_desired_salary_level']}\n" \
             f"Занятость: {data.get('user_employment_type', 'Не указано')}\n\n" \
             f"<i>Опыт работы:</i>\n" \
             
    experience = json.loads(data['user_experience'])
    if isinstance(experience, dict):  # Проверяем, что опыт работы представлен словарем (ихвильних)
        resume += f"<b>{experience.get('company_name', 'Не указано')}</b>\n" \
                  f"Период работы: {experience.get('experience_period', 'Не указано')}\n" \
                  f"Должность: {experience.get('experience_position', 'Не указано')}\n" \
                  f"Основные обязанности: {experience.get('experience_duties', 'Не указано')}\n\n" \
                  
    else:
        resume += "Не указано\n"
    
    additional_info = data.get('user_additional_info', 'Не указано')
    resume += f"<i>Дополнительная информация:</i> {additional_info}\n"
    
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