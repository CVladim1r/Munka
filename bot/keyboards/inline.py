from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def get_save_restart_keyboard():
    Inlinekeyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Сохранить", callback_data="save_resume"),
                InlineKeyboardButton(text="Начать заново", callback_data="restart_resume")
            ]
        ]
    )
    return Inlinekeyboard

async def get_choose_rule():
    Inlinekeyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Соискатель", callback_data="job_seeker"),
                InlineKeyboardButton(text="Работодатель", callback_data="employer")
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