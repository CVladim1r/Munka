import logging
from aiogram import Bot, Dispatcher, types
from config import TOKEN
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
import asyncio
import sys
from os import getenv
from aiogram.utils.markdown import hbold


bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def command_start_handler(message: types.Message) -> None:
    await message.answer(f"Привет, {hbold(message.from_user.full_name)}!")

@dp.message_handler()
async def echo_handler(message: types.Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Попробуйте еще раз!")

async def main() -> None:
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())