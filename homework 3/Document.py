import urllib.request as requests
from bs4 import BeautifulSoup



one = "the World is realy nice today"
two = "jame's eat some burger from new-york"

def wordPosition(text):
    words = text.split(" ")
    position = 0
    dic = []
    for word in words:
        lowercase_word = word.lower()
        sequence = (lowercase_word, position)
        dic.append(sequence)
        position += 1
    return dic
        
        

def getText(url):
    html = requests.urlopen(url).read()
    soup = BeautifulSoup(html)

    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text
    
content = getText("https://en.wikipedia.org/wiki/Jean_Messiha")
final = wordPosition(content)

for val in final:
    print(val)





