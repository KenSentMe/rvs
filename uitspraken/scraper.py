import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime
import locale
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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


def get_full_data(soup):

    titel = soup.find("h1", class_="grid-title").get_text().split("Uitspraak ")[1].strip()
    if len(titel) > 90:
        titel = titel[:90]
    print("Found entry " + titel)
    if entry_already_exists(titel):
        print("Duplicate found: " + titel)
        return

    ecli = soup.find("div", class_="rol-metadata-blok").find(string=re.compile("ECLI:")).get_text(strip=True)
    datum = soup.find(string=re.compile("Datum uitspraak")).find_next('dd').contents[0].get_text(strip=True)
    datum_parsed = parse_dutch_datetime(datum)
    samenvatting = soup.find(string=re.compile("Inhoudsindicatie")).find_next('dd').contents[0].get_text(strip=True)

    trefwoorden_element = soup.find("ul", class_="trefwoorden").find_all("li")
    trefwoorden = []
    for trefwoord in trefwoorden_element:
        tw_title = trefwoord.attrs["title"]
        if tw_title.startswith("Proceduresoort "):
            trefwoorden.append(("proceduresoort", tw_title.split("Proceduresoort ")[1]))
        elif tw_title.startswith("Rechtsgebied "):
            trefwoorden.append(("rechtsgebied", tw_title.split("Rechtsgebied ")[1]))

    inhoud = soup.find("div", id="volledigetekst").find("div", class_="iprox-rich-content").get_text()

    return titel, ecli, datum_parsed, samenvatting, trefwoorden, inhoud


def scrape_and_populate_database():

    url = f"https://www.raadvanstate.nl/uitspraken/?zoeken=true&zoeken_term=&pager_rows=&kalenderjaar=&actualiteit=&Zoe_Selected_facet%3AType%20uitspraak=111&Zoe_Selected_facet%3AProceduresoort=78&Zoe_Selected_facet%3AProceduresoort=75&Zoe_Selected_facet%3AProceduresoort=47&Zoe_Selected_facet%3AProceduresoort=142&Zoe_Selected_facet%3AProceduresoort=141&Zoe_Selected_facet%3AProceduresoort=51&Zoe_Selected_facet%3ARechtsgebied=73&Zoe_Selected_facet%3ARechtsgebied=82&Zoe_Selected_facet%3ARechtsgebied=102&Zoe_Selected_facet%3ARechtsgebied=85&Zoe_Selected_facet%3ARechtsgebied=101&Zoe_Selected_facet%3ARechtsgebied=57&Zoe_Selected_facet%3ARechtsgebied=58&Zoe_Selected_facet%3ARechtsgebied=59&Zoe_Selected_facet%3ARechtsgebied=60&Zoe_Selected_facet%3ARechtsgebied=61&Zoe_Selected_facet%3ARechtsgebied=38&Zoe_Selected_facet%3ARechtsgebied=63&Zoe_Selected_facet%3ARechtsgebied=56&Zoe_Selected_facet%3ARechtsgebied=65&Zoe_Selected_facet%3ARechtsgebied=66&Zoe_Selected_facet%3ARechtsgebied=67&Zoe_Selected_facet%3ARechtsgebied=68&Zoe_Selected_facet%3ARechtsgebied=69&Zoe_Selected_facet%3ARechtsgebied=70&Zoe_Selected_facet%3ARechtsgebied=104&Zoe_Selected_facet%3ARechtsgebied=121"

    print("Scraping url " + url)

    driver = webdriver.Firefox()
    driver.get(url)

    entry = driver.find_element(By.CSS_SELECTOR, "div.rol-entry")
    entry.click()

    while True:
        try:
            next_button = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.goto-next-result a"))
            )
        except TimeoutException:
            print("Driver timeout")
            driver.quit()
            return

        link = driver.current_url

        soup = BeautifulSoup(driver.page_source, "html.parser")
        try:
            titel, ecli, datum, samenvatting, trefwoorden, inhoud = get_full_data(soup)
        except:  # noqa
            print("Skipping")
            next_button.click()
            continue

        if datum >= datetime(2024, 7,1):
            print("Too recent")
            next_button.click()
            continue

        if datum < datetime(2004, 7,1):
            print("Too old")
            driver.quit()
            break

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

        print("Saved " + titel)
        next_button.click()
