# German Housing Parser (Kleinanzeigen)

---

## About the Project
This is a modular, automated, and fault-tolerant web scraper designed to monitor the real estate market in Germany. The script connects to the popular online marketplace **Kleinanzeigen**, extracts apartment rental listings in Berlin, cleans the raw text data, transforms it into a clean format, and saves everything into a structured database.


## Current Features
* **Multi-Page Scraping (Pagination):** The script dynamically navigates through website pages (currently configured to scan up to 20 pages per run).
* **Safe Scraping Practices:** Integrated request delays (`time.sleep`) and realistic browser headers (`User-Agent`) prevent the script from triggering captchas or getting IP-banned.
* **Smart Data Cleaning:** Prices are automatically stripped of currency symbols (`€`), dots, and extra text (`VB`), converting them into clean floating-point numbers (`float`).
* **Error Prevention (Robustness):** * The code automatically detects and skips embedded ad banners masquerading as listings.
  * `try-except` blocks catch errors if a price field contains non-numeric text (e.g., *"Sдано"* / *"Soll"* or *"Exchange"*), preventing the script from crashing.
* **Duplicate Protection:** Thanks to unique constraints (`UNIQUE`) in the database schema, consecutive script runs will not create duplicate entries for already saved apartments.

---

## Technologies Used
* **Programming Language:** `Python 3.10+`
* **Scraping & HTML Parsing:** `Requests` (for downloading pages) and `BeautifulSoup4` (for DOM traversing and element extraction).
* **Database:** `SQLite3` (an embedded relational database for fast and reliable data storage).
* **Type Hinting:** `bs4.element.Tag` and `ResultSet` (for strict data structuring and better IDE autocomplete support).

---

## Future Roadmap
The project is actively developed, with the following powerful features planned next:
1. **Professional Logging (`logging`):** Replacing standard `print()` statements with structured event and error logging into a dedicated `parser.log` file.
2. **SQL Data Analytics:** Creating analytical scripts to query the database (calculating average housing prices by Berlin districts, filtering top deals).
3. **Configuration File (`config.json`):** Moving all configuration parameters (target URL, page limits, delays) into an external file to control the scraper without changing the source code.
