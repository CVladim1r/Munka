from aiogram.fsm.state import StatesGroup, State

class UserForm(StatesGroup):
    nickname = State()
    regStart = State()
    age = State()
    description = State()
    company_name = State()
    location = State()
    fullname = State() 
    citizenship = State()
    desired_position = State()
    work_experience = State()
    experience_details = State()
    experience_another = State()
    resume_check = State()
    resume_confirmation = State()
    resume_start = State()
    skills = State()
    resume_edit = State()
    experience_description = State()
    search_vacancies = State()
    dislike_resume = State()
    
class CommandState(StatesGroup):
    COMMAND_PROCESSING = State()