import json
import os
import logging
from datetime import datetime

import json
import os
import re
from datetime import datetime


def clean_autotrader_data(input_path="output/autotrader_raw.json", output_path="output/autotrader_clean.json"):
    with open(input_path, "r") as f:
        raw_listings = json.load(f)

    seen_links = set()
    cleaned = []
    scraped_at = datetime.utcnow().isoformat()

    for listing in raw_listings:
        link = listing.get("link")
        if not link or link in seen_links:
            continue
        seen_links.add(link)

        # Extract external_id from URL if missing
        external_id = listing.get("external_id")
        if not external_id and link:
            match = re.search(r'/5_(\d+)', link)
            if match:
                external_id = match.group(1)

        # Normalize price
        try:
            price = int(listing["price"].replace("$", "").replace(
                ",", "")) if listing["price"] else None
        except Exception:
            price = None

        # Normalize mileage
        try:
            mileage = int(listing["mileage"].replace("KM", "").replace(
                ",", "").strip()) if listing["mileage"] else None
        except Exception:
            mileage = None

        cleaned.append({
            "source": listing.get("source", "autotrader"),
            "external_id": external_id,
            "title": listing.get("title"),
            "price": price,
            "mileage": mileage,
            "location": listing.get("location"),
            "link": link,
            "scraped_at": scraped_at
        })

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(cleaned, f, indent=2)

    print(f"✅ Cleaned {len(cleaned)} listings and saved to {output_path}")
    return cleaned
