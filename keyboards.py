from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def get_position_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Повар"))
    keyboard.add(KeyboardButton("Официант"))
    keyboard.add(KeyboardButton("Бариста"))
    keyboard.add(KeyboardButton("Другое"))
    return keyboard

async def get_yes_no_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Да"))
    keyboard.add(KeyboardButton("Нет"))
    return keyboard

async def get_save_restart_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Сохранить", callback_data="save_resume"))
    keyboard.add(InlineKeyboardButton("Начать заново", callback_data="restart_resume"))
    return keyboard
