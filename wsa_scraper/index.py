import requests
import json
from elasticsearch import Elasticsearch
#before this we need to check that no other index present
def check_if_index_is_present(url):
    response = requests.request("GET", url, data="")
    json_data = json.loads(response.text)
    return json_data
#cd into wsa_scraper
#curl -H "Content-Type: application/json" -XPOST "localhost:9200/bank/_bulk?pretty&refresh" --data-binary "@stackoverflow_temp.json"

if __name__ == "__main__":
    url="http://localhost:9200/_template/search_engine_template/"
    response = requests.request("GET", url, data="")
    if(len(response.text)>2):
        response_del=requests.request("DELETE",url)
    
    payload={
        "template":"stackoverflow",
        "settings":{
            "number_of_shards":1
        },
        "mappings": {
            "tutorials":{
                "_source": {
                    "enabled": True
                },
                "properties":{
                    "question":{
                        "type":"text"
                    },
                    "details":{
                        "type":"text"
                    },
                    "answers":{
                        "type":"text"
                    }
                }
            }
        }
    }

    # To load data
    payload=json.dumps(payload)
    headers={
        'Content-Type':"application/json",
        'cache-control':"no-cache"
    }
    response = requests.request("PUT", url, data=payload, headers=headers)
    if (response.status_code == 200):
        print("Created a new template: search_engine_template")

    url="http://localhost:9200/stackoverflow"
    json_data = check_if_index_is_present(url)

    if(not 'error' in json_data):
        response = requests.request("DELETE", url)

    response = requests.request("PUT", url)
    if (response.status_code == 200):
        print(" Created an index: stackoverflow")
    
    # payload = {
    #   "mappings": {
    #     "titles" : {
    #       "properties" : {
    #         "title" : { "type" : "string" },
    #         "title_suggest" : {
    #           "type" :     "completion",
    #           "analyzer" :  "standard",
    #           "search_analyzer" : "standard",
    #           "preserve_position_increments": False,
    #           "preserve_separators": False
    #         }
    #       }
    #     }
    #   }
    # }
    # payload = json.dumps(payload)
    # response = requests.request("PUT", url, data=payload, headers=headers)
    