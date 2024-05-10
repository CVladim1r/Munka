from aiogram import Dispatcher
from aiogram import Router, F, Bot
from bot.config_reader import config
from bot.keyboards import *

router = Router()
bot = Bot(config.bot_token.get_secret_value(), parse_mode='HTML')

# Админ панель в боте

async def main_menu_admin(user_id, message_id):
    main_text = "Статус сервера\n"
    main_text += "Кол-во пользователей\n"
    main_text += "Активностьn" # -> Редактировать профиль компании или оставить как есть
    main_text += "Логи\n"
    await bot.send_message(user_id, main_text, reply_markup=None, disable_notification=True)
