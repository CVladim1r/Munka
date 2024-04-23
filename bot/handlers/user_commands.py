from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
import asyncio

from aiogram.fsm.storage.base import (
    BaseEventIsolation,
    BaseStorage,
    StateType,
    StorageKey,
)

from aiogram.fsm.state import StatesGroup, State

from aiogram.fsm.context import FSMContext


from .user_registration import *

from bot.cities import CITIES

from bot.utils import format_vacancy

from bot.config_reader import config
from bot.keyboards.inline import *
from bot.keyboards.reply import *
from bot.utils.states import *

from bot.database.methods import *

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
        await callback_query.message.answer("Отлично, у нас как раз много интересных вакансий! Чтобы выбрать самые подходящие, давай создадим резюме 😊", reply_markup=None)
        await callback_query.message.answer("Напиши свое ФИО\nНапример: Достоевский Федор Михайлович", reply_markup=rmk)

        await state.set_state(UserForm.fio)
        #await state.set_state(UserForm.age)

    elif user_type == "employer":
        await register_employer(callback_query.message, user_tgid, user_fullname, user_tgname)



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