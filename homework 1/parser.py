import os
import re

from datetime import datetime
from elasticsearch import Elasticsearch
es = Elasticsearch() 


class Document:
    def __init__(self, docNo, fileId, second, head, dateLine, text):
        self.docNo = docNo
        self.fileId = fileId
        self.second = second
        self.dateLine = dateLine
        self.text = text



documentStart = '<DOC>'
documentEnd = '</DOC>'
keyID = '<DOCNO>'
contentStart = '<TEXT>'
contentEnd =  '</TEXT>'

dir_name = '/Users/Pierre-Alexandre/Documents/Classes/Information Retrivial/homework 1/AP_DATA/ap89_collection'
relativePath = 'AP_DATA/ap89_collection'

documentsList = list()

## loop over all the documents in the AP_DATA folder
for filename in os.listdir(relativePath):
    
    ## current document location
    currentPath = os.path.join(relativePath, filename)

    #open that current document
    f = open(currentPath)
    i = 0
    ## read each document <DOC></DOC> in each file individualy 
    for individualDoc in filename


    for word in f.read().split():
        print(i, " ", word)
        ## in the word starts with <DOC> then it's a new doc
        
        if(word == documentStart):
            i = i + 1
            
            '''current = ""
            while(word != documentEnd):
                    current += word
        print(current)
        documentsList.append(current)'''
        documentEnd = documentEnd            
        ##current = Document(null, null, null, null, null, null)
        ##documentsList.append(current)





{
    "settings" : {
        "number_of_shards": 1,
        "number_of_replicas": 1,
        "analysis": {
            "filter": {
                "english_stop": {
                    "type": "stop",
                    "stopwords_path": "my_stoplist.txt"
                }
            },
            "analyzer": {
                "stopped": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter": [
                        "lowercase",
                        "english_stop"
                    ]
                }
            }
      }
    },
    "mappings": {
        "properties": {
            "text": {
                "type": "text",
                "fielddata": True,
                "analyzer": "stopped",
                "index_options": "positions"
            }
        }
    }
}

