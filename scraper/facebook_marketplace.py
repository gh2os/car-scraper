from playwright.sync_api import sync_playwright
from database import insert_or_update_listing

def scrape_facebook_marketplace():
    print("Scraping Facebook Marketplace...")
    listings = []
    search_params = [
        {"make": "Mazda", "model": "CX-5", "year_from": 2013, "year_to": 2015},
        {"make": "Toyota", "model": "RAV4", "year_from": 2013, "year_to": 2015},
        {"make": "Honda", "model": "CR-V", "year_from": 2013, "year_to": 2015},
    ]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Log in to Facebook if necessary
        page.goto("https://www.facebook.com/marketplace")
        # Add login logic here if needed

        for params in search_params:
            search_url = f"https://www.facebook.com/marketplace/search?query={params['make']}%20{params['model']}%20{params['year_from']}-{params['year_to']}"
            page.goto(search_url)

            # Extract listings
            for listing in page.query_selector_all('.listing-row'):
                title = listing.query_selector('.title').inner_text()
                price = listing.query_selector('.price').inner_text().replace('$', '').replace(',', '')
                mileage = listing.query_selector('.mileage').inner_text().replace(' km', '').replace(',', '')
                location = listing.query_selector('.location').inner_text()
                link = listing.query_selector('.title a').get_attribute('href')

                listings.append({
                    "title": title,
                    "price": int(price) if price.isdigit() else None,
                    "mileage": int(mileage) if mileage.isdigit() else None,
                    "location": location,
                    "link": f"https://www.facebook.com{link}"
                })

        browser.close()

    return listings
    print("Scraping Facebook Marketplace...")
    # Add scraping logic here
