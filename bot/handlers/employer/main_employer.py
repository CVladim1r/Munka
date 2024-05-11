from bot.keyboards.inline import *
from bot.keyboards.reply import *
from bot.config_reader import config
from aiogram import Router, F, Bot

bot = Bot(config.bot_token.get_secret_value(), parse_mode='HTML')

async def main_menu_employer(user_id, message_id):
    await bot.send_message(user_id, "Вот мы и в главном меню", reply_markup=rmk)
    main_text = "Активные вакансии\n"
    main_text += "Разместить вакансию\n"
    main_text += "Профиль компании\n" # -> Редактировать профиль компании или оставить как есть
    main_text += "Баланс\n"
    await bot.send_message(user_id, main_text, reply_markup=get_choose_menu_employer_buttons, disable_notification=True)
