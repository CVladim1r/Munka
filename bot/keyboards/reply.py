from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

rmk = ReplyKeyboardRemove()

get_send_or_dislike_resume_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="👎"),
            KeyboardButton(text="✉"),
            KeyboardButton(text="😴")
        ]
    ],
    resize_keyboard=True,
)

get_save_restart_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Сохранить"),
            KeyboardButton(text="Начать заново"),
            KeyboardButton(text="Изменить")
        ]
    ],
    resize_keyboard=True,
)

company_type = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="ИП"),
            KeyboardButton(text="Физическое лицо"),
            KeyboardButton(text="Юр лицо (ООО, АО)")
        ]
    ],
    resize_keyboard=True,
)

get_citizenship_r = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="РФ"),
            KeyboardButton(text="Другое")
        ]
    ],    
    resize_keyboard=True,
)

finReg = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="✅ Подтвердить")
        ]
    ]
)


get_location_r = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Питер"),
            KeyboardButton(text="Москва"),
        ],
        [
            KeyboardButton(text="Другое")
        ]
    ]
)

get_position_keyboard = ReplyKeyboardMarkup(
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

get_yes_no_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Да"),
            KeyboardButton(text="Нет")
        ]
    ],
    resize_keyboard=True
)

get_choose_menu_user_buttons = ReplyKeyboardMarkup(
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
    resize_keyboard=True
)

get_choose_menu_employer_buttons = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🔍 Опубликовать вакансию"),
            KeyboardButton(text="👤 Информация о компании")
        ],
        [
            KeyboardButton(text="ℹ️ О боте")
        ]
    ],
    resize_keyboard=True
)

get_resume_button = ReplyKeyboardMarkup(
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
    resize_keyboard=True
)