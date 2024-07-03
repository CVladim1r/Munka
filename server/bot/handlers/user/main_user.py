from bot.keyboards.inline import *
from bot.keyboards.reply import *
from bot.config_reader import config
from aiogram import Router, F, Bot

bot = Bot(config.bot_token.get_secret_value(), parse_mode='HTML')

async def main_menu_job_seeker(bot, user_id, message_id):
    await bot.send_message(user_id, "Вот мы и в главном меню. Куда отпарвимся сейчас?", reply_markup=rmk)
    main_text = "Искать вакансии\n"
    main_text += "Личный кабинет\n"
    main_text += "Редактировать резюме\n"
    main_text += "О боте\n"
    await bot.send_message(user_id, main_text, reply_markup=get_choose_menu_user_buttons, disable_notification=True)
