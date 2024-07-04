import asyncio
import logging 

from aiogram.exceptions import TelegramBadRequest
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.client.default import DefaultBotProperties

from bot.keyboards.inline import *
from bot.keyboards.reply import *
from bot.database.methods import *
from bot.utils.states import *
from bot.handlers.bot_messages import *

logger = logging.getLogger(__name__)

bot = Bot(Settings().BOT_TOKEN.get_secret_value(), default=DefaultBotProperties(parse_mode='HTML'))
commands = Router()

welcome_message_id = None

@commands.message(CommandStart())
async def start_command(msg: Message, state: FSMContext):
    user_tgid = msg.from_user.id
    user_tgfullname = msg.from_user.full_name
    user_tgname = msg.from_user.username or str(user_tgid)
    user_language_code = msg.from_user.language_code

    await state.update_data(
        user_tgid=user_tgid,
        user_fullname=user_tgfullname,
        user_tgname=user_tgname,
        user_language_code=user_language_code
    )

    try:
        await bot.delete_message(msg.chat.id, msg.message_id)
    except Exception as e:
        logger.error(f"Failed to delete message: {e}")

    welcome_message = await msg.answer(
        'Привет! Команда Мунки рада приветствовать тебя :)',
        reply_markup=rmk
    )
    
    await state.set_state(StartMessage.welcome_message_id)
    await state.update_data(welcome_message_id=welcome_message.message_id)
    
    await msg.answer("Расскажи пожалуйста, кто ты?", reply_markup=await get_choose_rule())

@commands.callback_query(lambda c: c.data in ["user", "employer"])
async def process_user_type(callback_query: CallbackQuery, state: FSMContext):
    user_type = callback_query.data

    try:
        await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
        data = await state.get_data()
        welcome_message_id = data.get('welcome_message_id')
        if welcome_message_id:
            await bot.delete_message(callback_query.message.chat.id, welcome_message_id)
    except Exception as e:
        logger.error(f"Failed to delete message: {e}")

    if user_type == "user":
        await callback_query.message.answer("Отлично! Давай теперь создадим тебе резюме 😊", reply_markup=rmk)
        await callback_query.message.answer("Напиши свое ФИО\nНапример: Туровец Валерий Андреевич", reply_markup=rmk)

        await state.set_state(UserForm.fio)
        
    elif user_type == "employer":
        await callback_query.message.answer("Чтобы найти подходящего сотрудника, давай создадим профиль компании 😊", reply_markup=rmk)
        await callback_query.message.answer("Как к Вам обращаться?", reply_markup=rmk)
        
        await state.set_state(EmployerForm.name)

@commands.message(Command("help"))
async def help_command(msg: Message):
    help_text = "Список доступных команд:\n" \
                "/start - Начать диалог с ботом\n" \
                "/help - Получить список доступных команд\n" \
                "Личный кабинет - Просмотреть информацию о пользователе\n" \
                "Искать Вакансии - Поиск вакансий\n" \
                "Редактировать резюме - Изменить информацию о себе\n" \
                "О боте - Информация о боте\n"

    await msg.answer(help_text, reply_markup=None)


@commands.message(Command('about'))
async def about_command(msg: Message):
    user_id = msg.from_user.id
    user_data = await get_user_data(user_id)

    if user_data:
        ...
    else:
        await msg.answer('SuckMyDickBROOO', reply_markup=None)
