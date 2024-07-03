import json
import pandas as pd
from ....database.db_connector import create_connection

connection = create_connection

try:
    with open('parsed_vacancies.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    filtered_data = [row for row in data if isinstance(row.get('skills'), list)]

    for row in filtered_data:
        row['skills'] = ', '.join(row['skills'])
    df = pd.DataFrame(filtered_data)
    with connection.cursor() as cursor:
        cursor.execute("SET FOREIGN_KEY_CHECKS=0")
        cursor.execute("TRUNCATE TABLE vacancies")
        cursor.execute("SET SESSION sql_mode='STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION'")
        records = df.to_records(index=False)
        values = list(records)

        cursor.executemany("INSERT INTO vacancies (vacancy_id, vacancy_title, company_name, vacancy_url, created_date, employment, experience, salary_info, description, skills) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", values)
        connection.commit()
        cursor.execute("SET FOREIGN_KEY_CHECKS=1")

finally:
    connection.close()
