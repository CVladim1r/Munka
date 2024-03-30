from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from database.db_connector import add_user_info_to_db

class EmployerForm(StatesGroup):
    company_name = State()

async def register_employer(message: Message, user_id: int, user_username: str, user_name: str):
    await message.answer("Давайте создадим профиль вашей компании:")
    await EmployerForm.company_name.set()

async def process_company_name(message: Message, state: FSMContext):
    company_name = message.text
    user_id = message.from_user.id
    await add_user_info_to_db(user_id, company_name=company_name)
    await message.answer("Спасибо за регистрацию.")

