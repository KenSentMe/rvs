import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime
import locale

from .models import Uitspraak, Trefwoord


def parse_dutch_datetime(date_string):
    locale.setlocale(locale.LC_TIME, 'nl_NL')

    try:
        parsed_datetime = datetime.strptime(date_string, '%d %B %Y')
        return parsed_datetime
    except ValueError:
        return datetime.min


def entry_already_exists(titel):
    return Uitspraak.objects.filter(titel=titel).exists()


def get_full_data(url, headers):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    ecli = soup.find("div", class_="rol-metadata-blok").find(string=re.compile("ECLI:")).get_text(strip=True)
    datum = soup.find(string=re.compile("Datum uitspraak")).find_next('dd').contents[0].get_text(strip=True)
    datum_parsed = parse_dutch_datetime(datum)
    samenvatting = soup.find(string=re.compile("Inhoudsindicatie")).find_next('dd').contents[0].get_text(strip=True)

    trefwoorden_element = soup.find("ul", class_="trefwoorden").find_all("li")
    trefwoorden = []
    for trefwoord in trefwoorden_element:
        title = trefwoord.attrs["title"]
        if title.startswith("Proceduresoort "):
            trefwoorden.append(("proceduresoort", title.split("Proceduresoort ")[1]))
        elif title.startswith("Rechtsgebied "):
            trefwoorden.append(("rechtsgebied", title.split("Rechtsgebied ")[1]))

    inhoud = soup.find("div", id="volledigetekst").find("div", class_="iprox-rich-content").get_text()

    return ecli, datum_parsed, samenvatting, trefwoorden, inhoud


def scrape_and_populate_database(url):
    headers = {
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.8',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 '
                      'Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract the data using BeautifulSoup and populate the database
    # Use the Uitspraak model to create instances and save them to the database

    statements = []

    for element in soup.select("div.rol-entry"):
        link = element.select_one("div.grid-title a.siteLink")["href"]
        titel = element.select_one("div.grid-title a.siteLink").get_text(strip=True)
        print("Found entry " + titel)

        if not entry_already_exists(titel):

            print(titel + " not scraped yet. Start scraping")

            ecli, datum, samenvatting, trefwoorden, inhoud = get_full_data(link, headers)

            trefwoorden_data = []

            for trefwoord in trefwoorden:
                trefwoord_data, _ = Trefwoord.objects.get_or_create(
                    naam=trefwoord[1],
                    type=trefwoord[0]
                )
                trefwoorden_data.append(trefwoord_data)

            uitspraak = Uitspraak(
                titel=titel,
                ecli=ecli,
                samenvatting=samenvatting,
                datum=datum,
                link=link,
                inhoud=inhoud,
            )

            uitspraak.save()

            uitspraak.trefwoorden.set(trefwoorden_data)

            uitspraak.save()
            statements.append("New entry: " + titel)
        else:
            print("Duplicate found: " + titel)
            statements.append("Duplicate found: " + titel)

    return statements
