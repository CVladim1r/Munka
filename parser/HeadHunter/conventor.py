import pandas as pd
import json

# Загрузка данных из JSON файла
with open('parsed_vacancies.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Проверка наличия дубликатов в 'vacancy_id' и их удаление
seen_ids = set()
unique_data = []
for vacancy in data:
    if vacancy['vacancy_id'] not in seen_ids:
        unique_data.append(vacancy)
        seen_ids.add(vacancy['vacancy_id'])

# Преобразование временной зоны в строке даты
for vacancy in unique_data:
    vacancy['created_date'] = vacancy['created_date'].split('+')[0]

# Преобразование массива навыков в строку, если навыки представлены списком
def convert_skills(skills):
    if isinstance(skills, list) and skills:
        return ', '.join(skills)
    else:
        return None  # Возвращаем None для пустых значений

# Преобразование данных перед созданием DataFrame
for vacancy in unique_data:
    vacancy['skills'] = convert_skills(vacancy.get('skills', []))

# Создание DataFrame
df = pd.DataFrame(unique_data)

# Сохранение в CSV
df.to_csv('vacancies.csv', index=False)
