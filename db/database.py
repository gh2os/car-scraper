import os
import sqlite3
from datetime import datetime


def init_db(schema_path="models/schema.sql", db_path="data/listings.db"):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)

    with open(schema_path, "r") as f:
        conn.executescript(f.read())

    conn.commit()
    return conn


def insert_or_update_listing(conn, listing):
    cursor = conn.cursor()
    now = datetime.utcnow().isoformat()

    # Check if the listing exists
    cursor.execute('''
        SELECT id, price FROM listings WHERE source = ? AND external_id = ?
    ''', (listing['source'], listing['external_id']))
    result = cursor.fetchone()
    if result:
        logging.debug(f"Existing listing found: {result}")

    if result:
        listing_id, old_price = result

        logging.debug(f"Incoming listing: {listing}")
        # Price change? → log to price_history
        if listing['price'] is not None and old_price != listing['price']:
            cursor.execute('''
                INSERT INTO price_history (listing_id, recorded_at, price)
                VALUES (?, ?, ?)
            ''', (listing_id, now, listing['price']))
            print(
                f"📉 Price changed: {old_price} → {listing['price']} | {listing['title']}")

        # Update listing record
        cursor.execute('''
            UPDATE listings
            SET title = ?, price = ?, mileage = ?, location = ?, link = ?, last_seen = ?, date_scraped = ?
            WHERE id = ?
        ''', (
            listing['title'],
            listing['price'],
            listing['mileage'],
            listing['location'],
            listing['link'],
            now,
            now,
            listing_id
        ))
    else:
        logging.debug(f"No existing listing found for: {listing['external_id']}")
        # Insert new listing
        cursor.execute('''
            INSERT INTO listings (
                source, external_id, title, price, mileage, location, link,
                date_scraped, first_seen, last_seen
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            listing['source'],
            listing['external_id'],
            listing['title'],
            listing['price'],
            listing['mileage'],
            listing['location'],
            listing['link'],
            now,
            now,
            now
        ))

        listing_id = cursor.lastrowid

        # Save initial price to price history
        if listing['price'] is not None:
            cursor.execute('''
                INSERT INTO price_history (listing_id, recorded_at, price)
                VALUES (?, ?, ?)
            ''', (listing_id, now, listing['price']))
