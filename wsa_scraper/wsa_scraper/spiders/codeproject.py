import scrapy
from ..items import QuestionListItem
class codeproject(scrapy.Spider):
    page_no = 1
    name = 'codeproject'
    start_urls = [
        "https://www.codeproject.com/search.aspx?q=elasticsearch&doctypeid=4%3b5&pgnum={}".format(page_no)
    ]
    def parse(self, response):
        base_url = 'https://www.codeproject.com'
        que_set = response.css('div.entry')
        for q in que_set:
            link = q.css('span.title a::attr(href)').get()
            #print(link)
            yield response.follow(url = link, callback=self.parse_question)
        if self.page_no<10:
             self.page_no +=1
             yield scrapy.Request(url = "https://www.codeproject.com/search.aspx?q=elasticsearch&doctypeid=4%3b5&pgnum={}".format(self.page_no), callback=self.parse)


    def parse_question(self, response):
        items = QuestionListItem()
        data = response.css('#contentdiv')
        items['question'] = data.css("h1::text").extract_first()
        # details = data.css("div.question div.s-prose p::text, div.question div.s-prose ul::text, div.question div.s-prose .h::text, div.question div.s-prose p code::text, div.question div.post-layout div.s-prose pre code::text").extract()
        answers_raw = data.css('div.answer')
        answers = []

        if answers_raw :
            for answer in answers_raw:
                data = ''
                raw_data = answer.css("p::text, code::text, .h::text, ul::text, pre::text, span::text, div.text::text").extract()
                for row in raw_data:
                    data = data + row #put a newline if newline separated data is needed
                answers.append(data)

        # concat_details = ''
        # for detail in details:
        #     concat_details = concat_details + detail #put a newline if newline separated data is needed
        
        # items['details'] = concat_details
        items['answers'] = answers
        yield items