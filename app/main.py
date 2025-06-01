from bs4 import BeautifulSoup
import requests
from fastapi import FastAPI, Path
from typing import List
from pydantic import BaseModel
import asyncio

from api.emcees import emceeRouter as emceeRouter
from api.tournaments import tournamentRouter as tournamentRouter


app = FastAPI()
app.include_router(emceeRouter)
app.include_router(tournamentRouter)