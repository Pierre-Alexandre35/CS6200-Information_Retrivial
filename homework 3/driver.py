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
seedUrls = [
    "http://www.nhc.noaa.gov/outreach/history/", 
    "https://en.wikipedia.org/wiki/List_of_Atlantic_hurricane_records",
    "https://en.wikipedia.org/wiki/List_of_Atlantic_hurricane_records",
    "http://en.wikipedia.org/wiki/Hurricane_Katrina"
    ]
inlinks_dic =defaultdict(list)

## method to check if a given url is returning a 200 server response. If yes, return true otherwise false. 
def urlErrorFree(url):
    try:
        resp = req.head(url)
        resp.raise_for_status()
        try: 
            if not "text/html" in resp.headers["content-type"]:
                print(url + " - not html")
                return False
        except KeyError:
            print(url + " - key error")
            return False  
    except req.exceptions.HTTPError as err:
        print(url + " - error: " + err)
        return False
    return True

def update_inlink_dic(from_urls, to_url):
    for from_url in from_urls:
            inlinks_dic[from_url.url].append(to_url)
            

def retrieve_outlinks(base_url):
    ##The outgoing urls dictionnary is going to store the href of a given link as a key and it's description as a value
    outgoing_urls = []
    resp = requests.urlopen(base_url)
    soup = BeautifulSoup(resp, from_encoding=resp.info().get_param('charset'))
    for link in soup.find_all('a', href=True):
        clean_url = canonical.Canonicalizer().canonicalize(base_url, link['href'])
        score_outgoing_url = get_score(clean_url, link.text)
        current = Node(clean_url, score_outgoing_url)
        outgoing_urls.append(current)
    update_inlink_dic(outgoing_urls, base_url)
    return outgoing_urls
        
        
    

##  We first start with the seed urls. Then crawl highest scores url's from the queue until the limit is reached.
def crawl(seeds, limit):
    ##A visited document is a document that has been selected from the queue, processed and stored. Each url visited will be stored in that set in order to avoid to visit the same document > 1. 
    visited = set()
    total_crawled = 0
    
    
    ## explore error-free seed urls first. 
    for seed in seeds:
        if urlErrorFree(seed):
            visited.add(seed)
            nodes = retrieve_outlinks(seed)
    for node in nodes:
        print(node.url, node.score)
        
    for key, value in inlinks_dic.items() :
        print("key: ", key, " -- value:", value)

    ##while(total_crawled < limit):
        ##total_crawled = total_crawled + 1
    


## Main method that is running the program 
def main():
    store_domains_ranking()
    crawl(seedUrls, 100)

  


## Run the main() method auto 
if __name__== "__main__":
  main()