# Car Listings Scraper

This project is a web scraper for used car listings from AutoTrader.ca. It collects data on specific car models and stores it in an SQLite database.

## Setup Instructions

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/car-listings-scraper.git
   cd car-listings-scraper
   ```

2. **Set up Python environment:**

   Ensure you have Python 3.11 installed. You can use `pyenv` or another version manager to install it.

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Playwright:**

   Install Playwright browsers:

   ```bash
   playwright install
   ```

5. **Initialize the SQLite database:**

   The database will be automatically set up when you run the scraper for the first time.

## Running Locally

To run the scraper locally, execute:

```bash
python main.py
```

This will scrape the specified websites and update the `data/listings.db` SQLite database with the latest listings.

## GitHub Actions Automation

The project includes a GitHub Actions workflow that automates the scraping process. The workflow is scheduled to run daily at 6am UTC. It performs the following steps:

1. Checks out the repository.
2. Sets up Python 3.11.
3. Installs dependencies and Playwright.
4. Runs the scraper.
5. Commits and pushes any changes to the `data/listings.db` database if new or updated listings are found.

This ensures that the database is kept up-to-date with the latest car listings.

## SQLite Usage

The scraper stores data in an SQLite database located at `data/listings.db`. The database schema includes a `listings` table with fields for the car details and timestamps for when the listing was first and last seen.

You can query the database using any SQLite-compatible tool or library to analyze the collected data.
