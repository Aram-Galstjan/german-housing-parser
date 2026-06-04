import requests
import sqlite3
from bs4 import BeautifulSoup

url = "https://www.kleinanzeigen.de/s-wohnung-mieten/berlin/c203l3331"


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",  # Якобы наш браузер настроен на немецкий язык
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

apartments = soup.find_all("article", class_="aditem")

print(response.status_code)  # Проверяем статус ответа