import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode
from aiogram.utils import executor
from config import TOKEN, DB_CONFIG
from models.user import User
from database.db_connector import Database

async def main():
    # Создание бота, хранилища и диспетчера
    bot = Bot(token=TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)

    # Получение текущего асинхронного цикла событий
    loop = asyncio.get_event_loop()

    # Подключение к базе данных
    db = Database(loop=loop, **DB_CONFIG)
    await db.connect()

    # Обработчик команды /start
    @dp.message_handler(commands=["start"])
    async def start(message: types.Message):
        await message.answer("Привет! Этот бот поможет тебе с eco-вопросами. Введите /help для получения справки.")
        
        # Создание нового пользователя и сохранение его в базе данных
        new_user = User(user_type='USER', user_name=message.from_user.username)
        await new_user.save()

    # Обработчик команды /help
    @dp.message_handler(commands=["help"])
    async def help_command(message: types.Message):
        help_text = (
            "Этот бот поможет тебе с eco-вопросами.\n"
            "Доступные команды:\n"
            "/start - начать общение с ботом\n"
            "/help - получить справку"
        )
        await message.answer(help_text, parse_mode=ParseMode.MARKDOWN)

    # Запуск бота
    await executor.start_polling(dp, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
