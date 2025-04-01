import json
import logging
from datetime import datetime
from database import init_db, insert_or_update_listing

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


def load_clean_data_to_db(input_path="output/autotrader_clean.json"):
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

    inserted = 0
    skipped = 0

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
            if insert_or_update_listing(conn, listing):
                inserted += 1
                logging.info(
                    f"[#{idx}] Upserted: {listing['title']} | {listing['external_id']}"
                )
            else:
                logging.warning(
                    f"[#{idx}] Duplicate or failed insert: {listing['title']} | {listing['external_id']}"
                )
        except Exception as e:
            logging.error(f"[#{idx}] DB insert/update failed: {e}")
            skipped += 1

    # ✅ Update time-on-market after all inserts
    update_days_on_market(conn)

    conn.commit()
    conn.close()
    logging.info(
        f"✅ Done: {inserted} listings inserted/updated, {skipped} skipped.")


if __name__ == "__main__":
    load_clean_data_to_db()
