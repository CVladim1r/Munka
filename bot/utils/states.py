from aiogram.fsm.state import StatesGroup, State
class UserForm(StatesGroup):
    nickname = State()
    regStart = State()

    description = State()
    company_name = State()
    
    location = State()
    location_text = State()
    location_retry = State()

    fullname = State() 
    citizenship = State()
    desired_position = State()
    desired_position_v1 = State()
    work_experience = State()
    
    resume_check = State()
    resume_confirmation = State()
    resume_start = State()

    resume_edit = State()

    experience_details = State()
    experience_another = State()
    experience_description = State()
    experience_period = State()
    experience_position = State()
    experience_duties = State()

    search_vacancies = State()
    dislike_resume = State()

    user_desired_salary_level = State()

    user_fullname = State()
    user_tgid = State()
    user_tgname = State()
    user_language_code = State()
    age = State()
    fio = State()

    photo_upload = State()

    additional_info = State()
    additional_info_details = State()

class CommandState(StatesGroup):
    COMMAND_PROCESSING = State()
