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
import os


#HTTP Error 308: Permanent Redirect - 	http://www.livescience.com/22522-hurricane-katrina-facts.html

cano = canonical.Canonicalizer()

seedUrls = [
    "http://www.nhc.noaa.gov/outreach/history/", 
    "https://en.wikipedia.org/wiki/List_of_Atlantic_hurricane_records",
    "http://www.cnn.com/2013/08/23/us/hurricane-katrina-statistics-fast-facts",
    "http://en.wikipedia.org/wiki/Hurricane_Katrina"
]
'''
i = 0
urls = []
for seed in seedUrls:
    resp = requests.urlopen(seed)
    soup = BeautifulSoup(resp, from_encoding=resp.info().get_param('charset'))
    
    for link in soup.find_all('a', href=True):
        i = i + 1
        current = cano.canonicalize(seed, link['href']);
        try:
            open_link = requests.urlopen(current)
        except Exception as e:
            with open('error-log.txt', 'a') as log:
                log.write(str(e) + " " +  current + "\n")
print(i)
'''
inlinks_dic = defaultdict(list)

def addToDic(from_urls, to_url):
    for from_url in from_urls:
        inlinks_dic[from_url.url].append(to_url)








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
    except req.exceptions.HTTPError as err:
        print(url + " - error: " + err)
        return False
    return True