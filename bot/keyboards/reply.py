from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

async def get_send_or_dislike_resume_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="👎"),
                KeyboardButton("✉"),
                KeyboardButton("😴")
            ]
        ],
        resize_keyboard=True,
    )
    return keyboard

async def get_position_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton("Повар"),
                KeyboardButton("Официант")
            ],
            [
                KeyboardButton("Бариста"),
                KeyboardButton("Другое")
            ]
        ],
        resize_keyboard=True
    )
    return keyboard

async def get_citizenship_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton("РФ"),
                KeyboardButton("Казахстан")
            ],
            [
                KeyboardButton("Беларусь"),
                KeyboardButton("Грузия")
            ]
        ],
        
        resize_keyboard=True)
    return keyboard

async def get_yes_no_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton("Да"),
                KeyboardButton("Нет")
            ]
        ],
        resize_keyboard=True)
    return keyboard

async def get_choose_menu_user_buttons():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton("🔍 Искать Вакансии"),
                KeyboardButton("👤 Личный кабинет")
            ],
            [
                KeyboardButton("✏️ Редактировать резюме"),
                KeyboardButton("ℹ️ О боте")
            ]
        ],
        
        resize_keyboard=True)
    return keyboard

async def get_choose_menu_employer_buttons():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton("🔍 Опубликовать вакансию"),
                KeyboardButton("👤 Информация о компании")
            ],
            [
                KeyboardButton("ℹ️ О боте")
            ]
        ],
        
        resize_keyboard=True)
    return keyboard

async def get_resume_button():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton("Заполнить анкету заново"),
                KeyboardButton("Изменить описание")
            ],
            [
                KeyboardButton("🔍 Искать Вакансии"),
                KeyboardButton("↩️ Назад")
            ]
        ],
        resize_keyboard=True)
    return keyboard