from fastapi import APIRouter, Path
from bs4 import BeautifulSoup
import requests
from typing import Optional
from domain.links import FliptopURLs
from service.scrape import scrapeUrl


emceeRouter = APIRouter()

@emceeRouter.get("/emcees/{emcee_name}")
def get_emcee(emcee_name:str):
    urlString = FliptopURLs['MC'].value + emcee_name.lower()
    parsedHTML = scrapeUrl(urlString)
    emceeDiv = parsedHTML.find('div', class_='col-md-8')
    name = emceeDiv.find('h1', class_='text-uppercase').text
    print(name)
    details = emceeDiv.find('ul', class_='list-unstyled text-small').find_all('li')
    return {
        "name": name,
        "hometown": details[0].text.split(':')[1],
        "groups": details[1].text.split(':')[1].strip(),
        "division": details[2].text.split(':')[1].strip(),
        "year-joined": details[3].text.split(':')[1].strip()
    }
    


@emceeRouter.get("/emcees")
@emceeRouter.get("/emcees/division/{division}")
async def get_emcees(division: Optional[str] = 'all'):
    print(division)
    emcee_list = []
    pageNum = 1
    while True:
        if(division != "all"):
            urlString = FliptopURLs['MCD'] + division + '?page='
        else:
            urlString = FliptopURLs['MC'] + '?page='
        parsedHTML = scrapeUrl(urlString)
        emceesDiv = parsedHTML.find('div', class_='row mt-3 mb-5')
        if not emceesDiv:
            emceesDiv = parsedHTML.find('div', class_='row mt-3 mb-2')
        
        emceeDiv = emceesDiv.find_all('h4')
        
        if not emceeDiv:
            break
        
        for emcee in emceeDiv:
            name = emcee.text
            name = name.replace(' ','-')
            emcee_details = get_emcee(name)
            emcee_list.append(emcee_details)
        pageNum += 1
    return {
        "division": division,
        "emcees":emcee_list
        }
