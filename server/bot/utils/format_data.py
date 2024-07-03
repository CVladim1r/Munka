async def format_vacancy(vacancy):
    formatted_vacancy = f"<b>{vacancy.get('vacancy_title', 'Не указано')}</b>\n\n"
    formatted_vacancy += f"<b>Компания:</b> {vacancy.get('vacancies_company_name', 'Не указано')}\n"
    formatted_vacancy += f"<b>Дата создания:</b> {vacancy.get('vacancies_created_date', 'Не указана')}\n"
    formatted_vacancy += f"<b>Тип занятости:</b> {vacancy.get('vacancies_employment', 'Не указан')}\n"
    formatted_vacancy += f"<b>Требуемый опыт работы:</b> {vacancy.get('vacancies_experience', 'Не указан')}\n"
    
    # Проверяем наличие информации о зарплате
    if 'vacancies_salary_info' in vacancy and vacancy['vacancies_salary_info']:
        formatted_vacancy += f"<b>Зарплата:</b> {vacancy['vacancies_salary_info']}\n\n"
    else:
        formatted_vacancy += "<b>Зарплата:</b> Обсуждается лично\n\n"
    
    # Отдельно форматируем описание, чтобы избежать слипания
    description = vacancy.get('vacancy_description', 'Описание отсутствует')
    formatted_vacancy += f"<b>Описание:</b>\n"
    formatted_vacancy += f"{description}\n\n"
    
    #Сслыка на вакансию с HeadHunter
    #formatted_vacancy += f"<a href='{vacancy.get('vacancy_url', '')}'>Ссылка на вакансию</a>"
    
    return formatted_vacancy

