import scrapy
import json

class HhRuSpider(scrapy.Spider):
    name = 'hh_ru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy']

    def parse(self, response):
        # Парсим ссылки на страницы с вакансиями
        vacancy_links = response.css('.vacancy-serp-item__info-title a::attr(href)').getall()
        for link in vacancy_links:
            yield response.follow(link, callback=self.parse_vacancy)

        # Переходим на следующую страницу
        next_page = response.css('a.HH-Pager-Controls-Next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_vacancy(self, response):
        # Парсим информацию о вакансии
        title = response.css('.vacancy-title h1::text').get()
        salary = response.css('.vacancy-title p::text').get()
        company = response.css('.vacancy-company-name::text').get()
        location = response.css('.vacancy-address-text::text').get()
        description = response.css('.vacancy-description::text').get()

        # Формируем словарь с данными о вакансии
        vacancy_data = {
            'title': title,
            'salary': salary,
            'company': company,
            'location': location,
            'description': description
        }

        # Сохраняем данные в файл jobs.json
        with open('jobs.json', 'a', encoding='utf-8') as f:
            f.write(json.dumps(vacancy_data, ensure_ascii=False) + '\n')