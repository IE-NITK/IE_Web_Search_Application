from flask import app,Flask
from flask_restful import Resource, Api, reqparse
import elasticsearch
from elasticsearch import Elasticsearch
import datetime
import concurrent.futures
import requests
import json

app = Flask(__name__)
api = Api(app)

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
if es.ping():
    print('Connected to ES!')
else:
    print('Could not connect!')


class Controller(Resource):
    def __init__(self):
        self.query = parser.parse_args().get("query", None)
        print(self.query)
        # self.baseQuery ={
        #     "_source": [],
        #     "size": 0,
        #     "min_score": 0.5,
        #     "query": {
        #         "bool": {
        #             "must": [
        #             {
        #                 "wildcard": {
        #                     "question": {
        #                         "value": "{}".format(self.query)
        #                     }
        #                 }
        #             }
        #             ],
        #             "filter": [],
        #             "should": [],
        #             "must_not": []
        #         }
        #     },
        #     "aggs": {
        #         "auto_complete": {
        #             "terms": {
        #                 "field": "question"
        #                 # "order": {
        #                 #     "_count": "desc"
        #                 # },
        #                 # "size": 10
        #             }
        #         }
        #     }
        # }
        self.baseQuery={           
                
            "query": {
                "match": {
                    "question": {"query": "{}".format(self.query), "analyzer": "standard"}
                }
            }
        }
        

    def get(self):
        res = es.search(index="ie-3",body=self.baseQuery)
        # l2 = []
        # for hit in res['hits']['hits']:
        #     l2.append([hit['_score'] , hit['_id']]
        for x in res['hits']['hits']:
            question = x['_source']['question']
            print(question)
        return res

parser = reqparse.RequestParser()
parser.add_argument("query", type=str, required=True, help="query parameter is Required ")

api.add_resource(Controller, '/autocomplete')


if __name__ == '__main__':
    app.run(debug=True, port=4000)