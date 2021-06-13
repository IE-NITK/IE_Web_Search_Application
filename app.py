from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import tensorflow_hub as hub
import sys
import io
import pytesseract
from PIL import Image
import requests
from flask import Flask, request, render_template, redirect, url_for, session
import tensorflow as tf
import flask
import json


# Connecting to ElasticSearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
if es.ping():
    print('Connected to ES!')
else:
    print('Could not connect!')
    sys.exit()

# Loading the Universal Encoder
embed = hub.load('universal_encoder')
def make_vector(query):
    embeddings = embed([query])
    vector = []
    for i in embeddings[0]:
        vector.append(float(i))
    return vector

# Function to Normalize the scores of each document

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

    res= es.search(index='ie-3',body=request)
    l1 = []
    for hit in res['hits']['hits']:
        l1.append([hit['_score'] , hit['_id']])
        
# Using Cosine Similarity to calculate scores of each document

    query_vector = make_vector(query)
    request ={
            "query" : {
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
    res= es.search(index='ie-3',body=request)
    l2 = []
    for hit in res['hits']['hits']:
        l2.append([hit['_score'] , hit['_id']])
    
    l1 = norm_list(l1)
    l2 = norm_list(l2)
    
    # Calculating the weighted average score for Text and Semantic Search
    temp_doc = {}
    for i in l1:
        temp_doc[i[1]]  = i[0]*2
    for i in l2:
        temp_doc[i[1]] = temp_doc.get(i[1] , 0) + i[0]*5
    
    inverse_temp_doc = [(i[1] , i[0])  for i in temp_doc.items()]
    inverse_temp_doc = sorted(inverse_temp_doc , reverse = True)

    return inverse_temp_doc[:10]



# Getting the search results.

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

#Home Page
@app.route('/')
def index():
    return flask.render_template('index.html')

#Image Search 
@app.route('/image_search',methods=['GET'])
def image_search():
    return flask.render_template('image_search.html')

#Search Results
@app.route('/return_searches', methods=['POST'])
def return_searches():
    j=0
    result_sup = {}
    
    for i in search(request.form.to_dict()['query']):
        result = es.search(index="ie-3",body={"query": {
        "terms": {
        "_id": ['{}'.format(i[1])]
        }
        }})
        for x in result['hits']['hits']:
            question = x['_source']['question']
            details = x['_source']['details']
            answer = x['_source']['answers']
            upvotes =x['_source']['upvotes']
            tags = x['_source']['tags']
        result_sup[str(j)] = {}
        result_sup[str(j)]["question"] = question
        result_sup[str(j)]["details"] = details
        result_sup[str(j)]["answer"] = answer
        result_sup[str(j)]["upvotes"] = upvotes
        result_sup[str(j)]["tags"] = tags
        j=j+1
    return flask.render_template('search.html',result=result_sup)

#Converting image into textual data
@app.route('/scanner', methods=['POST'])
def scan_file():
    image_data = request.files['file'].read()

    query = pytesseract.image_to_string(Image.open(io.BytesIO(image_data)))
    print(query)
    j=0
    result_sup = {}
    
    for i in search(query):
        result = es.search(index="ie-3",body={"query": {
        "terms": {
        "_id": ['{}'.format(i[1])]
        }
        }})
        for x in result['hits']['hits']:
            question = x['_source']['question']
            details = x['_source']['details']
            answer = x['_source']['answers']
            upvotes =x['_source']['upvotes']
            tags = x['_source']['tags']
        result_sup[str(j)] = {}
        result_sup[str(j)]["question"] = question
        result_sup[str(j)]["details"] = details
        result_sup[str(j)]["answer"] = answer
        result_sup[str(j)]["upvotes"] = upvotes
        result_sup[str(j)]["tags"] = tags
        j=j+1
    return flask.render_template('search.html',result=result_sup)


#Testing the image to text conversion

# @app.route('/result')
# def result():
#     if "data" in session:
#         data = session['data']
#         return render_template(
#             "result.html",
#             title="Result",
#             time=data["time"],
#             text=data["text"],
#             words=len(data["text"].split(" "))
#         )
#     else:
#         return "Wrong request method."



#Autocomplete the search query 
@app.route('/pipe', methods=["GET", "POST"])
def pipe():
    data = request.form.get("data")
    payload = {}
    headers= {}
    url = "http://127.0.0.1:4000/autocomplete?query="+str(data)
    print(url)
    response = requests.request("GET", url, headers=headers, data = payload)
    return response.json()
    
if __name__ == '__main__':
    pytesseract.pytesseract.tesseract_cmd = r'D:\Pytesseract\tesseract'
    app.run( port=8080)