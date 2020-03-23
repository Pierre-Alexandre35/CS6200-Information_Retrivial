from elasticsearch import Elasticsearch
global es
es = Elasticsearch()


# generating a new index in the elastic search instance. Default port for elastic search 9200 // kibana (GUI for elastic search): 5601
def initialize_es_instance():
    try:
        es.indices.create(index="ap_dataset_hw3",
                          body={
                              "settings": {
                                  "number_of_shards": 1,
                                  "number_of_replicas": 1,
                                  "analysis": {
                                      "filter": {
                                          "english_stop": {
                                              "type": "stop",
                                              "stopwords_path": "stoplist.txt"
                                          },
                                          "english_stemmer": {
                                              "type": "stemmer",
                                              "language": "english"
                                          },
                                      },
                                      "analyzer": {
                                                "rebuilt_english": {
                                                    "type": "custom",
                                                    "tokenizer": "standard",
                                                    "filter": [
                                                    "lowercase",
                                                    "english_stop",
                                                    "english_stemmer"
                                                    ]
                                                },
                                      }
                                  }
                              },
                              "mappings": {
                                  "properties": {
                                      "title": {
                                          "type": "text",
                                          "store": True
                                      },
                                      "url": {
                                          "type": "text",
                                          "store": True
                                      },
                                      "headers": {
                                          "type": "text",
                                          "index": False,
                                          "store": True
                                      },
                                      "text": {
                                          "type": "text",
                                          "fielddata": True,
                                          "analyzer": "rebuilt_english",
                                          "index_options": "positions"
                                      },
                                      "raw_html": {
                                          "type": "text",
                                          "fielddata": False,
                                          "index": False,
                                          "store": True
                                      },
                                      "in_links": {
                                          "type": "text",
                                          "index": False,
                                          "store": True
                                      },
                                      "out_links": {
                                          "type": "text",
                                          "index": False,
                                          "store": True
                                      }
                                  }
                              }
                          })
        print("index created with success")
    except Exception as e:
        print("index creation failed...", str(e))
