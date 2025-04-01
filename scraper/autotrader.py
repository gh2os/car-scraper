from playwright.sync_api import sync_playwright
import json
import os


def scrape_autotrader_raw(output_path="output/autotrader_raw.json"):
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-infobars",
                "--window-size=1200,800"
            ]
        )

        context = browser.new_context(
            viewport={"width": 1200, "height": 800},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )

        page = context.new_page()

        url = "https://www.autotrader.ca/cars/mazda/cx-5/bc/vancouver/?rcp=100&rcs=0&srt=12&yRng=2013%2C2017&prx=500&prv=British%20Columbia&loc=Vancouver%2C%20BC&hprc=True&wcp=True&inMarket=advancedSearch"
        print("Navigating to:", url)

        try:
            page.goto(url, timeout=30000, wait_until="domcontentloaded")
            page.wait_for_timeout(5000)
        except Exception as e:
            print("Page load failed or was blocked:", e)
            page.screenshot(path="autotrader_debug.png")
            browser.close()
            return []

        listings = page.query_selector_all("div.result-item-inner")
        raw_listings = []

        for idx, listing in enumerate(listings):
            title = listing.query_selector(".h2-title .title-with-trim")
            price = listing.query_selector(".price-amount")
            mileage = listing.query_selector(".odometer-proximity")
            location = listing.query_selector(
                ".proximity-text.overflow-ellipsis")
            link_elem = listing.query_selector(".inner-link")
            outer = listing.evaluate_handle("node => node.parentElement")
            external_id = outer.get_attribute("data-adid") if outer else None

            data = {
                "source": "autotrader",
                "external_id": external_id,
                "title": title.inner_text().strip() if title else None,
                "price": price.inner_text().strip() if price else None,
                "mileage": mileage.inner_text().strip() if mileage else None,
                "location": location.inner_text().strip() if location else None,
                "link": "https://www.autotrader.ca" + link_elem.get_attribute("href") if link_elem else None
            }

            raw_listings.append(data)

        browser.close()

        # Save to JSON
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(raw_listings, f, indent=2)

        print(f"Scraped {len(raw_listings)} listings from AutoTrader")
        print(f"Saved {len(raw_listings)} listings to {output_path}")
        return raw_listings
