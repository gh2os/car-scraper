import sqlite3
import csv
from datetime import datetime
from pathlib import Path


def daily_snapshot(db_path="data/listings.db", export_dir="output/snapshots"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    Path(export_dir).mkdir(parents=True, exist_ok=True)

    now = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{export_dir}/listings_{now}.csv"

    cursor.execute("""
        SELECT 
            source, external_id, title, price, mileage, location, link,
            first_seen, last_seen, days_on_market, is_delisted
        FROM listings
        ORDER BY price ASC
    """)

    rows = cursor.fetchall()
    headers = [desc[0] for desc in cursor.description]

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    print(f"📤 Exported snapshot to {filename}")
    conn.close()
