# German Housing Parser (Kleinanzeigen)

## Overview
This project is a Python web scraper that collects apartment listings from **Kleinanzeigen (Germany)**, specifically focusing on Berlin rentals.
It extracts key information such as title, price, address, and saves everything into a local SQLite database for later use or analysis.
The goal of this project is to practice real-world web scraping, data cleaning, and working with structured storage.

## Features

- Multi-page scraping (pagination support)
-  Web requests with custom headers (to mimic real browser behavior)
-  Data cleaning (price normalization, text formatting)
-  SQLite database storage
-  Duplicate protection using UNIQUE constraints (no duplicate listings)
-  Basic error handling for missing or invalid data
-  Request delay to reduce risk of blocking

## Example of extracted data

Title: 2-Zimmer Wohnung in Kreuzberg
Price: 850.0
Address: Berlin Kreuzberg
Link: https://www.kleinanzeigen.de/

## Technologies Used

- Python 3.10+
- requests
- BeautifulSoup4
- sqlite3
- json
- time

## Project Structure

project/
│── main.py
│── config.json
│── apartments.db
│── README.md

## Future Improvements

- Add logging system (logging module)
- Improve error handling for network issues (timeouts, retries)
- Move more settings into config.json (fully configurable scraper)
- Add simple analytics (average prices per area)
- Export data to CSV / JSON format

## What I learned from this project

- How to work with HTML structure and extract data using BeautifulSoup
- How to handle real-world messy web data
- How to store structured data using SQLite
- How to debug scraping issues (missing elements, invalid prices)
- Basics of building a modular Python project
