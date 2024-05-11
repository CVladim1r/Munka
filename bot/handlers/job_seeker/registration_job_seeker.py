import json
import os
import traceback
import json

from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import Router, F, Bot, types

from bot.utils import normalize_city
from .main_job_seeker import main_menu_job_seeker

from bot.keyboards import *
from bot.utils.states import *
from bot.database.methods import *
from bot.handlers.bot_messages import *

async def register_job_seeker(user_tgid, user_tgname, user_fullname, state: FSMContext):
    """
    Регистрация соискателя.
    :param user_tgid: Telegram ID пользователя
    :param user_tgname: Telegram username пользователя
    :param user_fullname: Полное имя пользователя
    """
    # Здесь код для регистрации соискателя в базе данных:
    # await db.save_user(user_tgid, user_tgname, user_fullname, user_type="JOB_SEEKER")

    # Вместо прямого вызова функций proc_age и process_location будем устанавливать состояния FSM
    await state.set_state(UserForm.fio)


# Вопрос про ФИО для соискателя
@router.message(UserForm.fio)
async def process_fio(msg: Message, state: FSMContext):
    await state.update_data(fio=msg.text)
    # Продолжаем диалог
    await state.set_state(UserForm.age)
    await msg.answer("Сколько тебе полных лет?\nНапример: 21", reply_markup=None)


# Вопрос про возраст для соискателя
@router.message(UserForm.age)
async def process_age(msg: Message, state: FSMContext):
    if int(msg.text) >= 14:
        if not msg.text.isdigit() or not (0 < int(msg.text) < 99):
            await msg.answer("Неверный формат возраста. Пожалуйста, введите возраст цифрами. Пример: 18", reply_markup=rmk)
            return
    elif msg.text == "писят два":
        await msg.answer("Отсылочка )))\nЛадно, давай повторим..", reply_markup=rmk)
        await state.set_state(UserForm.age)

        await msg.answer("Сколько тебе полных лет?\nНапример: 21", reply_markup=rmk)
        return
    else:
        await msg.answer('''К сожалению, в России можно работать только с 14 лет.
Но время летит быстро!
Мы будем тебя ждать ❤️''', reply_markup=rmk)
        await msg.answer("Но если ты просто ошибся с возрастом, то ты можешь его изменить", reply_markup=await get_change_age())
        return
    
    await state.update_data(age=msg.text)
    await msg.answer("В каком городе планируешь работать?", reply_markup=get_location_r)
    await state.set_state(UserForm.location)


