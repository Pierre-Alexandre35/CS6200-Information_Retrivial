import os 
import re 
from bs4 import BeautifulSoup 
import zlib
import pickle
import gzip
import json

## global dictionnary (shared between all batch) that contains every terms seen 
term_id_map = {}

## number of individuals documents extracted 
extracted_docs = 0

## list of idf index 
idf_indexes = []

batch_size = 100

## list of the words that won't be processed in this homework because too commun and may affect our scores such as 'you', 'that' ...
stopwords = []



token_list = []

current_idf = {}

batch_number = 0


def compress(string):

    res = ""

    count = 1

    #Add in first character
    res += string[0]

    #Iterate through loop, skipping last one
    for i in range(len(string)-1):
        if(string[i] == string[i+1]):
            count+=1
        else:
            if(count > 1):
                #Ignore if no repeats
                res += str(count)
            res += string[i+1]
            count = 1
    #print last one
    if(count > 1):
        res += str(count)
    return res


def storeStopWords():
    with open("AP_DATA/stoplist.txt", "r") as f:
        for line in f:
            stopwords.extend(line.split())
            

def update_term_id_map(tokens):
    index = 0
    for token in tokens:
        if token[1] not in term_id_map.values():
            term_id_map[index] = token[1]
            index = index + 1
            
            

## Function to clean and process text for a given doc_id
def tokenize(docid, doctext):
        
    ## lower every words in the text 
    doctext = doctext.lower()
    
    ## clean text by removing punctuation 
    doctext = [match.group() for match in re.finditer(r"\w+('\w+)*(\.?\w+)*", doctext, re.M | re.I)]

    position = 1
    doc_words_frequency = {}
    for word in doctext:
        if word in doc_words_frequency:
            doc_words_frequency[word].append(position);
        else:
            doc_words_frequency[word] = list([position])
        position = position + 1;

        
    for key in doc_words_frequency:
        list_positions = doc_words_frequency[key]
        idf_value = {docid: list_positions}
        if key in current_idf:
            current_idf[key].append(idf_value)
        else:
            current_idf[key] = list()
            current_idf[key].append(idf_value)
            

    

        
    
    ## remove stop_words from the text 
    pre_tokens = [(index + 1, word) for index, word in enumerate(doctext) if word not in stopwords]
    
    ## complete the global dictionnary shared by all words which map a AUTO_INCREMENT key to each word seen 
    update_term_id_map(pre_tokens)
        
    for token in pre_tokens:
        token_word = token[1]
        for map_key, map_words in term_id_map.items():
            if map_words == token_word:
                ##            doc_id | map_word_id | position in text"
                current_token = (docid, map_key, token[0])
                token_list.extend(current_token)
    return token_list





## function to retrieve text and doc id for each individual documents
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
    

def save_in_files(idf, batch_number):
    ## loop over each key of the idf (term)
    
    current_inverted_index = "inverted_indexes/id_" + str(batch_number) + ".txt"
    current_catalog_index = "catalogs/id_" + str(batch_number) + ".txt"

    current_catalog = {}
    
    with open(current_inverted_index, "wb") as my_file:
        for key in idf:
            with open("global_g.txt", "a") as f:
                f.write(key + str(idf[key]) + "\n")
            data = str(idf[key])
            current_offset = my_file.tell()
            compressed_index = gzip.compress(data.encode('ISO-8859-1'))
            current_size = my_file.write(compressed_index)
            current_catalog[key] = (current_offset, current_size)
            
    ##jsonFormat = {"":current_catalog} 
    with open(current_catalog_index, "w") as file:
        file.write(json.dumps(current_catalog))
        
        
        ##pickle.dump(current_catalog, s)
        
            
    
        
        
        
        ##with open(current_catalog, "a") as f:
          ##  f.write(key, ": ", )
        ##current_catalog_file = open(current_catalog, "wb")
        
        

        
        
        

## function to process a single xml page and retrieve all DOCs from that page. no return. 
def extract_individual_docs(valid_page):
    global batch_number
    global extracted_docs
    global current_idf
    ##find all indiviuals docs in  a given page
    single_docs = valid_page.find_all('DOC')
    

    
    
    for document in single_docs:
        ## inverted index for the current batch
        #send the indivual document data to the extract_doc_fields function
        extract_doc_fields(document)
        # #increase the total number of valid documents filtered
        extracted_docs = extracted_docs + 1

        
        ## Add the idf for the batch that just terminated into the global list of idf
        if(extracted_docs % batch_size == 0):
            batch_number = batch_number + 1
            save_in_files(current_idf, batch_number)
            current_idf = current_idf + 1
            idf_indexes.append(current_idf)
            current_idf = {}        
        

def readDocuments(path, batch_size):
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
    storeStopWords()
    readDocuments("AP_DATA/ap89_collection/", 1000)
    
if __name__ == "__main__":
    main();