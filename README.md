# rvs

For scraping the data, first run 

`heroku run python manage.py shell`

use the following lines:

`from uitspraken.scraper import scrape_and_populate_database`

and then

`scrape_and_populate_database(10000, [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023], 73)`