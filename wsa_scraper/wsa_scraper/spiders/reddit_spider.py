import scrapy
from ..items import QuestionListItem

# class RedditSpider(scrapy.Spider):
#     name = "posts"
#     count = 1
#     start_urls = [
#         'https://old.reddit.com/r/programming/'
#     ]

#     def parse(self, response):
#         for post in response.css('div.thing'):

#             yield {
#                 'question': post.css(' a.title::text')[0].get()
#             }
#             next_page = response.css('div.nav-buttons span.next-button a::attr(href)').get()
#             if next_page is not None:
#                 next_page = response.urljoin(next_page)
#                 yield scrapy.Request(next_page, callback=self.parse)


class RedditSpider(scrapy.Spider):
    page = 2
    name = 'posts'
    start_urls = [
        'https://old.reddit.com/r/programming/'
    ]

    def parse(self, response):

        que_set = response.css('div.entry')
        for q in que_set:
            link = q.css('li.first a::attr(href)')[0].get()
            # print(link)
            yield response.follow(url=link, callback=self.parse_question)
        if self.page < 1700:
            self.page += 1
            link = response.css('div.nav-buttons span.next-button a::attr(href)').get()
            yield scrapy.Request(url=link, callback=self.parse)

    def parse_question(self, response):
        items = QuestionListItem()
        # data = response.css('div.inner-content')
        items['question'] = response.css(
            "div.top-matter  a.title::text").extract_first()
        answers_raw = response.xpath('/html/body/div[4]/div[2]/div[3]/div[1]/div[2]/form/div/div')
        answers = []
        if answers_raw:
            for answer in answers_raw:
                data = ''
                raw_data = answer.css("p::text, code::text, .h::text, ul::text").extract()
                for row in raw_data:
                    data = data + row 
                answers.append(data)
        items['details'] = ''
        items['answers'] = answers
        yield items
