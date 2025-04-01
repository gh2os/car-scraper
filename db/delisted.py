import sqlite3
from datetime import datetime, timedelta

DB_PATH = "data/listings.db"
THRESHOLD_DAYS = 7


def detect_and_flag_delisted_listings(timestamp=None):
    if timestamp is None:
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    logging.info(f"Delisting process started at {timestamp}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cutoff = datetime.utcnow() - timedelta(days=THRESHOLD_DAYS)
    cutoff_str = cutoff.isoformat()

    # Find all stale listings not already marked as delisted
    cursor.execute("""
        SELECT id, title, price, mileage, location, link, last_seen
        FROM listings
        WHERE last_seen < ? AND is_delisted = 0
    """, (cutoff_str,))

    stale_listings = cursor.fetchall()
    print(f"🕵️ Found {len(stale_listings)} newly delisted listings\n")

    # Mark each one as delisted
    for row in stale_listings:
        listing_id, title, price, mileage, location, link, last_seen = row

        print(
            f"❌ {title} | ${price:,} | {mileage:,} km | {location} | Last seen: {last_seen[:10]}")
        print(f"   {link}\n")

        cursor.execute("""
            UPDATE listings SET is_delisted = 1 WHERE id = ?
        """, (listing_id,))

    conn.commit()
    conn.close()

    print("✅ Delisted status updated in the database.")


if __name__ == "__main__":
    detect_and_flag_delisted_listings()
