CREATE TABLE listings (
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
