import pandas as pd
import json

with open('parsed_vacancies.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

seen_ids = set()
unique_data = []
for vacancy in data:
    if vacancy['vacancy_id'] not in seen_ids:
        unique_data.append(vacancy)
        seen_ids.add(vacancy['vacancy_id'])

for vacancy in unique_data:
    vacancy['created_date'] = vacancy['created_date'].split('+')[0]

def convert_skills(skills):
    if isinstance(skills, list) and skills:
        return ', '.join(skills)
    else:
        return None

for vacancy in unique_data:
    vacancy['skills'] = convert_skills(vacancy.get('skills', []))

df = pd.DataFrame(unique_data)
df.to_csv('vacancies.csv', index=False)
