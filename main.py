from database import setup_database, insert_or_update_listing
import asyncio
from scraper.autotrader import scrape_autotrader


def run_scrapers():
    listings = asyncio.run(scrape_autotrader())
    new_count = 0
    updated_count = 0

    for listing in listings:
        result = insert_or_update_listing(listing)
        if result == "new":
            new_count += 1
        elif result == "updated":
            updated_count += 1

    print(f"AutoTrader: {new_count} new, {updated_count} updated listings")


def main():
    setup_database()
    run_scrapers()


if __name__ == "__main__":
    main()
