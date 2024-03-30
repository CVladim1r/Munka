from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from database.db_connector import add_user_info_to_db
from main import dp
from aiogram import executor
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
class JobSeekerForm(StatesGroup):
    name = State()
    age = State()
    description = State()

async def job_seeker_process_name(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer("Напишите ваш возраст:")
    await JobSeekerForm.next()

@dp.message_handler(state=JobSeekerForm.name)
async def process_name(message: Message, state: FSMContext):
    await job_seeker_process_name(message, state)

async def job_seeker_process_age(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['age'] = message.text
    await message.answer("Напишите краткую информацию о себе:")
    await JobSeekerForm.next()

@dp.message_handler(state=JobSeekerForm.age)
async def process_age(message: Message, state: FSMContext):
    await job_seeker_process_age(message, state)

async def job_seeker_process_description(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
        user_id = message.from_user.id
        await add_user_info_to_db(user_id, data['name'], data['age'], data['description'])
    await message.answer("Спасибо за регистрацию.")

@dp.message_handler(state=JobSeekerForm.description)
async def process_description(message: Message, state: FSMContext):
    await job_seeker_process_description(message, state)
