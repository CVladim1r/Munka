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

async def get_resume_button():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Заполнить анкету заново"))
    keyboard.add(KeyboardButton("Изменить описание"))
    keyboard.add(KeyboardButton("🔍 Искать Вакансии"))
    keyboard.add(KeyboardButton("↩️ Назад"))
    return keyboard
