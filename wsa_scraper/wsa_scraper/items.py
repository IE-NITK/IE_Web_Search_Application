# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WsaScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class QuestionListItem(scrapy.Item):
    question = scrapy.Field()
    details = scrapy.Field()
    answers = scrapy.Field()
