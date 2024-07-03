import requests
from bs4 import BeautifulSoup
import json

def parse_vacancy(vacancy):
    url = vacancy["vacancy_url"]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        description_block = soup.find('div', {'class': 'vacancy-description'})
        description = description_block.find('div', {'data-qa': 'vacancy-description'}).text.strip() if description_block else None
        
        skills_block = soup.find('div', {'class': 'bloko-tag-list'})
        skills = [tag.span.text.strip() for tag in skills_block.find_all('div', {'class': 'bloko-tag_inline'})] if skills_block else None
        
        working_time_modes_block = soup.find('p', {'class': 'vacancy-description-list-item'}, {'data-qa': 'vacancy-view-employment-mode'})
        working_time_modes = [mode.strip() for mode in working_time_modes_block.text.split(',')] if working_time_modes_block else []
        
        vacancy["description"] = description
        vacancy["skills"] = skills
        vacancy["working_time_modes"] = working_time_modes
    else:
        print(f"Ошибка при получении страницы {url}: {response.status_code}")
    return vacancy

def main():
    with open('vacancies.json', 'r', encoding='utf-8') as file:
        vacancies = json.load(file)
    parsed_vacancies = []
    for vacancy in vacancies:
        parsed_vacancy = parse_vacancy(vacancy)
        parsed_vacancies.append(parsed_vacancy)
    with open('parsed_vacancies.json', 'w', encoding='utf-8') as file:
        json.dump(parsed_vacancies, file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
