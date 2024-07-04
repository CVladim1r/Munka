from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def get_save_restart_keyboard():
    Inlinekeyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Сохранить", callback_data="save_resume"),
                InlineKeyboardButton(text="Начать заново", callback_data="restart_resume"),
                InlineKeyboardButton(text="Изменить", callback_data="edit_resume")
            ]
        ]
    )
    return Inlinekeyboard

async def get_skip_button():
    Inlinekeyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Пропустить", callback_data="skip"),
            ]
        ]
    )
    return Inlinekeyboard

async def get_choose_rule():
    Inlinekeyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Соискатель", callback_data="user"),
                InlineKeyboardButton(text="Работодатель", callback_data="employer")
            ]
        ]
    )
    return Inlinekeyboard

async def get_change_age():
    Inlinekeyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Изменить", callback_data="change_age"),
                InlineKeyboardButton(text="Оставить", callback_data="im_little")
            ]
        ]
    )
    return Inlinekeyboard

async def get_location_keyboard():
    Inlinekeyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Питер", callback_data="spb"),
                InlineKeyboardButton(text="Москва", callback_data="msk")
            ],
            [
                InlineKeyboardButton(text="Другое", callback_data="other_location")
            ]
        ]
    )
    return Inlinekeyboard

async def get_citizenship_keyboard():
    Inlinekeyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="РФ", callback_data="citizen_Russian_Federation"),
                InlineKeyboardButton(text="Другое", callback_data="other_citizen")
            ]
        ]
    )
    return Inlinekeyboard

async def get_employment_keyboard():
    Inlinekeyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Полная", callback_data="full_employment"),
                InlineKeyboardButton(text="Частичная", callback_data="part-time_employment")
            ]
        ]
    )
    return Inlinekeyboard

# async def get_location_keyboard():
#     keyboard = InlineKeyboardMarkup(
#         inline_keyboard=[
#             [
#                 InlineKeyboardButton(text="Питер", callback_data="location_spb"),
#                 InlineKeyboardButton(text="Москва", callback_data="location_moscow")
#             ],
#             [
#                 InlineKeyboardButton(text="Сочи", callback_data="location_sochi")
#             ]
#         ]
#     )
#     return keyboard