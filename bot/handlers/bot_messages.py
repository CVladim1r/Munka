from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from keyboards.inline import *
from keyboards.reply import *
from database.db_connector import *
from format_data import *
from config_reader import config

router = Router()

bot = Bot(config.bot_token.get_secret_value(), parse_mode='HTML')

# Позже надо разбить регистрацию

async def main_menu_user(user_id, message_id):
    main_text = "Искать вакансии\n"
    main_text += "Личный кабинет\n"
    main_text += "Редактировать резюме\n"
    main_text += "О боте\n"
    await bot.send_message(user_id, main_text, reply_markup=await get_choose_menu_user_buttons(), disable_notification=True)

@router.message(F.text=='🔍 Искать Вакансии')
async def seacrh_vacancies(msg: Message):
    user_id = msg.from_user.id
    user_data = await get_user_data(user_id)
    
    if user_data:
        random_vacancy = await get_random_vacancy_for_user(user_id)
        
        if random_vacancy:
            formatted_vacancy = await formatted_vacancy(random_vacancy)
            await msg.answer(
                formatted_vacancy, 
                reply_markup= await get_send_or_dislike_resume_keyboard()
            )
        else:
            await msg.answer('К сожалению, не удалось найти вакансии. Попробуйте еще раз позже.',
                             reply_markup=None
                             )
    else: 
        await msg.answer(
            "Похоже что ты не зарегистрирован в системе. Самое время пройти регистраицю! /start",
            reply_markup=None
        )
        
@router.message(F.text=="👎")
async def dislike_resume(msg: Message):
    user_id = msg.from_user.id
    user_data = await get_user_data(user_id)

    if user_data:
        random_vacancy = await get_random_vacancy_for_user(user_id)

        if random_vacancy:
            formatted_vacancy = await format_vacancy(random_vacancy)
            await msg.answer(
                formatted_vacancy,
                parse_mode="HTML",
                reply_markup=await get_send_or_dislike_resume_keyboard()
            )
        else:
            await msg.answer(
                "К сожалению, не удалось найти вакансии. Попробуйте еще раз позже.",
                reply_markup=None
            )

@router.message(F.text=="✉")
async def send_resume(msg: Message):
    user_id = msg.from_user.id
    user_data = await get_user_data(user_id)

    if user_data:
        await msg.answer("Резюме отправлено!\n\nТеперь можно перейти к просмотру анкет дальше!")
        await seacrh_vacancies(msg)

@router.message(F.text == '😴')
async def personal_sleep(msg: Message):
    await msg.answer("Отлично! Самое время сделать перерв 😁", reply_markup=await get_choose_menu_user_buttons())
    

@router.message(F.text == '👤 Личный кабинет')
async def personal_cabinet(msg: Message):
    user_id = msg.from_user.id

    user_data = await get_user_data(user_id)
    print("User data:", user_data)  # Отладочное сообщение для проверки данных о пользователе

    if user_data:
        fullname = user_data.get("user_fullname", "Не указано")
        age = user_data.get("user_age", "Не указан")
        location = user_data.get("user_location", "Не указано")
        skills = user_data.get("user_skills", "Не указано")
        experience = user_data.get("user_experience", [])

        if experience:
            experience_text = ""
            for exp in experience:
                if isinstance(exp, dict):
                    company_name = exp.get("company_name", "Не указано")
                    exp_description = exp.get("description", "Не указано")
                    experience_text += f"Место работы: {company_name}\nОписание: {exp_description}\n\n"
                else:
                    experience_text = "Нет данных об опыте работы"
        else:
            experience_text = "Нет данных об опыте работы"

        user_info_text = f"ФИО: {fullname}\nВозраст: {age}\nМестоположение: {location}\nОсобенные навыки: {skills}\n\nОпыт работы:\n{experience_text}"

        await msg.answer(f'Вот так будет выглядеть твоя анкета для работодателя:\n\n{user_info_text}', reply_markup=await get_resume_button())
    else:
        await msg.answer("Информация о пользователе не найдена.", reply_markup=None)


@router.message(F.text== '↩️ Назад')
async def back_to_main_menu(msg: Message):
    user_id = msg.from_user.id
    user_data = await get_user_data(user_id)
    if user_data:
        name = user_data.get("name")
        await main_menu_user(user_id, name)
    else:
        await msg.answer("Информация о пользователе не найдена. Пройдите регистрацию нажав на команду /start", reply_markup=None)


@router.message(F.text=='ℹ️ О боте')
async def about_bot(msg: Message):
    about_text = "Данный бот был создан для помощи компаниям в сфере общепита быстрее найти работников."
    await msg.answer(about_text)
    
@router.message(F.text=='✏️ Редактировать резюме')
async def red_resume(msg: Message):
    await msg.answer("Желаете что-нибудь подправить или начать заново?", reply_markup=await get_save_restart_keyboard())