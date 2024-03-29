import scrapy

class JobSpider(scrapy.Spider):
    name = 'job_spider'
    start_urls = ['https://spb.hh.ru/']  # Замените на URL сайта с вакансиями

    def parse(self, response):
        # Используем CSS-селекторы или XPath для извлечения информации о вакансиях
        job_listings = response.css('.job-listing')

        for job in job_listings:
            title = job.css('.job-title::text').get()
            company = job.css('.company-name::text').get()
            location = job.css('.job-location::text').get()
            salary = job.css('.job-salary::text').get()

            yield {
                'title': title,
                'company': company,
                'location': location,
                'salary': salary,
            }

        # Если есть следующая страница, переходим к ней
        next_page = response.css('a.next-page::attr(href)').get()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

# Запускаем парсер
from scrapy.crawler import CrawlerProcess

process = CrawlerProcess()
process.crawl(JobSpider)
process.start()