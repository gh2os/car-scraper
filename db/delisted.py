import sqlite3
import logging
from datetime import datetime, timedelta

DB_PATH = "data/listingsnew.db"
THRESHOLD_DAYS = 2
LOG_PATH = "output/price_events.jsonl"


def detect_and_flag_delisted_listings(timestamp=None):
    if timestamp is None:
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

    logging.info(f"📌 Delisting process started at {timestamp}")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cutoff = datetime.utcnow() - timedelta(days=THRESHOLD_DAYS)
    cutoff_str = cutoff.isoformat()

    # Find all stale listings not already marked as delisted
    cursor.execute("""
        SELECT id, title, location, link, last_seen
        FROM listings
        WHERE last_seen < ? AND is_delisted = 0
    """, (cutoff_str,))

    stale_listings = cursor.fetchall()
    print(f"🕵️ Found {len(stale_listings)} newly delisted listings\n")

    # Log file
    with open(LOG_PATH, "a") as log_file:
        for row in stale_listings:
            listing_id, title, location, link, last_seen = row

            print(
                f"❌ {title} | {location} | Last seen: {last_seen[:10]}")
            print(f"   {link}\n")

            # Log delisting event
            event = {
                "event": "delisted",
                "timestamp": timestamp,
                "listing_id": listing_id,
                "title": title,
                "location": location,
                "last_seen": last_seen,
                "link": link,
            }
            log_file.write(f"{event}\n")

            # Mark as delisted in DB
            cursor.execute("""
                UPDATE listings SET is_delisted = 1 WHERE id = ?
            """, (listing_id,))

    conn.commit()
    conn.close()

    print("✅ Delisted status updated in the database.")
