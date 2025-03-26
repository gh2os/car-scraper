from database import setup_database, insert_or_update_listing
from scraper.autotrader import scrape_autotrader
from scraper.cargurus import scrape_cargurus
from scraper.facebook_marketplace import scrape_facebook_marketplace

def run_scrapers():
    sources = {
        "AutoTrader": scrape_autotrader,
        "CarGurus": scrape_cargurus,
        "Facebook Marketplace": scrape_facebook_marketplace
    }
    
    summary = {source: {"new": 0, "updated": 0} for source in sources}

    for source, scraper in sources.items():
        listings = scraper()
        for listing in listings:
            # Assuming insert_or_update_listing returns a string "new" or "updated"
            result = insert_or_update_listing(listing)
            summary[source][result] += 1

    for source, counts in summary.items():
        print(f"{source}: {counts['new']} new, {counts['updated']} updated listings")

def main():
    setup_database()
    run_scrapers()

def main():
    setup_database()
    scrape_cargurus()
    scrape_facebook_marketplace()

if __name__ == "__main__":
    main()
