import scrapy

class QuotesSpiderCss(scrapy.Spider):
    name = 'quotes_css'
    start_urls = [
        'http://quotes.toscrape.com/'
    ]
    def parse(self, response):
        title = response.css('title').extract()
        yield {'titletext': title}