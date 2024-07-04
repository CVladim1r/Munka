from bot.keyboards.inline import *
from bot.keyboards.reply import *
from bot.config_reader import Settings

from aiogram import Router, F, Bot
from aiogram.client.default import DefaultBotProperties

bot = Bot(Settings().BOT_TOKEN.get_secret_value(), default=DefaultBotProperties(parse_mode='HTML'))

async def main_menu_employer(user_id, message_id):
    await bot.send_message(user_id, "Вот мы и в главном меню", reply_markup=rmk)
    main_text = "Активные вакансии\n"
    main_text += "Разместить вакансию\n"
    main_text += "Профиль компании\n"
    main_text += "Баланс\n"
    await bot.send_message(user_id, main_text, reply_markup=get_choose_menu_employer_buttons, disable_notification=True)
