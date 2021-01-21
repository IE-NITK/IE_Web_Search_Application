from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import tensorflow_hub as hub
import pickle
import sys
from flask import Flask, request
import tensorflow as tf
import flask

# code reference from the elastic search documentation 
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
if es.ping():
    print('Connected to ES!')
else:
    print('Could not connect!')
    sys.exit()

# loading the encoder model
embed = hub.load('universal_encoder')
def make_vector(query):
    embeddings = embed([query])
    vector = []
    for i in embeddings[0]:
        vector.append(float(i))
    return vector

# connecting to elastic search

# definning a function to normalize the score values of the result.


def search(query):
    def norm_list(lis):
        scores = [x[0] for x in lis]
        try:
            ma = max(scores)
            mi = min(scores)
        except:
            ma=mi=0
        for i in range(len(lis)):
            lis[i][0] = (lis[i][0] - mi)/(ma - mi + 0.0001)
        return lis
    
    request={
            'query':{ 'match':{"question":query } }
            }

    res= es.search(index='test-database1',body=request)
    l1 = []
    for hit in res['hits']['hits']:
        l1.append([hit['_score'] , hit['_id']])
# change the cosine similarity to euclidean distance

    query_vector = make_vector(query)
    request = {"query" : {
                "script_score" : {
                    "query" : {
                        "match_all": {}
                    },
                    "script" : {
                        "source": "cosineSimilarity(params.query_vector, 'total_vectors') + 1.0",
                        "params": {"query_vector": query_vector}
                    }
                }
             }
    }

    res= es.search(index='test-database1',body=request)
    l2 = []
    for hit in res['hits']['hits']:
        l2.append([hit['_score'] , hit['_id']])
    
    l1 = norm_list(l1)
    l2 = norm_list(l2)
    
    # getting the weighted average score for the text search and semantics search
    temp_doc = {}
    for i in l1:
        temp_doc[i[1]]  = i[0]*2
    for i in l2:
        temp_doc[i[1]] = temp_doc.get(i[1] , 0) + i[0]*5
    
    inverse_temp_doc = [(i[1] , i[0])  for i in temp_doc.items()]
    inverse_temp_doc = sorted(inverse_temp_doc , reverse = True)
    return inverse_temp_doc[:10]

# for i in search(" Sql  [duplicate] "):
#     result = es.search(index="test-database1",body={"query": {
#     "terms": {
#       "_id": ['{}'.format(i[1])]
#     }
#   }})
#     for x in result['hits']['hits']:
#         print (x['_source']['question'])
#         print (x['_source']['details'])
#         print (x['_source']['answers'])
# getting the combined search results both semantic and the text based.
app = Flask(__name__)

@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/return_searches', methods=['POST'])
def return_searches():
    answer_no = 1
    to_return = ''
    for i in search(request.form.to_dict()['query']):
        # to_return += '-'*50 + "Answer No:" + str(answer_no) + '-'*50
        # to_return += 2*'<br>'
        # title = total_text_dictionary[i[1]][0]
        # question = total_text_dictionary[i[1]][1]
        # to_return+= "title : " + title + 2*'<br>'
        # to_return += "question : " + question + 2*'<br>'
        # sub_answer = 1
        # for i in total_text_dictionary[i[1]][2:]:
        #     to_return += "subanswer " + str(sub_answer) +' : ' + i + 2*'<br>'
        #     sub_answer+=1
        
        result = es.search(index="test-database1",body={"query": {
        "terms": {
        "_id": ['{}'.format(i[1])]
        }
        }})
        for x in result['hits']['hits']:
            to_return += '-'*50 + "Question No:" + str(answer_no) + '-'*50
            to_return += 2*'<br>'
            title = (x['_source']['question'])
            question = (x['_source']['details'])
            answer = (x['_source']['answers'])[1]
            to_return+= "Question : " + title + 2*'<br>'
            to_return += "Detail : " + question + 2*'<br>'
            to_return +="Answer : " + answer + 2*'<br>'
        answer_no+=1     
    return to_return

if __name__ == '__main__':
    app.run( port=8080)