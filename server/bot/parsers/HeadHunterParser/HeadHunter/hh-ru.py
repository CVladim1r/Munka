import requests
from vacancies import vacancies
import json

def get_vacancies(keywords):
    url = "https://api.hh.ru/vacancies"
    area_id = 2  # Код для Санкт-Петербурга
    per_page = 1
    vacancies_list = []
    headers = {
        "User-Agent": "Your User Agent",
    }
    for keyword in keywords:
        params = {
            "text": keyword,
            "area": area_id,
            "per_page": per_page,
        }
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            vacancies = data.get("items", [])
            for vacancy in vacancies:
                vacancy_id = vacancy.get("id")
                vacancy_title = vacancy.get("name")
                vacancy_url = vacancy.get("alternate_url")
                company_name = vacancy.get("employer", {}).get("name")
                created_at = vacancy.get("created_at")
                employment = vacancy.get("employment", {}).get("name")
                working_time_modes = [item['name'] for item in vacancy.get("working_time_modes", [])]
                experience = vacancy.get("experience", {}).get("name")
                salary = vacancy.get("salary")
                if salary:
                    salary_from = salary.get("from")
                    salary_to = salary.get("to")
                    salary_currency = salary.get("currency")
                    if salary_from and salary_to:
                        salary_info = f"{salary_from} - {salary_to} {salary_currency}"
                    elif salary_from and not salary_to:
                        salary_info = f"{salary_from} {salary_currency}"
                    elif not salary_from and salary_to:
                        salary_info = f"{salary_to} {salary_currency}"
                else:
                    salary_info = None
                vacancies_list.append({
                    "vacancy_id": vacancy_id,
                    "vacancy_title": vacancy_title,
                    "company_name": company_name,
                    "vacancy_url": vacancy_url,
                    "created_date": created_at,
                    "employment": employment,
                    "working_time_modes": working_time_modes,
                    "experience": experience,
                    "salary_info": salary_info
                })
        else:
            print(f"Request failed with status code: {response.status_code}")

    with open("vacancies.json", "w", encoding="utf-8") as f:
        json.dump(vacancies_list, f, ensure_ascii=False, indent=4)
    print("Vacancies information saved to vacancies.json")

keywords = vacancies
get_vacancies(keywords)

