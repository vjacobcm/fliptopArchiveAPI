import requests
from bs4 import BeautifulSoup

def scrapeUrl(urlString):
    scrapedHTML = requests.get(urlString).text
    return BeautifulSoup(scrapedHTML, 'lxml')