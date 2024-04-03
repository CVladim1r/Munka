import requests
from vacancies import vacancies
import json

def get_vacancies(keywords):
    url = "https://api.hh.ru/vacancies"
    area_id = 2  # Код для Санкт-Петербурга
    per_page = 3
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
                vacancies_list.append({
                    "ID": vacancy_id,
                    "Title": vacancy_title,
                    "Company": company_name,
                    "URL": vacancy_url
                })
        else:
            print(f"Request failed with status code: {response.status_code}")

    with open("vacancies.json", "w", encoding="utf-8") as f:
        json.dump(vacancies_list, f, ensure_ascii=False, indent=4)

    print("Vacancies information saved to vacancies.json")

# Список интересующих специальностей из файла vacancies.py
keywords = vacancies
get_vacancies(keywords)
