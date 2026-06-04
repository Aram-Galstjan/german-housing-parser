import requests
import sqlite3
from bs4 import BeautifulSoup

connect = sqlite3.connect("books.db")  #подкл бд
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


connect.commit()


url = "https://www.kleinanzeigen.de/s-wohnung-mieten/berlin/c203l3331"


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",  # Якобы наш браузер настроен на немецкий язык
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

apartments = soup.find_all("article", class_="aditem")

all_apartments = []

for apartment in apartments:
    title = apartment.find("a", class_="ellipsis").text.strip()

    apartment_url = apartment.find("a", class_="ellipsis")["href"] 

    full_link = "https://www.kleinanzeigen.de" + apartment_url

    raw_price = apartment.find("p", class_="aditem-main--middle--price-shipping--price").text.strip()

    clean_price = raw_price.replace("€", "").replace(".", "").strip().replace("VB", "")

    new_price = float(clean_price)

    address = apartment.find("div", class_="aditem-main--top--left").text.strip()

    cursor.execute(
        "INSERT OR IGNORE INTO apartmens (title, price, address, link) VALUES (?, ?, ?, ?)",
        (title, new_price, address, full_link)
    )

    print(f"apartment: {title} | clean price: {new_price} | address: {address} | link: {full_link}")


connect.commit()

connect.close()
