import os
import traceback

from aiogram import types
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.cities import CITIES
from bot.utils import format_vacancy
from bot.keyboards import *
from bot.utils.states import *
from bot.database.methods import *
from bot.handlers.bot_messages import *


async def register_job_seeker(user_tgid, state: FSMContext):
    """
    Регистрация работодателя.
    :param employer_tgid: Telegram ID пользователя
    :param employer_tgname: Telegram username пользователя
    """
    # Здесь код для регистрации соискателя в базе данных:
    # await db.save_user(user_tgid, user_tgname, user_fullname, user_type="JOB_SEEKER")

    # Вместо прямого вызова функций proc_age и process_location будем устанавливать состояния FSM
    await state.set_state(EmployerForm.name)

# Вопрос про имя и фамилию представителя компании (работодатель)
@router.message(EmployerForm.name)
async def process_name(msg: Message, state: FSMContext):
    await state.update_data(name=msg.text)
    # Продолжаем диалог
    await state.set_state(EmployerForm.company_type)
    await msg.answer("Каков тип вашей компании? Выберите вариант ниже:", reply_markup=company_type)


# В зависимости от ответа идем дальше к вопросу о информации компании
@router.message(EmployerForm.company_type)
async def process_company_type(msg: Message, state: FSMContext):
    await state.update_data(company_type=msg.text)
    
    if msg.text == "Индивидуальный предприниматель (ИП)":
        await EmployerForm.individual_info.set()
        await msg.answer("Введите ваш ИНН:")
        
    elif msg.text == "Физическое лицо":
        await EmployerForm.physical_info.set()
        await msg.answer("Введите ваше ФИО")
        
    elif msg.text == "Юридическое лицо (ООО, АО)":
        await EmployerForm.entity_info.set()
        await msg.answer("Введите название вашей компании, ОГРН, ИНН, КПП:")
    else:
        await msg.answer("Пожалуйста, выберите один из предложенных вариантов.", reply_markup=company_type)

#Обработка ИП
@router.message(EmployerForm.individual_info)
async def process_individual_info(msg: Message, state: FSMContext):
    await state.update_data(individual_info=msg.text)
    await msg.answer("Введите название вашей компании, ОГРН, ИНН, КПП:")

# Обработка Физического лица
@router.message(EmployerForm.physical_info)
async def process_physical_info(msg: Message, state: FSMContext):
    await state.update_data(physical_info=msg.text)
    await msg.answer("Введите название вашей компании, ОГРН, ИНН, КПП:")

# ШагОбработка Юридического лица
@router.message(EmployerForm.entity_info)
async def process_entity_info(msg: Message, state: FSMContext):
    await state.update_data(entity_info=msg.text)
    await msg.answer("Введите название вашей компании, ОГРН, ИНН, КПП:")





@router.message(EmployerForm.company_name)
async def process_companyname(msg: Message, state: FSMContext):
    await state.update_data(company_name=msg.text)
    await state.set_state(EmployerForm.type_business_activity)
    await msg.answer("""Юридическое или торговое название вашей компании. 
                    Если вы ИП или частное лицо, укажите имя и фамилию""", reply_markup=rmk)
