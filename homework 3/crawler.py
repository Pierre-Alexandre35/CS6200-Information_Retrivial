## list of seeds urls provided by the professor for this assignment
import urllib.request as requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import Canonicalization as canonical
from scoring import get_score 
from scoring import store_domains_ranking
import requests as req
from Node import Node
from collections import defaultdict
from Buckets import Buckets as bucket
from Pqueue import PriorityQueue as pQueue
import time
import os
import Document
import uuid


#HTTP Error 308: Permanent Redirect - 	http://www.livescience.com/22522-hurricane-katrina-facts.html

seedUrls = [
    "http://www.nhc.noaa.gov/outreach/history/", 
    "https://en.wikipedia.org/wiki/List_of_Atlantic_hurricane_records",
    "http://www.cnn.com/2013/08/23/us/hurricane-katrina-statistics-fast-facts",
    "http://en.wikipedia.org/wiki/Hurricane_Katrina"
]

##A visited document is a document that has been scored but not yet crawled. The document is stored in one of the buckets. 
visited = set()

inlinks_dic = defaultdict(list)
outlink_dic = defaultdict(list)

pQueue  = pQueue()


## method to check if a given url is returning a 200 server response. If yes, return true otherwise false. 
def urlErrorFree(url):
    try:
        resp = req.head(url)
        resp.raise_for_status()
        try: 
            if not "text/html" in resp.headers["content-type"]:
                print(url + " - not html")
                print(resp.headers["content-type"])
                return False
        except KeyError:
            print(url + " - key error")
            return False  
    except Exception as e:
        print(str(e))
        return False
    return True


def update_inlink_dic(from_urls, to_url):
    for from_url in from_urls:
            inlinks_dic[from_url.url].append(to_url)

def update_outlink_dic(from_url, to_urls):
    for to_url in to_urls:
        outlink_dic[from_url].append(to_url)
            

def retrieve_outlinks(base_node):
    ##The outgoing urls dictionnary is going to store the href of a given link as a key and it's description as a value
    outgoing_nodes = set()
    base_wave = base_node.wave
    base_url = base_node.url
    
    resp = requests.urlopen(base_url)
    soup = BeautifulSoup(resp, from_encoding=resp.info().get_param('charset'))
    
    for link in soup.find_all('a', href=True):
        clean_url = canonical.Canonicalizer().canonicalize(base_url, link['href'])
        if clean_url not in visited:
            visited.add(clean_url)
            score_outgoing_url = get_score(clean_url, link.text)
            current_node = Node(clean_url, base_wave + 1, score_outgoing_url)
            outgoing_nodes.add(current_node)
            outlink_dic[base_url].append(clean_url)
    return outgoing_nodes
        

def insertToQueue(currentBatch):
    for nodes in currentBatch:
        pQueue.insert(nodes)
    
def hash_id(url):
    return str(uuid.uuid3(uuid.NAMESPACE_URL, url))

def ap89_format(document):
    (raw, text, title) = document.getHtml()
    docId = hash_id(document.getDocId())
    headers = document.getHeader()
    
    return f"{os.linesep}".join([
        "<DOC>",
        f"<DOCNO>{docId}</DOCNO>",
        f"<TITLE>{title}</TITLE>",
        f"<URL>{document.url}</URL>",
        f"<HEADERS>{headers}</HEADERS>",
        "<TEXT>",
        f"{text}",
        "</TEXT>",
        "<RAW>",
        f"{raw}",
        "</RAW>",
        f"</DOC>"
    ])
        
##  We first start with the seed urls. Then crawl highest scores url's from the queue until the limit is reached.
def crawl(seeds, limit):
    ##A crawled document is a document that has been selected from the queue, processed and stored. Each url visited will be stored in that set in order to avoid to visit the same document > 1. 
    crawled = set()
    total_crawled = 0
    current_bucket = bucket()

    ## explore error-free seed urls first. 
    for seed in seeds:
        if urlErrorFree(seed):
            crawled.add(seed)
            seed_node = Node(seed, 0, 1)
            nodes = retrieve_outlinks(seed_node)
            update_inlink_dic(nodes, seed)
            current_bucket.insert_nodes(nodes)
            total_crawled = total_crawled + 1

    
    while(total_crawled < 1000):
        next_buckets = bucket()
        
        while(not current_bucket.isEmpty()):
            current_set = current_bucket.pop_nodes(100);
            pQueue.insert_list(current_set)
            while(pQueue.size() > 0):
                current_node = pQueue.pop()
                time.sleep(0.2)
                if urlErrorFree(current_node.url) and current_node.url not in crawled:
                    try: 
                        outgoing_nodes = retrieve_outlinks(current_node)
                        update_inlink_dic(outgoing_nodes, current_node.url)
                        next_buckets.insert_nodes(outgoing_nodes)
                        total_crawled = total_crawled + 1
                        crawled.add(current_node.url)
                        document = Document.Document(current_node.url)
                        formated_doc = ap89_format(document)
                        temp = str(total_crawled) + ".txt"
                        with open(temp, 'a') as f:
                            f.write(formated_doc)

                    except Exception as e:
                        print(str(e))
                        
        current_bucket = next_buckets


                
    
    
            
        
                    


         

            
        


        

    ##while(total_crawled < limit):
        ##total_crawled = total_crawled + 1
    


## Main method that is running the program 
def main():
    store_domains_ranking()
    crawl(seedUrls, 100)

  


## Run the main() method auto 
if __name__== "__main__":
  main()