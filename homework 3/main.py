import bs4
import requests
import urllib.request
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from lxml import html

import lxml.html


keywords = ["katrina", "hurricane", "cyclogenesis", "Saffir–Simpson", "storm", "camille", " pressure", " wind speed", "Harvey", "cyclone"]


## Check if HTTP request is valid (2xx), if not, go to the next url 
def HTTPErrorFree(url):
    try:
        soup = BeautifulSoup(urllib.request.urlopen(url).read())
        return soup
    except urllib.error.HTTPError as e:
        return



## Get the html title of a given link
def getTitle(page):
    soup = BeautifulSoup(page, 'html.parser')
    title_data = soup.title.string
    return title_data



## Return true if there is a match between the html page title and subject keywords
def TitleKeyWordsMatch(title):
    ##Split the title into individual keywords
    title_words = title.split()

    ##Transform each keyword to lowercase
    title_words = [word.lower() for word in title_words]
    print(title_words)

    ##compare title_words and keywords to see if there is a match 
    matches_number = len(set(title_words) & set(keywords))
    
    return matches_number > 0



## return a list of links for a given html page
def storeAllLinks(page):
    soup = BeautifulSoup(html_page)
    with open('links.txt', 'w') as file:
        for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
            file.write(link.get("href") + "\n")


def visitAll():
    with open("links.txt") as f:
        lines = f.readlines()
        id_ = 0
        for url in lines:
            try:
                response = requests.get(url)
                if 'html' in response.headers['content-type'] and response.status_code == 200 :
                    with open(f"data/index{id_}.html", 'w') as html:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        html.write(str(soup))
                        id_ += 1
            except:
                pass


def canonicalization(url):
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

    return cleanUrl

##html_page = urllib.request.urlopen("http://en.wikipedia.org/wiki/Hurricane_Katrina")
##storeAllLinks(html_page)
##title = getTitle(html_page)
##print(TitleKeyWordsMatch(title))





