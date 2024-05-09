
from aiogram.fsm.context import FSMContext

from bot.cities import CITIES
from bot.utils import format_vacancy
from bot.config_reader import config
from bot.keyboards import *
from bot.utils.states import *
from bot.database.methods import *

from bot.handlers.bot_messages import *

from aiogram.types.input_file import InputFile


async def register_job_seeker(user_tgid, user_tgname, user_fullname, state: FSMContext):
    """
    Регистрация работодателя.
    :param employer_tgid: Telegram ID пользователя
    :param employer_tgname: Telegram username пользователя
    :param user_fullname: Полное имя пользователя
    """
    # Здесь код для регистрации соискателя в базе данных:
    # await db.save_user(user_tgid, user_tgname, user_fullname, user_type="JOB_SEEKER")

    # Вместо прямого вызова функций proc_age и process_location будем устанавливать состояния FSM
    await state.set_state(UserForm.fio)
    # Здесь пример диалога:
    """
    Регитсрация: Работодатель

    Бот: Введите Имя и фамилию. Например: Чумаков Владимир
    Пользователь: Сергей Емельян
    Бот: Какую компанию Вы представляете?
    Пользователь: ООО Котики и Кофе
    Бот: Укажите город, где находится ваша компания.
    Пользователь: Санкт-петербург
    Юридическое или торговое название вашей компании. Если вы ИП или частное лицо, укажите имя и фамилию.
    Пользователь: ИП -> Сергей Емельян
    Укажите город, где находится ваша компания
    """