import json
import os
import logging
from datetime import datetime


def clean_autotrader_data(input_path=None, output_path=None, timestamp=None):
    if timestamp is None:
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    if input_path is None:
        input_path = f"output/autotrader_raw_{timestamp}.json"
    if output_path is None:
        output_path = f"output/autotrader_clean_{timestamp}.json"
    with open(input_path, "r") as f:
        raw_listings = json.load(f)

    cleaned = []
    for listing in raw_listings:
        try:
            price = int(listing["price"].replace("$", "").replace(
                ",", "")) if listing["price"] else None
        except:
            price = None

        try:
            mileage = int(listing["mileage"].replace("KM", "").replace(
                ",", "").strip()) if listing["mileage"] else None
        except:
            mileage = None

        listing["scraped_at"] = datetime.utcnow().isoformat()
        cleaned.append({
            "source": listing["source"],
            "external_id": listing["external_id"],
            "title": listing["title"],
            "price": price,
            "mileage": mileage,
            "location": listing["location"],
            "link": listing["link"]
        })

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(cleaned, f, indent=2)

    print(f"Cleaned {len(cleaned)} listings and saved to {output_path}")
    logging.info(f"Output path: {output_path}")
    return cleaned
