import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


def scrape_autotrader():
    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = uc.Chrome(options=options)
    driver.set_window_size(1200, 800)

    url = "https://www.autotrader.ca/cars/mazda/cx-5/bc/vancouver/?rcp=15&rcs=0&yRng=2013%2C2017"
    driver.get(url)

    time.sleep(10)  # Let page load fully

    listings = driver.find_elements(By.CSS_SELECTOR, "div.result-item")

    for listing in listings:
        try:
            title = listing.find_element(By.CSS_SELECTOR, "h2.title").text
            price = listing.find_element(
                By.CSS_SELECTOR, "span.price-amount").text
            mileage = listing.find_element(
                By.CSS_SELECTOR, "div.kilometers").text
            location = listing.find_element(
                By.CSS_SELECTOR, "div.location").text
            link = listing.find_element(
                By.CSS_SELECTOR, "a.result-title").get_attribute("href")

            print({
                "title": title,
                "price": price,
                "mileage": mileage,
                "location": location,
                "link": f"https://www.autotrader.ca{link}"
            })

        except Exception as e:
            print("Error parsing listing:", e)

    driver.quit()


if __name__ == "__main__":
    scrape_autotrader()
