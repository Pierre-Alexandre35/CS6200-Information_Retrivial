
import bs4
import requests
import urllib.request
import re
from bs4 import BeautifulSoup


response = requests.get("https://en.wikipedia.org/wiki/Mathematics")

if response is not None:
    html = bs4.BeautifulSoup(response.text, 'html.parser')

    title = html.select("#firstHeading")[0].text
    paragraphs = html.select("p")
    for para in paragraphs:
        print (para.text)

    # just grab the text up to contents as stated in question
    intro = '\n'.join([ para.text for para in paragraphs[0:5]])
    print (intro)



html_page = urllib.request.urlopen("http://www.nhc.noaa.gov/outreach/history/")
soup = BeautifulSoup(html_page)
for link in soup.findAll('a', href=True):
    print(link.get('href'))


    def sanitize(dirty_html):
    cleaner = Cleaner(page_structure=True,
                  meta=True,
                  embedded=True,
                  links=True,
                  style=True,
                  processing_instructions=True,
                  inline_style=True,
                  scripts=True,
                  javascript=True,
                  comments=True,
                  frames=True,
                  forms=True,
                  annoying_tags=True,
                  remove_unknown_tags=True,
                  safe_attrs_only=True,
                  safe_attrs=frozenset(['src','color', 'href', 'title', 'class', 'name', 'id']),
                  remove_tags=('span', 'font', 'div')
                  )

    return cleaner.clean_html(dirty_html)


    LSE_URL = "http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/indices/ftse-indices.html"
WAIT_PERIOD = 15

def getTitles(base):
    soup = BeautifulSoup(urllib.request.urlopen(base).read())
    for href in (a["href"] for a in soup.select("a[href]")):
        url = urljoin(base, href)
        soup = BeautifulSoup(urllib.request.urlopen(url).read())
        title = soup.title
        if title:
            with open('somefile.txt', 'a') as the_file:
                the_file.write(title.text.strip())
                

def stock_data_reader():
    stock_data = get_stock_data()
    while True:
        if not stock_data:
            sleep(WAIT_PERIOD) # sleep for a while until next retry
            stock_data = get_stock_data()                
        else:
            break

    print(stock_data) # do something with stock data



def get_stock_data():
    try:
        infile = urllib.request.urlopen(LSE_URL) # Open the URL
    except urllib.error.HTTPError as http_err:
        print("Error: %s" % http_err)
        return None
    else:
        soup = BeautifulSoup(infile)
        for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
            getTitles(link.get('href'))
            with open('somefile.txt', 'a') as the_file:
                the_file.write(link.get('href') + "\n")
                return link.get('href') 



stock_data_reader()