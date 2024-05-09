from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

rmk = ReplyKeyboardRemove()

async def get_send_or_dislike_resume_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="👎"),
                KeyboardButton(text="✉"),
                KeyboardButton(text="😴")
            ]
        ],
        resize_keyboard=True,
    )
    return keyboard

finReg = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="✅ Подтвердить")
        ]
    ]
)
'''
async def get_location_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Питер"),
                KeyboardButton(text="Москва")
            ],
            [
                KeyboardButton(text="Сочи")
            ]
        ]
    )
    return keyboard
'''
async def get_position_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Официант"),
                KeyboardButton(text="Бариста")
            ],
            [
                KeyboardButton(text="Бармен"),
                KeyboardButton(text="Администратор")
            ],
            [
                KeyboardButton(text="Повар"),
            ]
        ],
        resize_keyboard=True
    )
    return keyboard
'''
async def get_citizenship_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="РФ"),
                KeyboardButton(text="Казахстан")
            ],
            [
                KeyboardButton(text="Беларусь"),
                KeyboardButton(text="Грузия")
            ]
        ],
        
        resize_keyboard=True)
    return keyboard
'''
async def get_yes_no_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Да"),
                KeyboardButton(text="Нет")
            ]
        ],
        resize_keyboard=True)
    return keyboard

async def get_choose_menu_user_buttons():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🔍 Искать Вакансии"),
                KeyboardButton(text="👤 Личный кабинет")
            ],
            [
                KeyboardButton(text="✏️ Редактировать резюме"),
                KeyboardButton(text="ℹ️ О боте")
            ]
        ],
        resize_keyboard=True)
    return keyboard

async def get_choose_menu_employer_buttons():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🔍 Опубликовать вакансию"),
                KeyboardButton(text="👤 Информация о компании")
            ],
            [
                KeyboardButton(text="ℹ️ О боте")
            ]
        ],
        resize_keyboard=True)
    return keyboard

async def get_resume_button():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Заполнить анкету заново"),
                KeyboardButton(text="Изменить описание")
            ],
            [
                KeyboardButton(text="🔍 Искать Вакансии"),
                KeyboardButton(text="↩️ Назад")
            ]
        ],
        resize_keyboard=True)
    return keyboard