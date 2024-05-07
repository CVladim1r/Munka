from aiogram import Router, F, Bot

from bot.keyboards.inline import *
from bot.keyboards.reply import *
from bot.config_reader import config


bot = Bot(config.bot_token.get_secret_value(), parse_mode='HTML')

async def main_menu_employer(user_id, message_id):
    main_text = "Активные вакансии\n"
    main_text += "Разместить вакансию\n"
    main_text += "Профиль компании\n" # -> Редактировать профиль компании или оставить как есть
    main_text += "Баланс\n"
    await bot.send_message(user_id, main_text, reply_markup=await get_choose_menu_employer_buttons(), disable_notification=True)
