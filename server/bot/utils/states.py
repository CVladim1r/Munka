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
    user_tgid = State()
    user_language_code = State()
    user_fullname = State()
    user_tgname = State()
    
class StartMessage(StatesGroup):
    welcome_message_id = State()

class UserForm(StatesGroup):
    user_tgid = State()
    user_language_code = State()
    user_fullname = State()
    user_tgname = State()
    
    fio = State()
    age = State()
    citizenship = State()
    
    location = State()
    location_text = State()
    location_retry = State()
    
    desired_position = State()
    desired_salary_level = State()
    
    employment_type = State()
    
    work_experience = State()           # -> work_experience_data
    work_company_name = State()         # -> work_experience_data
    work_experience_period = State()    # -> work_experience_data
    work_experience_position = State()  # -> work_experience_data
    work_experience_duties = State()    # -> work_experience_data
    work_experience_another = State()   # -> work_experience_data
    work_experience_data = State()      # << work_experience_data
    
    additional_info = State()
    additional_info_details = State()
    
    photo_upload = State()
    photo_path = State()
    
    resume_check = State()
    resume_confirmation = State()
    
class CommandState(StatesGroup):
    COMMAND_PROCESSING = State()
