from bs4 import BeautifulSoup
import requests
from fastapi import FastAPI, Path
from typing import List
from enum import Enum
from pydantic import BaseModel
import asyncio
from typing import Optional

class DosPorDosYear(str, Enum):
    y2012 = '2012'
    y2013 = '2013'
    y2017 = '2017'
    y2024 = '2024'



app = FastAPI()

@app.get("/tournaments/isabuhay-{year}")
async def get_isabuhay_tournament(year: int = Path(...,title="Isabuhay Tournament Year",description="Isabuhay Tournament Year you want to view.",gt=2012,lt=2026)):
    emcee_list = await get_isabuhay_emcees(year)
    battle_list = await get_isabuhay_battles(year)
    return {
        "year" : year,
        "emcees" : emcee_list,
        "battles" : battle_list
    }

@app.get("/tournaments/isabuhay-{year}/emcees")
async def get_isabuhay_emcees(year: int = Path(...,title="Isabuhay Tournament Year",description="Isabuhay Tournament Year you want to view.",gt=2012,lt=2026)):
    emcee_list=[]
    urlString = 'https://www.fliptop.com.ph/tournaments/isabuhay-' + str(year)
    html_text = requests.get(urlString).text
    soup = BeautifulSoup(html_text, 'lxml')
    emcees = soup.find('ul', class_='list text-small').find_all('li')
    for emcee in emcees:
        emcee_list.append(emcee.text.strip())
    return {"year": year,
            "emcees": emcee_list}


@app.get("/tournaments/isabuhay-{year}/battles")
async def get_isabuhay_battles(year: int = Path(...,title="Isabuhay Tournament Year",description="Isabuhay Tournament Year you want to view.",gt=2012,lt=2026)):
    battle_list=[]
    urlString = 'https://www.fliptop.com.ph/tournaments/isabuhay-' + str(year)
    html_text = requests.get(urlString).text
    soup = BeautifulSoup(html_text, 'lxml')
    battleDiv = soup.find('div', class_='row my-3 mb-5')
    battles = battleDiv.find_all('h4')
    events = battleDiv.find_all('span',class_='badge bg-light text-dark')
    
    for n in range(15):
        battle_list.append(battles[n].text.strip() + " (" + events[n].text + ")")
    return {
        "year" : year,
        "tournamentBattles": battle_list
        }
        

@app.get("/tournaments/isabuhay-{year}/battles/{emcee_name}")
async def get_isabuhay_battles_per_emcee(year: int = Path(...,title="Isabuhay Tournament Year",description="Isabuhay Tournament Year you want to view.",gt=2012,lt=2026),emcee_name: str = Path(...,title="Battle Emcee",description="Battle Emcee's name whose battles you want to view.")):
    battle_list=[]
    urlString = 'https://www.fliptop.com.ph/tournaments/isabuhay-' + str(year)
    html_text = requests.get(urlString).text
    soup = BeautifulSoup(html_text, 'lxml')
    battleDiv = soup.find('div', class_='row my-3 mb-5')
    battles = battleDiv.find_all('h4')
    events = battleDiv.find_all('span',class_='badge bg-light text-dark')
    
    for n in range(15):
        if(emcee_name.strip() in battles[n].text.strip()):
            battle_list.append(battles[n].text.strip() + " (" + events[n].text + ")")
    return {
        "year": year,
        "emcee": emcee_name,
        "tournamentBattles": battle_list
        }
    
@app.get("/tournaments/dos-por-dos-{year}/emcees")
async def get_dpd_emcees(year: DosPorDosYear):
    emcee_list=[]
    filler = ''
    if year == '2024':
        filler = 'squared-'
    urlString = 'https://www.fliptop.com.ph/tournaments/dos-por-dos-' + filler + DosPorDosYear['y'+year]
    print(urlString)
    html_text = requests.get(urlString).text
    print(html_text)
    soup = BeautifulSoup(html_text, 'lxml')
    emcees = soup.find('ul', class_='list text-small').find_all('li')
    for emcee in emcees:
        emcee_list.append(emcee.text.strip())
    return {"year": year,"emcees": emcee_list}

@app.get("/emcees/{emcee_name}")
async def get_emcee(emcee_name:str):
    urlString = 'https://www.fliptop.com.ph/emcees/' + emcee_name.lower()
    print(urlString)
    html_text = requests.get(urlString).text
    soup = BeautifulSoup(html_text, 'lxml')
    emceeDiv = soup.find('div', class_='col-md-8')
    name = emceeDiv.find('h1', class_='text-uppercase').text
    details = emceeDiv.find('ul', class_='list-unstyled text-small').find_all('li')
    return {
        "name": name,
        "hometown": details[0].text.split(':')[1],
        "groups": details[1].text.split(':')[1].strip(),
        "division": details[2].text.split(':')[1].strip(),
        "year-joined": details[3].text.split(':')[1].strip()
    }

@app.get("/emcees")
@app.get("/emcees/division/{division}")
async def get_emcees(division: Optional[str] = 'all'):
    print(division)
    emcee_list = []
    pageNum = 1
    while True:
        if(division != "all"):
            urlString = 'https://www.fliptop.com.ph/emcees/division/' + division + '?page='
        else:
            urlString = 'https://www.fliptop.com.ph/emcees?page='
        print(urlString)
        html_text = requests.get(urlString + str(pageNum)).text
        soup = BeautifulSoup(html_text, 'lxml')
        print("html text is: "+ urlString + str(pageNum) )
        emceesDiv = soup.find('div', class_='row mt-3 mb-5')
        if not emceesDiv:
            emceesDiv = soup.find('div', class_='row mt-3 mb-2')
        

        emceeDiv = emceesDiv.find_all('h4')
        
        if not emceeDiv:
            break
        
        print(emceeDiv)

        for emcee in emceeDiv:
            name = emcee.text
            name = name.replace(' ','-')
            print(name)
            emcee_details = await get_emcee(name)
            emcee_list.append(emcee_details)
        pageNum += 1
    return {
        "division": division,
        "emcees":emcee_list
        }
