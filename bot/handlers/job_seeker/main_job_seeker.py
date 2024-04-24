from aiogram import Router, F, Bot

from bot.keyboards.inline import *
from bot.keyboards.reply import *
from bot.config_reader import config


bot = Bot(config.bot_token.get_secret_value(), parse_mode='HTML')

async def main_menu_user(user_id, message_id):
    main_text = "Искать вакансии\n"
    main_text += "Личный кабинет\n"
    main_text += "Редактировать резюме\n"
    main_text += "О боте\n"
    await bot.send_message(user_id, main_text, reply_markup=await get_choose_menu_user_buttons(), disable_notification=True)
