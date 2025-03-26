from playwright.sync_api import sync_playwright
from database import insert_or_update_listing
import requests


def scrape_cargurus():
    print("Scraping CarGurus...")
    listings = []
    search_params = [
        {"make": "Mazda", "model": "CX-5", "year_from": 2013, "year_to": 2015},
        {"make": "Toyota", "model": "RAV4", "year_from": 2013, "year_to": 2015},
        {"make": "Honda", "model": "CR-V", "year_from": 2013, "year_to": 2015},
    ]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for params in search_params:
            url = f"https://www.cargurus.ca/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?zip=00000&showNegotiable=true&sortDir=ASC&sourceContext=carGurusHomePageModel&distance=50000&entitySelectingHelper.selectedEntity=d{params['year_from']}&entitySelectingHelper.selectedEntity2=d{params['year_to']}&entitySelectingHelper.selectedEntity3=m{params['make']}&entitySelectingHelper.selectedEntity4=m{params['model']}"
            page.goto(url)

            # Extract listings
            for listing in page.query_selector_all('.listing-row'):
                title = listing.query_selector('.title').inner_text()
                price = listing.query_selector(
                    '.price').inner_text().replace('$', '').replace(',', '')
                mileage = listing.query_selector(
                    '.mileage').inner_text().replace(' km', '').replace(',', '')
                location = listing.query_selector('.location').inner_text()
                link = listing.query_selector('.title a').get_attribute('href')

                listings.append({
                    "title": title,
                    "price": int(price) if price.isdigit() else None,
                    "mileage": int(mileage) if mileage.isdigit() else None,
                    "location": location,
                    "link": f"https://www.cargurus.ca{link}"
                })

        browser.close()

    return listings
    print("Scraping CarGurus...")
    # Add scraping logic here
