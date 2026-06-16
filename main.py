from bs4.element import Tag
import requests
import sqlite3
from bs4 import BeautifulSoup, ResultSet
import time
import json
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("parser.log", encoding="utf-8"),   # Пишем в файл
        logging.StreamHandler()                                # Дублируем в консоль
    ]
)


def init_db(db_name):
    connect = sqlite3.connect(db_name)  #подкл бд
    cursor = connect.cursor()

    cursor.execute(
    """
        CREATE TABLE IF NOT EXISTS apartmens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            price REAL,
            address TEXT,
            link TEXT UNIQUE
            )
    """
    )

    return connect, cursor



def get_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",  # Якобы наш браузер настроен на немецкий язык
    }

    response = requests.get(url, headers=headers)
    return response.text



def main():
    config = load_config()
    connect, cursor = init_db(config["database_name"])


    for page in range(1, config["max_pages"] + 1):

        current_url = config["base_url"].format(page=page)
        html = get_html(current_url)
        soup = BeautifulSoup(html, "html.parser")

        apartments: ResultSet[Tag] = soup.find_all("article", class_="aditem")


        for apartment in apartments:
            title_element = apartment.find("a", class_="ellipsis")
            if title_element is None:
                continue

            title = title_element.text.strip()
            apartment_url = title_element["href"]
            full_link = "https://www.kleinanzeigen.de" + apartment_url

            raw_price = apartment.find("p", class_="aditem-main--middle--price-shipping--price").text.strip()
            try:
                clean_price = raw_price.replace("€", "").replace(".", "").strip().replace("VB", "")
                new_price = float(clean_price)
            except ValueError:
                logging.warning(f"Failed to convert the price to a number: '{raw_price}'. Setting to 0.0")
                new_price = 0.0

            address = apartment.find("div", class_="aditem-main--top--left").text.strip()

            cursor.execute(
                "INSERT OR IGNORE INTO apartmens (title, price, address, link) VALUES (?, ?, ?, ?)",
                (title, new_price, address, full_link)
            )

            logging.info(f"apartment: {title} | price: {new_price} | address: {address} | link: {full_link}")
        
        logging.info(f"Waiting before the next page...")
        time.sleep(config["sleep_time"])


    connect.commit()
    connect.close()
    logging.info(f"Done!")


if __name__ == "__main__":
    main()