import asyncio

from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext

from bot.handlers.job_seeker.main_job_seeker import main_menu_user
from bot.handlers.employer.main_employer import main_menu_employer
from bot.handlers.admin.main_admin import main_menu_admin

from bot.keyboards.inline import *
from bot.keyboards.reply import *
from bot.database.methods import *
from bot.utils.states import *

from ..bot import BotDispatcher

router = Router()
bot = BotDispatcher.bot

'''
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

'''

# job FINDER
@router.message(CommandStart())
async def start(msg: Message, state: FSMContext):
    user_tgid = msg.from_user.id
    
    await state.set_state(UserForm.user_tgid)
    await state.update_data(user_tgid=user_tgid)

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


    await state.set_state(UserForm.user_fullname)
    user_tgfullname = msg.from_user.full_name
    await state.update_data(user_fullname=user_tgfullname)

    await state.set_state(UserForm.user_tgname)
    user_tgname = msg.from_user.username
    await state.update_data(user_tgname=user_tgname)

    await state.set_state(UserForm.user_language_code)
    user_language_code = msg.from_user.language_code
    await state.update_data(user_language_code=user_language_code)



    if not user_tgname:
        user_tgname = str(user_tgid)

    await bot.send_message(msg.chat.id, '''Привет я кот Миша.\nЯ выполняю здесь самую главную функцию: помогаю соискателям и работодателям найти друг друга. Представь, у каждого есть работа, а в мире царит гармония – мяу, красота.''', reply_markup=None)

    # Позже надо реализовать не через asyncio.sleep !
    await asyncio.sleep(4)
    await msg.answer("Давай теперь познакомимся поближе. Кто ты?", reply_markup=await get_choose_rule())



@router.callback_query(lambda c: c.data in ["job_seeker", "employer"])
async def process_user_type(callback_query: CallbackQuery, state: FSMContext):
    user_type = callback_query.data

    if user_type == "job_seeker":
        await callback_query.message.answer("Отлично, у нас как раз много интересных вакансий! Чтобы выбрать самые подходящие, давай создадим резюме 😊", reply_markup=None)
        await callback_query.message.answer("Напиши свое ФИО\nНапример: Достоевский Федор Михайлович", reply_markup=rmk)

        await state.set_state(UserForm.fio)
        
    elif user_type == "employer":
        await bot.send_message("Отлично! Давайте теперь заполним некоторые данные о вашей компании.", reply_markup=None)
        await callback_query.message.answer("Напиши свое ФИО\nНапример: Достоевский Федор Михайлович", reply_markup=rmk)
        
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
        await main_menu_user(msg.from_user.id, msg.message_id)
    else:
        await msg.answer('SuckMyDickBROOO', reply_markup=None)