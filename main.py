import logging
from datetime import datetime
from scraper.autotrader import scrape_autotrader_raw
from cleaning.autotrader_cleaner import clean_autotrader_data
from db.load_clean_to_db import load_clean_data_to_db
from db.delisted import detect_and_flag_delisted_listings
from export.daily_snapshot import daily_snapshot


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("output/full_run.log"),
        logging.StreamHandler()
    ],
    force=True
)


def main():
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    logging.info(
        f"🚗 Starting full daily pipeline ({timestamp}): scrape → clean → load → flag delisted")

    # Step 1: Scrape listings
    logging.info("📥 Scraping AutoTrader...")
    scrape_autotrader_raw(timestamp=timestamp)

    # Step 2: Clean scraped data
    logging.info("🧹 Cleaning data...")
    clean_autotrader_data(timestamp=timestamp)

    # Step 3: Insert/update listings
    logging.info("💾 Loading into database...")
    load_clean_data_to_db(timestamp=timestamp)

    # Step 4: Mark delisted cars
    logging.info("🧯 Detecting delisted vehicles...")
    detect_and_flag_delisted_listings(timestamp=timestamp)

    # Step 5: Export snapshot
    logging.info("📤 Exporting daily CSV snapshot...")
    daily_snapshot(timestamp=timestamp)

    logging.info("✅ Daily scraper run complete.")


if __name__ == "__main__":
    main()
