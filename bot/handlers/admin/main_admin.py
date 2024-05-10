from aiogram import Dispatcher
from ...bot import BotDispatcher

bot = BotDispatcher.bot

# Админ панель в боте

async def main_menu_admin(user_id, message_id):
    main_text = "Статус сервера\n"
    main_text += "Кол-во пользователей\n"
    main_text += "Активностьn" # -> Редактировать профиль компании или оставить как есть
    main_text += "Логи\n"
