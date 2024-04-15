import asyncio
from aiogram import Bot, Dispatcher
from config_reader import config
from aiogram import Bot, Dispatcher
import logging
import handlers
import handlers.bot_messages


bot = Bot(config.bot_token.get_secret_value(), parse_mode='HTML')
dp = Dispatcher() 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Бот запущен и работает...")

async def main():  
    
    dp.include_routers(
        handlers.user_commands.router,
        handlers.bot_messages.router
    )
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())