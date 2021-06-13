
import scrapy

class QuestionListItem(scrapy.Item):
    id = scrapy.Field()
    question = scrapy.Field()
    details = scrapy.Field()
    answers = scrapy.Field()
    upvotes = scrapy.Field()
    tags = scrapy.Field()
    total_vectors = scrapy.Field()
