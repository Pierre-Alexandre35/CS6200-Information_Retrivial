import requests
from bs4 import BeautifulSoup

with open('links.txt', 'r') as f:
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