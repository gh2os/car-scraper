import json
import os


def clean_autotrader_data(input_path="output/autotrader_raw.json", output_path="output/autotrader_clean.json"):
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
    return cleaned
