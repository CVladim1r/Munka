from aiogram.fsm.state import StatesGroup, State

class EmployerForm(StatesGroup):
    name = State()                  # Name and lastname
    company_type = State()          # Тип компании
    
    individual_info = State()       # ИП       -> company_type
    physical_info = State()         # Физ лицо -> company_type
    entity_info = State()           # ООО и АП -> company_type
    
    company_name = State()          # Название компании
    company_info = State()          # Инфа о компании в зависимости от типа
    company_location = State()      # Location

    company_verification = State()  # Верификация

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
    experience_data = State()
    experience_details = State()
    experience_another = State()
    experience_description = State()
    experience_period = State()
    experience_position = State()
    experience_duties = State()

    search_vacancies = State()
    dislike_resume = State()

    user_desired_salary_level = State()
    user_employment_type = State()
    user_fullname = State()
    user_tgid = State()
    user_tgname = State()
    user_language_code = State()
    age = State()
    fio = State()

    photo_upload = State()

    additional_info = State()
    additional_info_details = State()

    user_additional_info  = State()


class CommandState(StatesGroup):
    COMMAND_PROCESSING = State()
