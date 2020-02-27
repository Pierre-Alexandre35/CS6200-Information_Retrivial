

import requests
from bs4 import BeautifulSoup
import urllib.request

seedUrls = [
    "http://www.nhc.noaa.gov/outreach/history/", 
    "https://en.wikipedia.org/wiki/List_of_Atlantic_hurricane_records",
    "https://en.wikipedia.org/wiki/List_of_Atlantic_hurricane_records",
    "http://en.wikipedia.org/wiki/Hurricane_Katrina"
    ]


def is_absolute(url):
    return bool(url.startswith("http") or url.startswith("https"))
    ##return bool(urllib.parse.urlparse(url).netloc)


def canonicalization(url):
    ##print(urllib.parse.urlparse(url).netloc)

    ##Steep 1: lowercase
    cleanUrl = url.lower()

    #Remove port 80 from http URLs, and port 443 from HTTPS URLs
    if(cleanUrl.endswith(':80')):
        cleanUrl = cleanUrl[:-3]

    if(cleanUrl.endswith(":243")):
        cleanUrl = cleanUrl[:-4]
    else:
        cleanUrl = cleanUrl

    ##Remove fragment such as .html#contact
    cleanUrl = cleanUrl.split("#")[0]

    ##Remove duplicate "/"
    cleanUrl = urllib.parse.urljoin(cleanUrl,urllib.parse.urlparse(cleanUrl).path.replace('//','/'))
    return cleanUrl

def add_incoming_urls(base_url):
    resp = urllib.request.urlopen(base_url)
    soup = BeautifulSoup(resp, from_encoding=resp.info().get_param('charset'))
    for link in soup.find_all('a', href=True):
        if(not is_absolute(link['href'])):
            absolute_url = urllib.request.urljoin(base_url, link['href'])
            print("was relative..." + absolute_url)
        else:
            absolute_url = link['href']
            print("was absolute..." + absolute_url)

        

        ##cleanLink = canonicalization(link['a'])
        ##print(cleanLink)


def urlErrorFree(url):
    try:
        resp = requests.head(url)
        resp.raise_for_status()
        try: 
            if not "text/html" in resp.headers["content-type"]:
                print(url + " - not html")
                return False
        except KeyError:
            print(url + " - key error")
            return False  
    except requests.exceptions.HTTPError as err:
        print(url + " - error: " + err)
        return False
    return True



def crawl(seeds, limit):
    visited = set()
    total_crawled = 0
    for seed in seeds:
        if urlErrorFree(seed):
            visited.add(seed)
            add_incoming_urls(seed)
    
    while(total_crawled < limit):
        total_crawled = total_crawled + 1
    


## Main method that is running the program 
def main():
  crawl_limit = 100
  crawl(seedUrls, crawl_limit)
  


## Run the main() method auto 
if __name__== "__main__":
  main()


