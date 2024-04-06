+-------------------+           +--------------------+           +------------------------+          +--------------------+
|      employers    |           |     vacancies      |           |         users          |          | vacancy_applicants |
+-------------------+           +--------------------+           +------------------------+          +--------------------+
| employer_id       |           | vacancy_id         |           | user_id                |          | vacancy_id         |
| employer_username |           | vacancy_title      |           | user_type              |          | user_id            |
| employer_name     |           | company_name       |           | name                   |          +--------------------+
| company_name      |           | vacancy_url        |           | age                    |          
| description       |           | created_date       |           | description            |          
| employer_type     |           | employment         |           | location               |          
| city              |           | working_time_modes |           | nickname               |          
| desired_position  |           | experience         |           | user_fullname          |          
| vacancy_title     |           | salary_info        |           | user_dob               |          
|company_description|           | description        |           | citizenship            |          
| responsibilities  |           | skills             |           | skills                 |          
| requirements      |           |                    |           | experience             |          
| working_conditions|           |                    |           | experience_description |
| image_path        |           |                    |           | additional_info        |          
|                   |           |                    |           | photo_path             |          
+-------------------+           +--------------------+           +------------------------+         

## Связи между таблицами:

- employers - vacancies:
1. employer_id в таблице employers является внешним ключом в таблице vacancies.

- users - vacancy_applicants:
1. user_id в таблице users является внешним ключом в таблице vacancy_applicants.

- vacancies - vacancy_applicants:
1. vacancy_id в таблице vacancies является внешним ключом в таблице vacancy_applicants.

Связь между пользователями и откликами на вакансии осуществляется через таблицу vacancy_applicants!, которая связывает пользователей и вакансии, на которые они откликнулись.