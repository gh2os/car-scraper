import asyncio
from scraper.autotrader import scrape_autotrader


def main():
    listings = asyncio.run(scrape_autotrader())
    print(f"Found {len(listings)} listings")
    for listing in listings[:3]:  # print only first 3 for brevity
        print(listing)


if __name__ == "__main__":
    main()
