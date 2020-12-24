import scrapy
class QuotesSpiderXpath(scrapy.Spider):
    name = 'quotes_xpath'
    start_urls = [
        'http://quotes.toscrape.com/'
    ]
    def parse(self, response):
        title = response.xpath("//title/text").extract()
        quotes = response.xpath("//span[@class ='text']/text()").extract()
        yield {'title': title, 'quotes': quotes}