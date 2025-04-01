CREATE TABLE IF NOT EXISTS listings (
    id INTEGER PRIMARY KEY,
    source TEXT NOT NULL,
    external_id TEXT NOT NULL,
    title TEXT,
    location TEXT,
    link TEXT,
    first_seen TEXT,
    last_seen TEXT,
    is_delisted BOOLEAN DEFAULT 0,
    days_on_market REAL,
    UNIQUE(source, external_id)
);

CREATE TABLE IF NOT EXISTS listing_snapshots (
    id INTEGER PRIMARY KEY,
    listing_id INTEGER NOT NULL,
    scraped_at TEXT NOT NULL,
    price INTEGER,
    mileage INTEGER,
    FOREIGN KEY (listing_id) REFERENCES listings(id)
);