import json
import logging
from datetime import datetime
import logging
from db.database import init_db, insert_or_update_listing

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("output/db_load.log"),
        logging.StreamHandler()
    ],
    force=True
)


def update_days_on_market(conn):
    cursor = conn.cursor()
    now = datetime.utcnow()

    cursor.execute("""
        UPDATE listings
        SET days_on_market = julianday(?) - julianday(first_seen)
    """, (now.isoformat(),))

    conn.commit()
    logging.info("🕒 Updated days_on_market for all listings")


def load_clean_data_to_db(input_path=None, timestamp=None):
    if timestamp is None:
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    if input_path is None:
        input_path = f"output/autotrader_clean_{timestamp}.json"
    logging.info("💡 Starting database load process")
    conn = init_db()
    logging.info("Connected to SQLite database")

    try:
        with open(input_path, "r") as f:
            listings = json.load(f)
    except Exception as e:
        logging.error(f"❌ Failed to read input file: {input_path} — {e}")
        return

    logging.info(f"Loaded {len(listings)} listings from {input_path}")

    inserted_count = 0
    skipped_count = 0

    for idx, listing in enumerate(listings, start=1):
        if not listing.get("external_id"):
            try:
                ad_id = listing["link"].split("/")[-2]
                listing["external_id"] = ad_id
                logging.debug(f"[#{idx}] Fallback external_id: {ad_id}")
            except Exception as e:
                logging.warning(
                    f"[#{idx}] Skipping listing with bad link: {listing.get('link')} ({e})"
                )
                skipped += 1
                continue

        try:
            result = insert_or_update_listing(conn, listing)
            if result == "inserted":
                inserted_count += 1
                logging.info(f"[#{idx}] Inserted: {listing['title']} | {listing['external_id']}")
            elif result == "updated_with_price_change":
                inserted_count += 1
                logging.info(f"[#{idx}] Updated (price changed): {listing['title']} | {listing['external_id']}")
            elif result == "updated":
                skipped_count += 1
                logging.info(f"[#{idx}] Skipped (no price change): {listing['title']} | {listing['external_id']}")
        except Exception as e:
            logging.error(f"[#{idx}] DB insert/update failed: {e}")
            skipped += 1

    # ✅ Update time-on-market after all inserts
    update_days_on_market(conn)

    conn.commit()
    conn.close()
    logging.info(f"✅ Done: {inserted_count} listings inserted/updated, {skipped_count} skipped.")
    return inserted_count, skipped_count


if __name__ == "__main__":
    load_clean_data_to_db()
