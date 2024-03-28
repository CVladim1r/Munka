import logging
import asyncio
import sys
from os import getenv

import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode
from aiogram.utils import executor
from config import TOKEN

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("Привет! Этот бот поможет тебе с eco-вопросами. Введите /help для получения справки.")

@dp.message_handler(commands=["help"])
async def help_command(message: types.Message):
    help_text = (
        "Этот бот поможет тебе с eco-вопросами.\n"
        "Доступные команды:\n"
        "/start - начать общение с ботом\n"
        "/help - получить справку"
    )
    await message.answer(help_text, parse_mode=ParseMode.MARKDOWN)

if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)