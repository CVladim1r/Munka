import requests
from bs4 import BeautifulSoup
import json

def parse_vacancy(vacancy):
    url = vacancy["URL"]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        description_block = soup.find('div', {'class': 'vacancy-description'})
        if description_block:
            description = description_block.find('div', {'data-qa': 'vacancy-description'})
            if description:
                description = description.text.strip()
            else:
                description = None
        else:
            description = None

        skills_block = soup.find('div', {'class': 'bloko-tag-list'})
        if skills_block:
            skills_tags = skills_block.find_all('div', {'class': 'bloko-tag_inline'})
            skills = [tag.span.text.strip() for tag in skills_tags]
        else:
            skills = None

        vacancy["Description"] = description
        vacancy["Skills"] = skills
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
