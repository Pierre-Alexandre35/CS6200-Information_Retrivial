import csv
from urllib.parse import urlparse


keywords = ["katrina", "hurricane", "hurricanes", "cyclogenesis", "saffir–simpson", "storm", "camille", " pressure", " wind speed", "Harvey", "cyclone", "atlantic", "winds", "wind", "eyewall", "alma", "dennis", "emily", "alice", "otto", "colin", "danielle", "mbar"];


ranker = {}


def urlContainsKeyWords(url):
  if 


def initDomainRanking():
  with open('utils/domain-ranking.csv') as ranking:
    csv_read = csv.reader(ranking, delimiter=",")
    for row in csv_read:
      ranker[row[1]] = row[0]

def getDomainRank(domain):
  if domain in ranker:
    print(ranker.get(domain))


def urlDomain(url):
    domain = urlparse(url).netloc
    getDomainRank("en-marche.fr")



initDomainRanking()
##print(next(iter(ranker)))
urlDomain("http://www.google.com")
