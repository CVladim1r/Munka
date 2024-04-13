from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
#
async def get_save_restart_keyboard():
    Inlinekeyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("Сохранить", callback_data="save_resume"),
                InlineKeyboardButton("Начать заново", callback_data="restart_resume")
            ]
        ]
    )
    return Inlinekeyboard

async def get_choose_rule():
    Inlinekeyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("Соискатель", callback_data="job_seeker"),
                InlineKeyboardButton("Работодатель", callback_data="employer")
            ]
        ]
    )
    return Inlinekeyboard

async def get_location_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("Питер", callback_data="location_spb"),
                InlineKeyboardButton("Москва", callback_data="location_moscow")
            ],
            [
                InlineKeyboardButton("Сочи", callback_data="location_sochi")
            ]
        ]
    )
    return keyboard