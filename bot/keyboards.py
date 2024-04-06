from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def get_send_or_dislike_resume_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    keyboard.add(
        KeyboardButton("👎"),
        KeyboardButton("✉"),
        KeyboardButton("😴")
    )
    return keyboard

async def get_position_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Повар"))
    keyboard.add(KeyboardButton("Официант"))
    keyboard.add(KeyboardButton("Бариста"))
    keyboard.add(KeyboardButton("Другое"))
    return keyboard

async def get_citizenship_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=5)
    keyboard.add(KeyboardButton("РФ"))
    keyboard.add(KeyboardButton("Казахстан"))
    keyboard.add(KeyboardButton("Беларусь"))
    keyboard.add(KeyboardButton("Грузия"))
    return keyboard

async def get_yes_no_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Да"))
    keyboard.add(KeyboardButton("Нет"))
    return keyboard

async def get_save_restart_keyboard():
    Inlinekeyboard = InlineKeyboardMarkup()
    Inlinekeyboard.add(InlineKeyboardButton("Сохранить", callback_data="save_resume"))
    Inlinekeyboard.add(InlineKeyboardButton("Начать заново", callback_data="restart_resume"))
    return Inlinekeyboard

async def get_choose_rule():
    Inlinekeyboard = InlineKeyboardMarkup()
    Inlinekeyboard.add(InlineKeyboardButton("Соискатель", callback_data="job_seeker"))
    Inlinekeyboard.add(InlineKeyboardButton("Работодатель", callback_data="employer"))
    return Inlinekeyboard

async def get_choose_menu_user_buttons():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("🔍 Искать Вакансии"))
    keyboard.add(KeyboardButton("👤 Личный кабинет"))
    keyboard.add(KeyboardButton("✏️ Редактировать резюме"))
    keyboard.add(KeyboardButton("ℹ️ О боте"))
    return keyboard

async def get_choose_menu_employer_buttons():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("🔍 Опубликовать вакансию"))
    keyboard.add(KeyboardButton("👤 Информация о компании"))
    keyboard.add(KeyboardButton("ℹ️ О боте"))
    return keyboard

async def get_location_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.row(
        InlineKeyboardButton("Питер", callback_data="location_spb"),
        InlineKeyboardButton("Москва", callback_data="location_moscow"),
        InlineKeyboardButton("Сочи", callback_data="location_sochi")
    )
    return keyboard

async def get_resume_button():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Заполнить анкету заново"))
    keyboard.add(KeyboardButton("Изменить описание"))
    keyboard.add(KeyboardButton("🔍 Искать Вакансии"))
    keyboard.add(KeyboardButton("↩️ Назад"))
    return keyboard