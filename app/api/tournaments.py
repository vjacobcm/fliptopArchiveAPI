from fastapi import APIRouter, Path
from domain.dpd import DosPorDosYear
from domain.links import FliptopURLs

from enum import Enum
from service.scrape import scrapeUrl

tournamentRouter = APIRouter()


@tournamentRouter.get("/tournaments/isabuhay-{year}")
async def get_isabuhay_tournament(year: int = Path(...,title="Isabuhay Tournament Year",description="Isabuhay Tournament Year you want to view.",gte=2013,lt=2025)):
    emcee_list = await get_isabuhay_emcees(year)
    battle_list = await get_isabuhay_battles(year)
    return {
        "year" : year,
        "emcees" : emcee_list,
        "battles" : battle_list
    }
    
@tournamentRouter.get("/tournaments/isabuhay-{year}/emcees")
async def get_isabuhay_emcees(year: int = Path(...,title="Isabuhay Tournament Year",description="Isabuhay Tournament Year you want to view.",gt=2012,lt=2026)):
    emcee_list=[]
    urlString = FliptopURLs['ISBHY'] + str(year)
    parsedHTML = scrapeUrl(urlString)
    emcees = parsedHTML.find('ul', class_='list text-small').find_all('li')
    for emcee in emcees:
        emcee_list.append(emcee.text.strip())
    return {
        "year": year,
        "emcees": emcee_list
        }
    
    
@tournamentRouter.get("/tournaments/isabuhay-{year}/battles")
async def get_isabuhay_battles(year: int = Path(...,title="Isabuhay Tournament Year",description="Isabuhay Tournament Year you want to view.",gt=2012,lt=2026)):
    battle_list=[]
    urlString = FliptopURLs['ISBHY'] + str(year)
    parsedHTML = scrapeUrl(urlString)
    battleDiv = parsedHTML.find('div', class_='row my-3 mb-5')
    battles = battleDiv.find_all('h4')
    events = battleDiv.find_all('span',class_='badge bg-light text-dark')
    
    for n in range(15):
        battle_list.append(battles[n].text.strip() + " (" + events[n].text + ")")
    return {
        "year" : year,
        "tournamentBattles": battle_list
        }


@tournamentRouter.get("/tournaments/dos-por-dos-{year}/emcees")
async def get_dpd_emcees(year: DosPorDosYear):
    emcee_list=[]

    if year == '2024':
        urlString = FliptopURLs['DPDS'].value
    else:
        urlString = FliptopURLs['DPD'].value + DosPorDosYear['y'+year]

    parsedHTML = scrapeUrl(urlString)
    emcees = parsedHTML.find('ul', class_='list text-small').find_all('li')
    
    for emcee in emcees:
        emcee_list.append(emcee.text.strip())
        
    return {
        "year": year,
        "emcees": emcee_list
        }