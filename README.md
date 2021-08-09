# Semantic Web Search Application IE
This project was taken as a year long project under IE NITK 2020.

## Demo

![](images/demo_image(1).jpeg)

![](images/demo_image(2).jpeg)

![](images/demo_image(3).jpeg)

![](images/demo_image(4).jpeg)

![](images/demo_image(5).jpeg)

## Requirements
- [ElasticSearch](https://www.elastic.co/downloads/elasticsearch)
- [Flask](https://www.elastic.co/downloads/elasticsearch)
- [Universal Sentence Encoder](https://tfhub.dev/google/universal-sentence-encoder/4)

## Usage

Move the Univesal_Encoder folder to the Spiders folder in the Directory.
Go to the Spiders Directory and run the following command

```
scrapy crawl stackoverflow -o <output file name>.json
```
After installing ElasticSearch, go to its directory and run 

```
.\bin\elasticsearch.bat
```
Move the Universal_Encoder folder back to IE_Web_Search_Application.

Run the API.py file from the root directory using the following command:
```
python api.py
```
Run the App.py file from the root directory using the following command:

```
python app.py
```

## Project Structure
  - __IE\_Web\_Search\_Application__
    - [ElasticSearch Test.ipynb](IE_Web_Search_Application/ElasticSearch%20Test.ipynb)
    - [README.md](IE_Web_Search_Application/README.md)
    - [api.py](IE_Web_Search_Application/api.py)
    - [app.py](IE_Web_Search_Application/app.py)
    - __images__
      - [demo\_image(1).jpeg](IE_Web_Search_Application/images/demo_image(1).jpeg)
      - [demo\_image(2).jpeg](IE_Web_Search_Application/images/demo_image(2).jpeg)
      - [demo\_image(3).jpeg](IE_Web_Search_Application/images/demo_image(3).jpeg)
      - [demo\_image(4).jpeg](IE_Web_Search_Application/images/demo_image(4).jpeg)
      - [demo\_image(5).jpeg](IE_Web_Search_Application/images/demo_image(5).jpeg)
    - __templates__
      - [WhatsApp Image 2021\-03\-06 at 9.40.01 PM.jpeg](IE_Web_Search_Application/templates/WhatsApp%20Image%202021-03-06%20at%209.40.01%20PM.jpeg)
      - [image\_search.html](IE_Web_Search_Application/templates/image_search.html)
      - [index.html](IE_Web_Search_Application/templates/index.html)
      - [result.html](IE_Web_Search_Application/templates/result.html)
      - [search.html](IE_Web_Search_Application/templates/search.html)
      - [style.css](IE_Web_Search_Application/templates/style.css)
    - __universal\_encoder__
      - [saved\_model.pb](IE_Web_Search_Application/universal_encoder/saved_model.pb)
      - __variables__
        - [variables.data\-00000\-of\-00001](IE_Web_Search_Application/universal_encoder/variables/variables.data-00000-of-00001)
        - [variables.index](IE_Web_Search_Application/universal_encoder/variables/variables.index)
    - __wsa\_scraper__
      - [index.py](IE_Web_Search_Application/wsa_scraper/index.py)
      - [scrapy.cfg](IE_Web_Search_Application/wsa_scraper/scrapy.cfg)
      - __wsa\_scraper__
        - [\_\_init\_\_.py](IE_Web_Search_Application/wsa_scraper/wsa_scraper/__init__.py)
        - [items.py](IE_Web_Search_Application/wsa_scraper/wsa_scraper/items.py)
        - [middlewares.py](IE_Web_Search_Application/wsa_scraper/wsa_scraper/middlewares.py)
        - [pipelines.py](IE_Web_Search_Application/wsa_scraper/wsa_scraper/pipelines.py)
        - [settings.py](IE_Web_Search_Application/wsa_scraper/wsa_scraper/settings.py)
        - __spiders__
          - [stackoverflow.py](IE_Web_Search_Application/wsa_scraper/wsa_scraper/spiders/stackoverflow.py)
          - [temp.json](IE_Web_Search_Application/wsa_scraper/wsa_scraper/spiders/temp.json)
          - [test.json](IE_Web_Search_Application/wsa_scraper/wsa_scraper/spiders/test.json)
          - __universal\_encoder__
            - [saved\_model.pb](IE_Web_Search_Application/wsa_scraper/wsa_scraper/spiders/universal_encoder/saved_model.pb)
            - __variables__
              - [variables.data\-00000\-of\-00001](IE_Web_Search_Application/wsa_scraper/wsa_scraper/spiders/universal_encoder/variables/variables.data-00000-of-00001)
              - [variables.index](IE_Web_Search_Application/wsa_scraper/wsa_scraper/spiders/universal_encoder/variables/variables.index)
