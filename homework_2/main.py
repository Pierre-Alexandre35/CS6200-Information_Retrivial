import os #to read every documents in a given file
from bs4 import BeautifulSoup ##validate document format and extract fields from documents 
import re ##words processing

##folder that contains collection of docs
path = "AP_DATA/ap89_collection/"

## the total number of docs is 84,547
number_docs = 0

## list of the words that won't be processed in this homework because too commun and may affect our scores such as 'you', 'that' ...
stopwords = []

token_list = []

def storeStopWords():
    with open("AP_DATA/stoplist.txt", "r") as f:
        for line in f:
            stopwords.extend(line.split())

        
def generateMap(tokens):
    index = 0;
    map = {}
    for token in tokens:
        if token[1] not in map.values():
            map[index] = token[1]
            index = index + 1
            
    return map

def tokenize(docid, doctext):
    ## lower every words in the text 
    doctext = doctext.lower()
    
    doctext = [match.group() for match in re.finditer(r"\w+('\w+)*(\.?\w+)*", doctext, re.M | re.I)]
    
    pre_tokens = [(index + 1, word) for index, word in enumerate(doctext) if word not in stopwords]
    
    termId_map = generateMap(pre_tokens)
    number_terms = len(termId_map)
    
    for token in pre_tokens:
        token_word = token[1];
        for map_key, map_words  in termId_map.items():
            if map_words == token_word:
                ##            doc_id | map_word_id | position in text"
                current_token = (docid, map_key, token[0])
                print(current_token)
                token_list.extend(current_token)
    return token_list

    
    
    
    

## function that given a valid document, will extract and clean every field and that document
def extract_doc_fields(doc):
    ## retrive all TEXT fields for a given document. A document can have multiple TEXT fields
    texts = doc.findAll('TEXT') 
    ##loop over each text field for a given document
    text_data = ""
    for text_block in texts:
        text_data += text_block.get_text()
    ##document id (key) of the current document
    docId = doc.DOCNO.get_text().strip()
    tokenize(docId, text_data)
    

        

## function to process a single xml page and retrieve all DOCs from that page. no return. 
def extract_individual_docs(valid_page):
    global number_docs
    ##find all indiviuals docs in  a given page
    single_docs = valid_page.find_all('DOC')
    for document in single_docs:
        #send the indivual document data to the extract_doc_fields function
        extract_doc_fields(document)
        #increase the total number of valid documents filtered
        number_docs = number_docs + 1

def readDocuments(path):
    for document in os.listdir(path):
        ##Open the current document as a textIOWrapper in encoding UTF-8 
        document = open(path + document)

        ## Try to read the given file and ensure that the given file is a xml file. 
        try: 
            page = document.read()
            valid_page = "<root>" + page + "</root>"
            #only parse valid xml documents
            soup = BeautifulSoup(valid_page, 'xml')
            extract_individual_docs(soup)
        except Exception as e:
            print(str(e), " for: ", document)
            pass

def main():
    storeStopWords();
    readDocuments("AP_DATA/ap89_collection/");
    
if __name__ == "__main__":
    main();