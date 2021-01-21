import scrapy
from ..items import QuestionListItem
from datetime import datetime
from elasticsearch import Elasticsearch
import tensorflow as tf
import tensorflow_hub as hub

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
if es.ping():
    print('Connected to ES!')
else:
    print('Could not connect!')


structure = {
    "mappings": {
        "properties": {
            "answers": {
                "type": "text",
                "fields": {
                "keyword": {
                "type": "keyword",
                "ignore_above": 256
                }
            }
            },
            "details": {
                "type": "text",
                "fields": {
                "keyword": {
                "type": "keyword",
                "ignore_above": 256
                }
            }
            },
            "question": {
                "type": "text",
                "fields": {
                "keyword": {
                "type": "keyword",
                "ignore_above": 256
                }
            }
            },
            "total_vectors": {
                "type": "dense_vector",
                "dims": 512
            }
        }
    }
}
ret = es.indices.create(index='test-database1', ignore=400, body=structure)

embed = hub.load('universal_encoder')
def make_vector(query):
    embeddings = embed([query])
    vector = []
    for i in embeddings[0]:
        vector.append(float(i))
    return vector




class stackoverflow(scrapy.Spider):
    i=0
    page_no = 2
    name = 'stackoverflow'
    start_urls = [
        "https://stackoverflow.com/questions?tab=frequent&page={}".format(page_no)
    ]
    def parse(self, response):
        base_url = 'https://stackoverflow.com'
        que_set = response.css('div.question-summary')
        for q in que_set:
            self.i+=1
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
        answers_raw = data.css('#answers')
        answers = []

        if answers_raw :
            for answer in answers_raw:
                data = ''
                raw_data = answer.css("p::text, code::text, .h::text, ul::text,a::text,strong::text,em::text, pre::text, span::text").extract()
                for row in raw_data:
                    data = data + row #put a newline if newline separated data is needed
                answers.append(data)

        concat_details = ''
        for detail in details:
            concat_details = concat_details + detail #put a newline if newline separated data is needed
        items['details'] = concat_details
        items['answers'] = answers
        items['total_vectors'] = make_vector(items['question'])
    

        doc = {
        'question': items['question'],
        'details': items['details'],
        'answers': items['answers'],
        'total_vectors': items['total_vectors']
        }
        res = es.index(index="test-database1", body=doc)
        print(res['result'])

        yield items

# res = es.search(index="test-index", body={"query": {"match_all": {}}})
# print("Got %d Hits:" % res['hits']['total']['value'])
