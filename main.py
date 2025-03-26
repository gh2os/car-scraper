from scraper.database import setup_database

def main():
    setup_database()
    scrape_cargurus()
    scrape_facebook_marketplace()

if __name__ == "__main__":
    main()
