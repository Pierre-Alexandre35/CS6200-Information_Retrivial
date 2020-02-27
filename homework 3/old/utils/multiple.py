from bs4 import BeautifulSoup
import requests
from lxml.html import fromstring
import time
import urllib3
urllib3.disable_warnings()


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



##check if page is html (see what kind of page it is before to make the request)