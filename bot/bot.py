import asyncio
import logging
from aiogram import Bot, Dispatcher
from .config_reader import Settings
from bot import handlers

class BotDispatcher:
    bot = Bot(Settings.bot_token.get_secret_value(), parse_mode='HTML')
    dp = Dispatcher()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Бот запущен и работает...")

async def main():
    # Включаем отдельные роутеры
    BotDispatcher.dp.include_router(handlers.user_commands.router)
    BotDispatcher.dp.include_router(handlers.bot_messages.router)
    await BotDispatcher.dp.start_polling(BotDispatcher.bot)

if __name__ == "__main__":
    asyncio.run(main())
