from bs4 import BeautifulSoup
import requests
from lxml.html import fromstring
import time
import urllib3
urllib3.disable_warnings()


with open("links.txt") as f:
    i = 0
    for url in f:
        start = time.time()
        i = i + 1
        time.sleep(0.5)
        response = False
        try:
            r = requests.get(url, stream=True, verify=False)
            if(r.status_code == 200):
                tree = fromstring(r.content)
                ##print(tree.findtext('.//title'))
                response = True
        except requests.exceptions.RequestException:
            r.status_code = "Connection refused"
            print("execpt")
        end = time.time()
        print("request {} is {} {} {} seconds".format(i, response, "and took: ", int(end - start)))



##check if page is html (see what kind of page it is before to make the request)