import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from .config_reader import Settings
from bot.handlers import user_commands, bot_messages

bot = Bot(Settings().BOT_TOKEN.get_secret_value(), default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Bot start.")

async def main():  
    dp.include_router(user_commands.commands)
    dp.include_router(bot_messages.router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
