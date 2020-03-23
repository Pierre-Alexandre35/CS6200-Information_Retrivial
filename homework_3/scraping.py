from bs4 import BeautifulSoup

VALID_TAGS = ['p', 'ul', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'em', 'b', 'i', 'img']

def scrap(content):
    result = ""
    soup = BeautifulSoup(content, 'html.parser')
    for tag_type in VALID_TAGS:
        for tag in soup.find_all(tag_type):
         result += tag.text
    return result