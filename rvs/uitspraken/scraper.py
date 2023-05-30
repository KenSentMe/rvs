import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from .models import Uitspraak


def get_full_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    # Perform additional scraping logic to extract the full text from the soup object
    # Extract the necessary content using BeautifulSoup selectors or methods
    full_text = soup.select_one("#volledigetekst div.iprox-rich-content").get_text(strip=True)
    return full_text


def scrape_and_populate_database(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract the data using BeautifulSoup and populate the database
    # Use the Uitspraak model to create instances and save them to the database
    for element in soup.select("div.rol-entry:nth-of-type(n+2) div.grid-edge"):
        samenvatting = element.select_one("p").get_text(strip=True)
        datum = element.select_one("dt:contains('Datum uitspraak') + dd").get_text(strip=True)
        ecli = element.select_one("dt:contains('ECLI') + dd").get_text(strip=True)
        link = element.select_one("a.siteLink")["href"]
        inhoud = get_full_text(link)

        uitspraak = Uitspraak(
            samenvatting=samenvatting,
            datum=datum,
            ecli=ecli,
            link=link,
            inhoud=inhoud,
        )
        uitspraak.save()