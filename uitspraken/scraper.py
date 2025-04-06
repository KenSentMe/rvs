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

    url = f"https://www.raadvanstate.nl/uitspraken/?zoeken=true&pager_page=70&Zoe_Selected_facet%3aProceduresoort=78%2c75%2c31%2c47%2c53&kalenderjaar=2025&Zoe_Selected_facet%3aRechtsgebied=80%2c87%2c57%2c58%2c59%2c60%2c61%2c38%2c63%2c56%2c65%2c66%2c67%2c68%2c69%2c70%2c97%2c149%2c113%2c124%2c104%2c114%2c88%2c81%2c137%2c77%2c121%2c132%2c99%2c91%2c71%2c120%2c98%2c95%2c119&Zoe_Selected_facet%3aType+uitspraak=111%2c109&pager_rows=100"

    print("Scraping url " + url)

    driver = webdriver.Firefox()
    driver.get(url)

    # Handle cookie bar
    try:
        cookie_button = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".cookies_buttons input.btn_allow_true"))
        )
        cookie_button.click()
    except TimeoutException:
        print("No cookie bar found or couldn't click it")

    # Try entries until finding a clickable one
    entries = driver.find_elements(By.CSS_SELECTOR, "div.rol-entry.linking")
    entry_clicked = False
    for entry in entries:
        try:
            entry.click()
            entry_clicked = True
            break
        except:
            continue
    
    if not entry_clicked:
        print("No clickable entries found")
        driver.quit()
        return

    while True:
        max_retries = 3
        retry_count = 0
        while retry_count < max_retries:
            try:
                next_button = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.goto-next-result a"))
                )
                break
            except TimeoutException:
                retry_count += 1
                if retry_count == max_retries:
                    print("Max retries reached, driver timeout")
                    driver.quit()
                    return
                print(f"Timeout, retrying ({retry_count}/{max_retries})")
                driver.refresh()  # Refresh the page before retrying
                continue

        link = driver.current_url

        soup = BeautifulSoup(driver.page_source, "html.parser")
        try:
            titel, ecli, datum, samenvatting, trefwoorden, inhoud = get_full_data(soup)
        except Exception as e:  # noqa
            print("Skipping")
            print(e)
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
