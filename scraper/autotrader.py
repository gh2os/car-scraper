from urllib.parse import urlencode
from playwright.async_api import async_playwright
from database import insert_or_update_listing
import asyncio


def build_autotrader_url(make, model, year_from, year_to, location="vancouver", province="British Columbia"):
    base_url = f"https://www.autotrader.ca/cars/{make.lower()}/{model.lower()}/bc/{location}/"
    query_params = {
        "rcp": "15",
        "rcs": "0",
        "srt": "35",
        "yRng": f"{year_from},{year_to}",
        "oRng": ",160000",
        "prx": "100",
        "prv": province,
        "loc": location,
        "hprc": "True",
        "wcp": "True",
        "sts": "New-Used",
        "inMarket": "advancedSearch"
    }
    return f"{base_url}?{urlencode(query_params)}"


async def scrape_autotrader():
    search_params = [
        {"make": "Mazda", "model": "CX-5", "year_from": 2013, "year_to": 2015},
        {"make": "Toyota", "model": "RAV4", "year_from": 2013, "year_to": 2015},
        {"make": "Honda", "model": "CR-V", "year_from": 2013, "year_to": 2015},
    ]

    listings = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        for params in search_params:
            url = build_autotrader_url(
                params["make"], params["model"], params["year_from"], params["year_to"])
            print(f"Visiting: {url}")
            await page.goto(url)
            await page.wait_for_selector("div.result-item", timeout=10000)

            result_items = await page.query_selector_all("div.result-item")

            for listing in result_items:
                title_el = await listing.query_selector("h2.title")
                price_el = await listing.query_selector("span.price-amount")
                mileage_el = await listing.query_selector("div.kilometers")
                location_el = await listing.query_selector("div.location")
                link_el = await listing.query_selector("a[href^='/go/']")

                title = await title_el.inner_text() if title_el else None
                price = await price_el.inner_text() if price_el else None
                mileage = await mileage_el.inner_text() if mileage_el else None
                location = await location_el.inner_text() if location_el else None
                link = await link_el.get_attribute('href') if link_el else None

                if not link:
                    continue

                listing_data = {
                    "title": title,
                    "price": int(price.replace('$', '').replace(',', '')) if price else None,
                    "mileage": int(mileage.replace(' km', '').replace(',', '')) if mileage else None,
                    "location": location,
                    "link": f"https://www.autotrader.ca{link}",
                    "external_id": link.split('/')[-1],
                    "source": "AutoTrader"
                }

                insert_or_update_listing(listing_data)
                listings.append(listing_data)

        await browser.close()

    return listings
