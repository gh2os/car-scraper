import json
import os
import logging
import time
from datetime import datetime
from playwright.sync_api import sync_playwright


def scrape_autotrader_raw(output_dir="output", timestamp=None):
    if timestamp is None:
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

    output_filename = f"autotrader_raw_{timestamp}.json"
    output_path = os.path.join(output_dir, output_filename)
    logging.info(f"Output path: {output_path}")

    urls = [
        "https://www.autotrader.ca/cars/mazda/cx-5/bc/vancouver/?rcp=100&rcs=0&srt=12&yRng=2013%2C2017&prx=500&prv=British%20Columbia&loc=Vancouver%2C%20BC&hprc=True&wcp=True&inMarket=advancedSearch",
        "https://www.autotrader.ca/cars/honda/cr-v/bc/vancouver/?rcp=100&rcs=0&srt=12&pRng=%2C25000&prx=500&prv=British%20Columbia&loc=Vancouver%2C%20BC&hprc=True&wcp=True&inMarket=advancedSearch",
        "https://www.autotrader.ca/cars/toyota/rav4/bc/vancouver/?rcp=100&rcs=0&srt=12&pRng=%2C25000&prx=500&prv=British%20Columbia&loc=Vancouver%2C%20BC&hprc=True&wcp=True&inMarket=advancedSearch"
    ]

    raw_listings = []

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-infobars",
                "--window-size=1200,800"
            ]
        )

        for url in urls:
            context = browser.new_context(  # 🔥 New context per URL
                viewport={"width": 1200, "height": 800},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )

            page = context.new_page()
            print("🌐 Navigating to:", url)

            try:
                page.goto(url, timeout=30000, wait_until="domcontentloaded")
                page.wait_for_timeout(2000)
                page.mouse.wheel(0, 1000)  # trigger lazy load
                page.wait_for_timeout(2000)
            except Exception as e:
                print("❌ Page load failed or was blocked:", e)
                safe_name = url.split("/cars/")[1].split("/")[0]
                page.screenshot(path=f"autotrader_debug_{safe_name}.png")
                page.close()
                context.close()
                continue

            listings = page.query_selector_all("div.result-item-inner")
            print(f"🔍 Found {len(listings)} listings on page")

            for listing in listings:
                title = listing.query_selector(".h2-title .title-with-trim")
                price = listing.query_selector(".price-amount")
                mileage = listing.query_selector(".odometer-proximity")
                location = listing.query_selector(
                    ".proximity-text.overflow-ellipsis")
                link_elem = listing.query_selector(".inner-link")
                outer = listing.evaluate_handle("node => node.parentElement")
                external_id = outer.get_attribute(
                    "data-adid") if outer else None

                if not title or not price:
                    continue

                data = {
                    "source": "autotrader",
                    "external_id": external_id,
                    "title": title.inner_text().strip(),
                    "price": price.inner_text().strip(),
                    "mileage": mileage.inner_text().strip() if mileage else None,
                    "location": location.inner_text().strip() if location else None,
                    "link": "https://www.autotrader.ca" + link_elem.get_attribute("href") if link_elem else None
                }

                raw_listings.append(data)

            page.close()
            context.close()
            time.sleep(1.5)

        browser.close()

    os.makedirs(output_dir, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(raw_listings, f, indent=2)

    print(
        f"✅ Scraped total {len(raw_listings)} listings from {len(urls)} URLs")
    print(f"💾 Saved to {output_path}")
    return raw_listings
