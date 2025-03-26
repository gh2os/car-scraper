import sqlite3
from datetime import datetime

def setup_database():
    conn = sqlite3.connect('data/listings.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS listings (
            id INTEGER PRIMARY KEY,
            source TEXT NOT NULL,
            external_id TEXT NOT NULL,
            title TEXT,
            price INTEGER,
            mileage INTEGER,
            location TEXT,
            link TEXT,
            date_scraped DATETIME,
            first_seen DATETIME,
            last_seen DATETIME,
            UNIQUE(source, external_id)
        );
    ''')
    conn.commit()
    conn.close()

def insert_or_update_listing(listing):
    conn = sqlite3.connect('data/listings.db')
    cursor = conn.cursor()
    now = datetime.now()

    cursor.execute('''
        SELECT id, price FROM listings WHERE source = ? AND external_id = ?
    ''', (listing['source'], listing['external_id']))
    result = cursor.fetchone()

    if result:
        # Update existing listing
        listing_id, old_price = result
        cursor.execute('''
            UPDATE listings
            SET price = ?, last_seen = ?
            WHERE id = ?
        ''', (listing['price'], now, listing_id))
    else:
        # Insert new listing
        cursor.execute('''
            INSERT INTO listings (source, external_id, title, price, mileage, location, link, date_scraped, first_seen, last_seen)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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

    conn.commit()
    conn.close()
