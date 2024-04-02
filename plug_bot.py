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

from database.db_connector import add_user_to_db_plug_bot

logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()

logger = logging.getLogger('bot')
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('bot.log')
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

bot = Bot(token=TOKEN_PLUG)
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware(logger=logger)) 

class CommandState(StatesGroup):
    COMMAND_PROCESSING = State()

async def send_with_interval(message: types.Message, text: str):
    delay = uniform(0,1)
    for line in text.split('\n\n'):
        if line.strip():
            await asyncio.sleep(delay)
            await message.answer(line)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message, state: FSMContext):
    await CommandState.COMMAND_PROCESSING.set()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton(text="Что будет уметь бот?")
    markup.add(button)
    
    await send_with_interval(
        message,
        "Пивет! Давай я расскажу тебе об отом боте:\n\n"
        "В этом боте, сойдутся две стороны, которые постоянно ищут друг друга: соискатель и работодатель.\n \nСоискатель - сможет составить резюме и смотреть вакансии от работодателей.\n \nРаботодатель - сможет размещать вакансии, а так же просматривать резюме от соискателей. \n\n"
        "Просматривая резюме или вакансии, ты сможешь отмечать 👍 понравившиеся тебе и 👎 если тебе что-то не понравилось.\n\n"
        "А теперь, осталось ждать, когда произойдет тот самый ⚡️мэтч⚡️\n\n"
        "(Если хочешь оказать материальную помощь проекту, чтоб он заработал быстрее, то напишите нашему менеджеру (ссылка в профиле), либо используйте команду /donate)",
    )
    await add_user_to_db_plug_bot(message, message.from_user.id, message.from_user.username, message.from_user.full_name)
    await state.finish()

@dp.message_handler(Text(equals="Что будет уметь бот?"))
async def send_description(message: types.Message, state: FSMContext):
    await CommandState.COMMAND_PROCESSING.set()
    await send_with_interval(
        message,
        "Здесь ты в скором времени сможешь найти или разместить работу в общепите! Офицант, повар, кондитер, менеджер и другие вакансии скоро будут ждать тебя!\n\n",
    )
    await state.finish()



@dp.message_handler(commands=['donate'])
async def send_description_info(message: types.Message, state: FSMContext):
    await CommandState.COMMAND_PROCESSING.set()
    await send_with_interval(
        message,
        "Если хочешь поддержать проект финансово, то мы принимаем донаты через sber/tinkoff. Вы можете отправить пожертвование по номеру: tel:+79955934612\n\n",
    )
    await state.finish()

@dp.message_handler(commands=['info'])
async def send_description_info(message: types.Message, state: FSMContext):
    await CommandState.COMMAND_PROCESSING.set()
    await send_with_interval(
        message,
        "Здесь ты в скором времени сможешь найти работу в общепите! Офицант, повар, кондитер, менеджер и другие вакансии скоро будут ждать тебя!\n\n",
    )
    await state.finish()

@dp.message_handler()
async def handle_unknown_message(message: types.Message):
    await message.answer("Извини, я тебя не понял.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
