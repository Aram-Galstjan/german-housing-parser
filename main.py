from bs4.element import Tag
import requests
import sqlite3
from bs4 import BeautifulSoup, ResultSet
import time


def init_db():
    connect = sqlite3.connect("apartments.db")  #подкл бд
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
    connect, cursor = init_db()


    for page in range(1, 41):

        current_url = f"https://www.kleinanzeigen.de/s-wohnung-mieten/berlin/seite:{page}/c203l3331"
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
                print(f"[WARNING] Не удалось перевести цену в число: '{raw_price}'. Ставим 0.0")
                new_price = 0.0

            address = apartment.find("div", class_="aditem-main--top--left").text.strip()

            cursor.execute(
                "INSERT OR IGNORE INTO apartmens (title, price, address, link) VALUES (?, ?, ?, ?)",
                (title, new_price, address, full_link)
            )

            print(f"apartment: {title} | clean price: {new_price} | address: {address} | link: {full_link}")
        
        print("[INFO] Ожидание перед следующей страницей...")
        time.sleep(2)


    connect.commit()
    connect.close()
    print(f"apartment: {title} | price: {new_price} | address: {address} | link: {full_link}")


if __name__ == "__main__":
    main()