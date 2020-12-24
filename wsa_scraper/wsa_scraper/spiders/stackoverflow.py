import scrapy
from ..items import QuestionListItem
class stackoverflow(scrapy.Spider):
    page_no = 2
    name = 'stackoverflow'
    start_urls = [
        "https://stackoverflow.com/questions?tab=frequent&page={}".format(page_no)
    ]
    def parse(self, response):
        base_url = 'https://stackoverflow.com'
        que_set = response.css('div.question-summary')
        for q in que_set:
            link = q.css('h3 a::attr(href)').get()
            #print(link)
            yield response.follow(url = base_url + link, callback=self.parse_question)
        # if self.page_no<10:
        #     self.page_no +=1
        #     yield scrapy.Request(url = "https://stackoverflow.com/questions?tab=frequent&page={}".format(self.page_no), callback=self.parse)


    def parse_question(self, response):
        items = QuestionListItem()
        data = response.css('div.inner-content')
        items['question'] = data.css("div h1 a.question-hyperlink::text").extract_first()
        details = data.css("div.question div.s-prose p::text, div.question div.s-prose ul::text, div.question div.s-prose .h::text, div.question div.s-prose p code::text, div.question div.post-layout div.s-prose pre code::text").extract()
        answers_raw = data.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "js-post-body", " " ))]')
        answers = []

        if answers_raw :
            for answer in answers_raw:
                data = ''
                raw_data = answer.css("p::text, code::text, .h::text, ul::text").extract()
                for row in raw_data:
                    data = data + row #put a newline if newline separated data is needed
                answers.append(data)

        concat_details = ''
        for detail in details:
            concat_details = concat_details + detail #put a newline if newline separated data is needed
        
        items['details'] = concat_details
        items['answers'] = answers
        yield items
        