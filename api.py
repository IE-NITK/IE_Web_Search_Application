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

#Running ElasticSearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
if es.ping():
    print('Connected to ES!')
else:
    print('Could not connect!')


class Controller(Resource):
    def __init__(self):
        self.query = parser.parse_args().get("query", None)
        print(self.query)
        
        #Passing the query into the pre-defined analyzer

        self.baseQuery={           
                
            "query": {
                "match": {
                    "question": {"query": "{}".format(self.query), "analyzer": "standard"}
                }
            }
        }
        

    def get(self):
        #Relevant autocomplete results for the query
        res = es.search(index="ie-3",body=self.baseQuery)
        for x in res['hits']['hits']:
            question = x['_source']['question']
            print(question)
        return res

parser = reqparse.RequestParser()

parser.add_argument("query", type=str, required=True, help="query parameter is Required ")

api.add_resource(Controller, '/autocomplete')


if __name__ == '__main__':
    app.run(debug=True, port=4000)