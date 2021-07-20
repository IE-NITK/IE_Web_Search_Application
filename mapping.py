#Universal Encoder is required in the parent folder before running the scraper
from datetime import datetime
from elasticsearch import Elasticsearch
import tensorflow as tf
import tensorflow_hub as hub

#Connecting to elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
if es.ping():
    print('Connected to ES!')
else:
    print('Could not connect!')
    exit()

#defining mapping
structure = {
    "settings": {
            "analysis": {
                "filter": {
                "autocomplete_filter": {
                "type": "edge_ngram",
                "min_gram": 1,
                "max_gram": 5
                }
            },
                "analyzer": {
                    "autocomplete_analyzer": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter": [ "lowercase", "autocomplete_filter"]
                }
            }
        }
    },    
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
                },
                "analyzer": "autocomplete_analyzer"
            },
            "tags": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                }
            },
            "upvotes": {
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

#Creating an index using the above defined mapping
res = es.indices.create(index='ie-4', ignore=400, body=structure)