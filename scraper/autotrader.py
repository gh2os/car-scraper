from playwright.async_api import async_playwright

import asyncio

async def scrape_autotrader():
    base_url = "https://www.autotrader.ca/cars/"
    search_params = [
        {"make": "Mazda", "model": "CX-5", "year_from": 2013, "year_to": 2015},
        {"make": "Toyota", "model": "RAV4", "year_from": 2013, "year_to": 2015},
        {"make": "Honda", "model": "CR-V", "year_from": 2013, "year_to": 2015},
    ]
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        listings = []
        
        for params in search_params:
            url = f"{base_url}{params['make']}/{params['model']}/{params['year_from']}-{params['year_to']}/"
            await page.goto(url)
            await page.wait_for_load_state('networkidle')
            
            for listing in await page.query_selector_all('div.result-item'):
                title = await listing.query_selector('h2.title').inner_text()
                price = await listing.query_selector('span.price').inner_text()
                price = price.replace('$', '').replace(',', '')
                mileage = await listing.query_selector('div.mileage').inner_text()
                mileage = mileage.replace(' km', '').replace(',', '')
                location = await listing.query_selector('div.location').inner_text()
                link = await listing.query_selector('a.result-title').get_attribute('href')
                
                listing_data = {
                    "title": title,
                    "price": int(price) if price.isdigit() else None,
                    "mileage": int(mileage) if mileage.isdigit() else None,
                    "location": location,
                    "link": f"https://www.autotrader.ca{link}",
                    "external_id": link.split('/')[-1],  # Assuming the last part of the link is a unique ID
                    "source": "AutoTrader"
                }
                insert_or_update_listing(listing_data)
                listings.append(listing_data)
        
        await browser.close()
    
    return listings

# To run the async function
if __name__ == "__main__":
    asyncio.run(scrape_autotrader())
