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
    is_delisted BOOLEAN DEFAULT 0,
    days_on_market REAL,
    UNIQUE(source, external_id)
);

CREATE TABLE IF NOT EXISTS price_history (
    id INTEGER PRIMARY KEY,
    listing_id INTEGER NOT NULL,
    recorded_at DATETIME NOT NULL,
    price INTEGER NOT NULL,
    FOREIGN KEY (listing_id) REFERENCES listings(id)
);