async def format_vacancy(vacancy):
    formatted_vacancy = f"<b>{vacancy['vacancy_title']}</b>\n\n"
    formatted_vacancy += f"<b>Компания:</b> {vacancy['company_name']}\n"
    formatted_vacancy += f"<b>Дата создания:</b> {vacancy['created_date']}\n"
    formatted_vacancy += f"<b>Тип занятости:</b> {vacancy['employment']}\n"
    formatted_vacancy += f"<b>Требуемый опыт работы:</b> {vacancy['experience']}\n"
    
    # Проверяем наличие информации о зарплате
    if 'salary_info' in vacancy and vacancy['salary_info']:
        formatted_vacancy += f"<b>Зарплата:</b> {vacancy['salary_info']}\n\n"
    else:
        formatted_vacancy += "<b>Зарплата:</b> Обсуждается лично\n\n"
    
    # Отдельно форматируем описание, чтобы избежать слипания
    description = vacancy['description'].strip()
    formatted_vacancy += f"<b>Описание:</b>\n"
    formatted_vacancy += f"{description}\n\n"

    #formatted_vacancy += f"<b>Ключевые навыки:</b> {vacancy['skills']}\n"
    #formatted_vacancy += f"<b>Сылка на версию hh:</b>\n"
    formatted_vacancy += f"<a href='{vacancy['vacancy_url']}'>Ссылка на вакансию</a>"
    return formatted_vacancy
