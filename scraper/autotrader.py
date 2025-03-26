import requests
from bs4 import BeautifulSoup

def scrape_autotrader():
    print("Scraping AutoTrader...")
    base_url = "https://www.autotrader.ca/cars/"
    search_params = [
        {"make": "Mazda", "model": "CX-5", "year_from": 2013, "year_to": 2015},
        {"make": "Toyota", "model": "RAV4", "year_from": 2013, "year_to": 2015},
        {"make": "Honda", "model": "CR-V", "year_from": 2013, "year_to": 2015},
    ]
    
    listings = []
    
    for params in search_params:
        url = f"{base_url}{params['make']}/{params['model']}/{params['year_from']}-{params['year_to']}/"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        for listing in soup.find_all('div', class_='result-item'):
            title = listing.find('h2', class_='title').get_text(strip=True)
            price = listing.find('span', class_='price').get_text(strip=True).replace('$', '').replace(',', '')
            mileage = listing.find('div', class_='mileage').get_text(strip=True).replace(' km', '').replace(',', '')
            location = listing.find('div', class_='location').get_text(strip=True)
            link = listing.find('a', class_='result-title')['href']
            
            listings.append({
                "title": title,
                "price": int(price) if price.isdigit() else None,
                "mileage": int(mileage) if mileage.isdigit() else None,
                "location": location,
                "link": f"https://www.autotrader.ca{link}"
            })
    
    return listings
