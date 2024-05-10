import asyncio
import logging
from aiogram import Bot, Dispatcher
from .config_reader import config
from bot import handlers

bot = Bot(config.bot_token.get_secret_value(), parse_mode='HTML')
dp = Dispatcher() 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Бот запущен и работает...")

async def main():  
    # Включаем отдельные роутеры
    dp.include_router(handlers.user_commands.router)
    dp.include_router(handlers.bot_messages.router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())