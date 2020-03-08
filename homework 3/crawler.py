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

buckets = bucket()

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
    return outgoing_nodes
        

def insertToQueue(currentBatch):
    for nodes in currentBatch:
        pQueue.insert(nodes)
    

##  We first start with the seed urls. Then crawl highest scores url's from the queue until the limit is reached.
def crawl(seeds, limit):
    ##A crawled document is a document that has been selected from the queue, processed and stored. Each url visited will be stored in that set in order to avoid to visit the same document > 1. 
    crawled = set()
    total_crawled = 0
    
    ## explore error-free seed urls first. 
    for seed in seeds:
        if urlErrorFree(seed):
            seed_node = Node(seed, 0, 1)
            nodes = retrieve_outlinks(seed_node)
            update_inlink_dic(nodes, seed)
            buckets.insert_nodes(nodes)
            total_crawled = total_crawled + 1

    
    while(total_crawled < 300):
        currentBatch = buckets.pop_nodes(10)
        insertToQueue(currentBatch)
        
        while(pQueue.size() > 0): 
            time.sleep(1)
            print("e")
            current_node = pQueue.pop()
            if urlErrorFree(current_node.url):
                try: 
                    outgoing_nodes = retrieve_outlinks(current_node)
                    update_inlink_dic(outgoing_nodes, current_node.url)
                    buckets.insert_nodes(outgoing_nodes)
                    total_crawled = total_crawled + 1
                except Exception as e:
                    print(str(e))


                
            
            
        
                    


         

            
        


        

    ##while(total_crawled < limit):
        ##total_crawled = total_crawled + 1
    


## Main method that is running the program 
def main():
    store_domains_ranking()
    crawl(seedUrls, 100)

  


## Run the main() method auto 
if __name__== "__main__":
  main()