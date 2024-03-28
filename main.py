# main.py

import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from config import TOKEN
from aiogram.dispatcher.storage import MemoryStorage

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Hello! I am a simple bot. To get started, just type something to me.")


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(f"You wrote: {message.text}")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)