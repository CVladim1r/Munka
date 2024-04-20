import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import executor

from random import uniform
from config import TOKEN_PLUG

from bot.database.db_connector import add_user_to_db_plug_bot

logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()

logger = logging.getLogger('bot')
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

bot = Bot(token=TOKEN_PLUG)
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware(logger=logger)) 

class CommandState(StatesGroup):
    COMMAND_PROCESSING = State()

async def send_with_interval(message: types.Message, text: str):
    delay = uniform(2, 3)
    for line in text.split('\n\n'):
        if line.strip():
            await asyncio.sleep(delay)
            await message.answer(line)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message, state: FSMContext):
    await CommandState.COMMAND_PROCESSING.set()
    await message.answer("Привет! Спасибо, что перешел по ссылке, мы рады каждому ❤️")

    await send_with_interval(
        message,
        "Данный бот пока находится на этапе разработки, но буквально через считанные дни, ты сможешь воспользоваться его функциями!"
    )
    await asyncio.sleep(1)
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text="Что будет уметь бот?", callback_data="bot_capabilities")
    markup.add(button)
    await message.answer(
        "Мы обязательно оповестим тебя, когда бот полностью заработает, отправив сообщение. ☺️",
        reply_markup=markup
    )

    await add_user_to_db_plug_bot(message, message.from_user.id, message.from_user.username, message.from_user.full_name)
    await state.finish()

@dp.callback_query_handler(lambda query: query.data == 'bot_capabilities')
async def handle_bot_capabilities(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await send_description_info(callback_query.message, None)

@dp.message_handler(lambda message: message.text == "Что будет уметь бот?" or message.text == "?")
async def handle_info_button(message: types.Message, state: FSMContext):
    await send_description_info(message, state)

@dp.message_handler(commands=['donate'])
async def send_description_info(message: types.Message, state: FSMContext):
    await CommandState.COMMAND_PROCESSING.set()
    await send_with_interval(
        message,
        "Если хочешь поддержать проект финансово, то мы принимаем донаты через sber/tinkoff. Вы можете отправить пожертвование по номеру: tel:+79955934612\n\n",
    )
    if state:
        await state.finish()

@dp.message_handler(commands=['info'])
async def send_description_info(message: types.Message, state: FSMContext):
    await CommandState.COMMAND_PROCESSING.set()
    await message.answer("В этом боте, сойдутся две стороны, которые постоянно ищут друг друга: соискатель и работодатель.\n \nСоискатель - сможет составить резюме и смотреть вакансии от работодателей.\n \nРаботодатель - сможет размещать вакансии, а так же просматривать резюме от соискателей.")
    await send_with_interval(
        message,
        "Просматривая резюме или вакансии, ты сможешь отмечать 👍 понравившиеся тебе и 👎 если тебе что-то не понравилось.\n\n"
        "А теперь, осталось ждать, когда произойдет тот самый ⚡️мэтч⚡️\n\n"
        "(Если хочешь оказать материальную помощь проекту, чтоб он заработал быстрее, то напишите нашему менеджеру (ссылка в профиле), либо используйте команду /donate)",
    )
    if state:
        await state.finish()

@dp.message_handler()
async def handle_unknown_message(message: types.Message):
    await message.answer("Извини, я тебя не понял.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
