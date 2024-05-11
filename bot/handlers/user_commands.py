import asyncio

from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext

from bot.keyboards.inline import *
from bot.keyboards.reply import *
from bot.database.methods import *
from bot.utils.states import *

from bot.handlers.bot_messages import *


router = Router()
bot = Bot(config.bot_token.get_secret_value(), parse_mode='HTML')


# /start
@router.message(CommandStart())
async def start(msg: Message, state: FSMContext):
    user_tgid = msg.from_user.id
    ReplyKeyboardRemove()
    
    await state.set_state(UserForm.user_tgid)
    await state.update_data(user_tgid=user_tgid)
    '''
    employer_data = await get_employer_data(user_tgid)
    user_data = await get_user_data(user_tgid)
    admin_data = await get_admin_data(user_tgid)


    if employer_data:
        await main_menu_employer(user_tgid, msg.chat.id)
        return
    
    elif user_data:
        await main_menu_user(user_tgid, msg.chat.id)
        return
    
    elif admin_data:
        await main_menu_admin(user_tgid, msg.chat.id)
        return
    '''

    await state.set_state(UserForm.user_fullname)
    user_tgfullname = msg.from_user.full_name
    await state.update_data(user_fullname=user_tgfullname)

    await state.set_state(UserForm.user_tgname)
    user_tgname = msg.from_user.username
    await state.update_data(user_tgname=user_tgname)

    await state.set_state(UserForm.user_language_code)
    user_language_code = msg.from_user.language_code
    await state.update_data(user_language_code=user_language_code)

    # Если нет username в tg, то используем id
    if not user_tgname:
        user_tgname = str(user_tgid)

    await bot.send_message(msg.chat.id, '''Привет! Я готов тебе помочь найти работу или сотрудников.''', reply_markup=rmk)

    # Позже надо реализовать не через asyncio.sleep !
    await asyncio.sleep(1)
    await msg.answer("Давай теперь познакомимся поближе. Кто ты?", reply_markup=await get_choose_rule())


@router.callback_query(lambda c: c.data in ["job_seeker", "employer"])
async def process_user_type(callback_query: CallbackQuery, state: FSMContext):
    user_type = callback_query.data
    await callback_query.message.delete()

    if user_type == "job_seeker":
        await callback_query.message.answer("Отлично, у нас как раз много интересных вакансий! Чтобы выбрать самые подходящие, давай создадим резюме 😊", reply_markup=rmk)
        await asyncio.sleep(2)
        await callback_query.message.answer("Напиши свое ФИО\nНапример: Достоевский Федор Михайлович", reply_markup=rmk)

        await state.set_state(UserForm.fio)
        
    elif user_type == "employer":
        await callback_query.message.answer("Отлично, у нас как раз много сотрудников! Чтобы найти подходящего, давай создадим профиль компании 😊", reply_markup=rmk)
        await asyncio.sleep(2)
        await callback_query.message.answer("Как к Вам обращаться?", reply_markup=rmk)
        
        await state.set_state(EmployerForm.name)


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
        #await main_menu_user(msg.from_user.id, msg.message_id)
        ...
    else:
        await msg.answer('SuckMyDickBROOO', reply_markup=None)