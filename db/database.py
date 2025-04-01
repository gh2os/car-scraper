import os
import sqlite3
import logging
import json
from datetime import datetime


def init_db(schema_path="models/schema.sql", db_path="data/listingsnew.db"):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)

    with open(schema_path, "r") as f:
        conn.executescript(f.read())

    conn.commit()
    return conn


def insert_or_update_listing(conn, listing):
    cursor = conn.cursor()
    scraped_at = datetime.strptime(
        listing["scraped_at"], "%Y%m%d_%H%M%S").isoformat()

    # Check if listing exists
    cursor.execute('''
        SELECT id FROM listings WHERE source = ? AND external_id = ?
    ''', (listing['source'], listing['external_id']))
    row = cursor.fetchone()

    if row:
        listing_id = row[0]

        # Update existing listing metadata
        cursor.execute('''
            UPDATE listings
            SET title = ?, location = ?, link = ?, last_seen = ?
            WHERE id = ?
        ''', (
            listing["title"],
            listing["location"],
            listing["link"],
            scraped_at,
            listing_id
        ))
        result = "updated"
    else:
        # Insert new listing
        cursor.execute('''
            INSERT INTO listings (source, external_id, title, location, link, first_seen, last_seen)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            listing["source"],
            listing["external_id"],
            listing["title"],
            listing["location"],
            listing["link"],
            scraped_at,
            scraped_at
        ))
        listing_id = cursor.lastrowid
        result = "inserted"

    # Detect price change vs last snapshot
    cursor.execute('''
        SELECT price FROM listing_snapshots
        WHERE listing_id = ?
        ORDER BY scraped_at DESC
        LIMIT 1
    ''', (listing_id,))
    prev = cursor.fetchone()
    prev_price = prev[0] if prev else None

    # Insert snapshot for price/mileage at this scrape
    cursor.execute('''
        INSERT INTO listing_snapshots (listing_id, scraped_at, price, mileage)
        VALUES (?, ?, ?, ?)
    ''', (
        listing_id,
        scraped_at,
        listing.get("price"),
        listing.get("mileage")
    ))

    # Log price change event (JSONL) if needed
    if prev_price is not None and listing.get("price") != prev_price:
        event = {
            "event": "price_change",
            "external_id": listing["external_id"],
            "title": listing["title"],
            "old_price": prev_price,
            "new_price": listing["price"],
            "scraped_at": scraped_at,
            "link": listing["link"],
        }
        os.makedirs("output", exist_ok=True)
        with open("output/price_events.jsonl", "a") as f:
            f.write(json.dumps(event) + "\n")

        logging.info(
            f"📉 Price changed: {prev_price} → {listing['price']} | {listing['title']}")

    return result
