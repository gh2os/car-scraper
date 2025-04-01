import sqlite3
import csv
from datetime import datetime
from pathlib import Path


def daily_snapshot(db_path="data/listingsnew.db", export_dir="output/snapshots", timestamp=None):
    if timestamp is None:
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    Path(export_dir).mkdir(parents=True, exist_ok=True)

    filename = f"{export_dir}/autotrader_snapshot_{timestamp}.csv"

    cursor.execute("""
        SELECT 
            l.source,
            l.external_id,
            l.title,
            s.price,
            s.mileage,
            l.location,
            l.link,
            l.first_seen,
            l.last_seen,
            ROUND(julianday(l.last_seen) - julianday(l.first_seen), 3) AS days_on_market,
            l.is_delisted
        FROM listings l
        JOIN listing_snapshots s ON s.id = (
            SELECT id FROM listing_snapshots
            WHERE listing_id = l.id
            ORDER BY scraped_at DESC
            LIMIT 1
        )
        ORDER BY s.price ASC
    """)

    rows = cursor.fetchall()
    headers = [desc[0] for desc in cursor.description]

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    print(f"📤 Exported snapshot to {filename}")
    conn.close()
