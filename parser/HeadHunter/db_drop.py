import pymysql
import json
import pandas as pd

connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='q1q1q1q1',
                             database='jfdatabase',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

try:
    with open('parsed_vacancies.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Filter out rows with empty or invalid JSON values in the 'skills' column
    filtered_data = [row for row in data if isinstance(row.get('skills'), list)]

    # Convert 'skills' list to comma-separated string
    for row in filtered_data:
        row['skills'] = ', '.join(row['skills'])

    # Convert data to DataFrame
    df = pd.DataFrame(filtered_data)

    # Insert data into MySQL database
    with connection.cursor() as cursor:
        # Disable foreign key checks
        cursor.execute("SET FOREIGN_KEY_CHECKS=0")

        # Truncate the vacancies table
        cursor.execute("TRUNCATE TABLE vacancies")

        # Enable batch insert mode
        cursor.execute("SET SESSION sql_mode='STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION'")

        # Convert DataFrame to list of tuples
        records = df.to_records(index=False)
        values = list(records)

        # Batch insert data into vacancies table
        cursor.executemany("INSERT INTO vacancies (vacancy_id, vacancy_title, company_name, vacancy_url, created_date, employment, experience, salary_info, description, skills) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", values)

        # Commit changes to the database
        connection.commit()

        # Re-enable foreign key checks
        cursor.execute("SET FOREIGN_KEY_CHECKS=1")

finally:
    connection.close()