# Если вдруг пользователь ошибся
@router.callback_query(lambda c: c.data == 'change_age')
async def change_age(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer("Давайте попробуем еще раз")
    await callback_query.message.answer("Сколько тебе полных лет?\nНапример: 21", reply_markup=rmk)
    await state.set_state(UserForm.age)

@router.message(UserForm.location)
async def process_location_msk_spb(msg: Message, state: FSMContext):
    location_text = msg.text.strip()

    if location_text.lower().startswith('другое'):
        await state.set_state(UserForm.location_retry)
        await msg.answer('Напиши свой город. Например: Сочи')
        return

    normalized_location = await normalize_city(location_text)

    if normalized_location is None:
        await msg.answer("К сожалению, мы не можем разобрать, что это за город. Пожалуйста, введи его снова.")
        return

    data = await state.get_data()
    data['location_text'] = location_text
    data['location'] = normalized_location
    await state.update_data(location=location_text)

    await state.set_state(UserForm.citizenship)  # Переход к следующему шагу
    await msg.answer("Ты гражданин какой страны?", reply_markup=get_citizenship_r)

@router.message(UserForm.location_retry)
async def process_location_retry(msg: Message, state: FSMContext):
    if 'location' not in await state.get_data():
        location_text = msg.text.strip()

        if location_text:  # Проверяем, что текст не пустой
            normalized_location = await normalize_city(location_text)

            if normalized_location is None:
                await msg.answer("К сожалению, мы не можем разобрать, что это за город. Пожалуйста, введи его снова.")
                return

            data = await state.get_data()
            data['location_text'] = location_text
            data['location'] = normalized_location
            await state.update_data(location=location_text)

            await state.set_state(UserForm.desired_position)  # Переход к следующему шагу
            await msg.answer("Выбери желаемую должность:", reply_markup=get_position_keyboard)
        else:
            await msg.answer("Вы не ввели название города. Пожалуйста, введите город еще раз.")
    else:
        await state.set_state(UserForm.desired_position)
        await msg.answer("Выбери желаемую должность:", reply_markup=get_position_keyboard)


# Предпочтиаемая зарплата
@router.message(UserForm.desired_position)
async def process_desired_position(msg: Message, state: FSMContext):
    await state.update_data(desired_position=msg.text)
    await state.set_state(UserForm.desired_salary_level)
    await msg.answer("Какую зарплату ты бы хотел получать?\nНапример: 50 000", reply_markup=rmk)


# Занятость соискателя (Полная или частичная)
@router.message(UserForm.desired_salary_level)
async def process_desired_salary_level(msg: Message, state: FSMContext):
    await state.update_data(desired_salary_level=msg.text)
    await msg.answer("Какая занятость тебя интересует?", reply_markup=await get_employment_keyboard())


# Выбор и отправка занятости , а так же вопрос опыте работы
@router.callback_query(lambda c: c.data == 'full_employment' or c.data == 'part-time_employment')
async def process_desired_positionv1(callback_query: CallbackQuery, state: FSMContext):
    message = callback_query.message
    if callback_query.data == 'full_employment':
        new_employment_type = 'Полная занятость'
    elif callback_query.data == 'part-time_employment':
        new_employment_type = 'Частичная занятость'
    else:
        return

    await state.update_data(employment_type=new_employment_type)
    await state.set_state(UserForm.work_experience)
    await message.answer("Был ли у тебя опыт работы?", reply_markup=get_yes_no_keyboard)


# proc_experience, распрашиваем про опыт если есть, либо скпиаем если нет :(
@router.message(UserForm.work_experience)
async def proc_experience(msg: Message, state: FSMContext):
    if msg.text.lower() == 'да':
        await state.set_state(UserForm.work_company_name)
        await msg.answer("Отлично! Расскажите о своем опыте работы. Напишите название предыдущего места работы.", reply_markup=rmk)
    elif msg.text.lower() == 'нет':
        await state.update_data(work_experience="Нет опыта работы")
        await state.set_state(UserForm.additional_info)
        await msg.answer("У тебя есть навыки, с которыми то хотел бы поделиться?", reply_markup=rmk)
    else:
        await msg.answer("Пожалуйста, ответьте 'да' или 'нет'.", reply_markup=rmk)


# Сохраняем данные о названии Компании и задаем вопрос про период работы
@router.message(UserForm.work_company_name)
async def process_experience_details(msg: Message, state: FSMContext):
    await state.update_data(work_company_name=msg.text)
    await state.set_state(UserForm.work_experience_period)
    await msg.answer("Введите период работы в формате: 11.2020-09.2022", reply_markup=rmk)


# Сохраняем данные о периоде работы и задаем вопрос про должность
@router.message(UserForm.work_experience_period)
async def process_experience_period(msg: Message, state: FSMContext):
    await state.update_data(work_experience_period=msg.text)
    await state.set_state(UserForm.work_experience_position)
    await msg.answer("Какую должность ты занимал?", reply_markup=rmk)


# Сохраняем данные о должности и задаем вопрос про опыт в опыте?? Вот это игра слов, вот это я молодец )))
@router.message(UserForm.work_experience_position)
async def process_experience_position(msg: Message, state: FSMContext):
    await state.update_data(work_experience_position=msg.text)
    await state.set_state(UserForm.work_experience_duties)
    await msg.answer("Расскажи, какие у тебя были обязанности на этой работе? Старайся отвечать на этот вопрос максимально кратко и лаконично, при этом не упуская главной сути", reply_markup=rmk)
    await msg.answer("Например: Я варил для моих посетителей – котиков, самое лучшее молоко, с пенкой. А в конце смены, я подметал полы от следов лапок, и вел учет, сколько кошачьей мяты поступило в кассу, а сколько было потрачено", reply_markup=rmk)


# Сохраняем данные о должности и задаем вопрос про опыт в опыте?? Вот это игра слов, вот это я молодец )))
@router.message(UserForm.work_experience_duties)
async def process_experience_duties(msg: Message, state: FSMContext):
    await state.update_data(work_experience_duties=msg.text)
    await state.set_state(UserForm.work_experience_another)
    await msg.answer("Был ли у вас другой опыт работы?", reply_markup=get_yes_no_keyboard)


# process_experience_another
@router.message(UserForm.work_experience_another)
async def process_experience_another(msg: Message, state: FSMContext):
    if msg.text.lower() == 'да':
        await state.set_state(UserForm.work_company_name)
        await msg.answer("Отлично! Напишите название предыдущего места работы.", reply_markup=rmk)
        
    elif msg.text.lower() == 'нет':
        data = await state.get_data()
        new_data = {
            "work_company_name": data.get("work_company_name"),
            "work_experience_period": data.get("work_experience_period"),
            "work_experience_position": data.get("work_experience_position"),
            "work_experience_duties": data.get("work_experience_duties")
        }
        await state.update_data(work_experience_data=new_data)
        await state.set_state(UserForm.additional_info)
        
        await msg.answer("Все круги ада пройдены! 👹\nТеперь финишная прямая.", reply_markup=rmk)
        await msg.answer("Хочешь ли ты добавить дополнительную информацию информацию о себе?", reply_markup=get_yes_no_keyboard)
    else:
        await msg.answer("Пожалуйста, ответьте 'да' или 'нет'.", reply_markup=get_yes_no_keyboard)


# process_additional_info
@router.message(UserForm.additional_info)
async def process_additional_info(msg: Message, state: FSMContext):
    if msg.text.lower() == 'да':
        await state.set_state(UserForm.additional_info_details)
        await msg.answer("Здесь ты можешь рассказать о своих навыках и умениях", reply_markup=rmk)
    elif msg.text.lower() == 'нет':
        await state.set_state(UserForm.photo_upload)
        await msg.answer("Чего-то не хватает. Соли? Перца? Фотографии! Ждем твое фото 🔥", reply_markup=rmk)
    else:
        await msg.answer("Пожалуйста, ответьте 'да' или 'нет'.", reply_markup=get_yes_no_keyboard)


# process_additional_info_details
@router.message(UserForm.additional_info_details)
async def process_additional_info_details(msg: Message, state: FSMContext):
    await state.update_data(additional_info=msg.text)
    await state.set_state(UserForm.photo_upload)
    await msg.answer("Чего-то не хватает. Соли? Перца? Фотографии! Ждем твое фото 🔥", reply_markup=await get_skip_button())


@router.callback_query(lambda c: c.data == 'skip')
async def skip_photo(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await state.set_state(UserForm.resume_check)
    

@router.message(UserForm.photo_upload)
async def photo_upload_and_resume_check(msg: Message, state: FSMContext):
    if msg.photo:
        try:
            username = msg.from_user.username
            user_folder = f"users_files/job_seeker/{username}/photo"
            os.makedirs(user_folder, exist_ok=True)
            file_info = await bot.get_file(msg.photo[-1].file_id)
            file_path = file_info.file_path

            file_name = "resume_photo.jpg"
            file_save_path = os.path.join(user_folder, file_name)
            await bot.download_file(file_path, file_save_path)
            await state.update_data(photo_path=file_save_path)
            await msg.answer("Твое резюме готово!\nВот как вот оно выглядит:")
            '''   
            data = await state.get_data()

            resume = f"<b>{data['desired_position']}</b>\n" \
                    f"<u>{data['fio']}</u>\n" \
                    f"Возраст: {data['age']}\n" \
                    f"Город: {data.get('location_text', 'Не указано')}\n" \
                    f"Гражданство: {data['citizenship']}\n" \
                    f"Желаемый уровень з/п: {data['user_desired_salary_level']}\n" \
                    f"Занятость: {data.get('user_employment_type', 'Не указано')}\n\n" \
                    f"<i>Опыт работы:</i>\n" \
                    
            experience = data.get('experience_data', {})
            if experience: 
                resume += f"<b>{experience.get('company_name', 'Не указано')}</b>\n" \
                        f"Период работы: {experience.get('experience_period', 'Не указано')}\n" \
                        f"Должность: {experience.get('experience_position', 'Не указано')}\n" \
                        f"Основные обязанности: {experience.get('experience_duties', 'Не указано')}\n\n" \
                        
            else:
                resume += "Не указано\n"
            
            additional_info = data.get('user_additional_info', 'Не указано')
            resume += f"<i>Дополнительная информация:</i> {additional_info}\n"
            
            await bot.send_photo(msg.chat.id, photo=types.FSInputFile(file_save_path), caption=resume, reply_markup=await get_save_restart_keyboard())
            '''
            await state.set_state(UserForm.resume_check)

        except Exception as e:
            print(f"An error occurred while processing the photo: {e}")
            traceback.print_exc()
            await msg.answer("Произошла ошибка при загрузке фотографии. Попробуйте еще раз.")
    else:
        await msg.answer("Хм, кажется это не фото..")
        return


@router.message(UserForm.resume_check)
async def process_resume_check(msg: Message, state: FSMContext):
    data = await state.get_data()

    resume = f"<b>{data['desired_position']}</b>\n" \
             f"<u>{data['fio']}</u>\n" \
             f"Возраст: {data['age']}\n" \
             f"Город: {data['location_text']}\n" \
             f"Гражданство: {data['citizenship']}\n" \
             f"Желаемый уровень з/п: {data['desired_salary_level']}\n" \
             f"Занятость: {data.get('employment_type', 'Не указано')}\n\n" \
             f"<i>Опыт работы:</i>\n" \
             
    work_experience = json.loads(data['work_experience_data'])
    if isinstance(work_experience, dict):
        resume += f"<b>{work_experience.get('work_company_name', 'Не указано')}</b>\n" \
                  f"Период работы: {work_experience.get('work_experience_period', 'Не указано')}\n" \
                  f"Должность: {work_experience.get('work_experience_position', 'Не указано')}\n" \
                  f"Основные обязанности: {work_experience.get('work_experience_duties', 'Не указано')}\n" \
                  
    else:
        resume += "Не указано\n"
    username = msg.from_user.username

    additional_info = data.get('additional_info', 'Не указано')
    resume += f"<i>Дополнительная информация:</i> {additional_info}\n"
    photo_path = f"users_files/job_seeker/{username}/photo/resume_photo.jpg"

    if photo_path:
        resume += f"Фото: {photo_path}\n"
    await bot.send_photo(msg.chat.id, photo=types.FSInputFile(photo_path), caption=resume, reply_markup=await get_save_restart_keyboard())
    await msg.answer(f"Ваше резюме:\n\n{resume}\n\nЖелаете что-нибудь подправить или начать заново?", 
                     reply_markup=await get_save_restart_keyboard())


@router.callback_query()
async def proc_con(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.data == 'save_resume' or callback_query.message.text.lower() in ['да', 'save_resume', 'сохранить', '/save_resume', 'Сохранить', 'ыфму', 'Да', 'ДА']:
        await state.set_state(UserForm.resume_confirmation)
        await state.update_data(resume_confirmation="Отправлено")
        await callback_query.message.answer("Резюме отправлено на модерацию.\nВ среднем, она выполняется за 5-10 минут.\nА пока можно пойти и выпить чаю ☕️\nты этого точно заслуживаешь!")
        await main_menu_job_seeker(callback_query.from_user.id, callback_query.message.message_id)

    elif callback_query.data == 'restart_resume' or callback_query.message.text.lower() in ['нет', 'restart_resume', 'отмена', '/restart_resume', 'Отмена']:
        await restart_resume(callback_query.message, state)
        
    elif callback_query.data == 'edit_resume':
        await callback_query.message.answer("Что именно ты хочешь изменить?")

    else: 
        await process_resume_confirmation(callback_query.message, state)
        
    await state.clear()


async def restart_resume(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer("Хорошо, давай заполним твое резюме сначала :)")
    await process_fio(msg=msg, state=state)
    

@router.message(UserForm.resume_confirmation)
async def process_resume_confirmation(msg: Message, state: FSMContext):
    if msg.text.lower()=='да':
        await msg.answer("Резюме отправлено на модерацию.\nВ среднем, она выполняется за 10 минут.\nА пока можно пойти и выпить чаю ☕️\nты этого точно заслуживаешь!")
        await main_menu_job_seeker(msg.from_user.id, msg.message_id)
    else: 
        await msg.answer("Хорошо, давайте перезаполним резюме.")
        await process_fio(msg=msg, state=state)
    await state.clear()