import scrapy
import json
from scrapy.crawler import CrawlerProcess

class JobSpider(scrapy.Spider):
    name = 'job_spider'
    start_urls = ['https://spb.hh.ru']  # Замените на URL сайта с вакансиями
    
    def __init__(self):
        self.jobs = []

    def parse(self, response):
        # Используем CSS-селекторы или XPath для извлечения информации о вакансиях
        job_listings = response.css('.job-listing')

        for job in job_listings:
            title = job.css('.job-title::text').get()
            company = job.css('.company-name::text').get()
            location = job.css('.job-location::text').get()
            salary = job.css('.job-salary::text').get()

            self.jobs.append({
                'title': title,
                'company': company,
                'location': location,
                'salary': salary,
            })

        # Если есть следующая страница, переходим к ней
        next_page = response.css('a.next-page::attr(href)').get()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def closed(self, reason):
        # Закрытие паука, сохранение данных в файл
        with open('jobs.json', 'w') as f:
            json.dump(self.jobs, f)

# Запускаем паука

process = CrawlerProcess()
process.crawl(JobSpider)
process.start()