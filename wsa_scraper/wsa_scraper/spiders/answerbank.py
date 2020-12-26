import scrapy
from ..items import AnswerBankItem
class answerbank(scrapy.Spider):
    page = 2
    name = 'answerbank'
    start_urls = [
        "https://www.theanswerbank.co.uk/Technology/?cftype=all_answered"
    ]
    def parse(self, response):
            base_url = 'https://www.theanswerbank.co.uk'
            que_set = response.css('div.head')
            for q in que_set:
                link = q.css('h2 a::attr(href)').get()            
                yield response.follow(url = base_url + link, callback=self.parse_question)
            if self.page < 1799:
                self.page+=1
                yield scrapy.Request(url = "https://www.theanswerbank.co.uk/Technology/?cftype=all_answered&page={}".format(self.page), callback=self.parse)

    def parse_question(self, response):
            items = AnswerBankItem()
            items['question'] = response.css("div.middle h1::text").extract_first()
            details = response.css("div.contentQuestionText::text").extract()
            answer = response.css("div.best-answer-block p::text").extract()
            concat_details = ''
            for detail in details:
                concat_details = concat_details + detail #put a newline if newline separated data is needed
            
            items['details'] = concat_details
            items['answers'] = answer
            yield items