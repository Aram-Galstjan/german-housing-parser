import sqlite3
import json


def load_config():
    with open("config.json", "r") as file:
        config = json.load(file)
        return config
    

def run_analytics():
    config = load_config()
    # Подключаемся к той базе, которая указана в конфиге
    connect = sqlite3.connect(config["database_name"])
    cursor = connect.cursor()

    print("=" * 50)
    print("ANALYTICS OF THE REAL ESTATE MARKET (BERLIN)")
    print("=" * 50)

    # 1. Сколько всего объявлений в базе
    cursor.execute("SELECT COUNT(*) FROM apartmens")
    total_apartments = cursor.fetchone()[0]
    print(f"Total apartments in database: {total_apartments}")

    # 2. Средняя, максимальная и минимальная цена (исключая фейковые цены 0.0)
    cursor.execute("SELECT AVG(price), MIN(price), MAX(price) FROM apartmens WHERE price > 0")
    avg_price, min_price, max_price = cursor.fetchone()
    if avg_price:
        print(f"Average rental cost: {avg_price:.2f} €")
        print(f"The cheapest apartment: {min_price:.2f} €")
        print(f"The most expensive apartment: {max_price:.2f} €")
    
    # 3. Сколько объявлений отсеялось без цены (со значением 0.0)
    cursor.execute("SELECT COUNT(*) FROM apartmens WHERE price = 0")
    zero_prices = cursor.fetchone()[0]
    print(f"Listings with hidden/non-standard pricing (0.0): {zero_prices}")

    print("-" * 50)
    print("Top 5 best deals (price > 200€)")
    print("-" * 50)

    # 4. Выводим 5 самых дешёвых квартир (но отсекаем подозрительные варианты дешевле 200€)
    cursor.execute("""
        SELECT title, price, link 
        FROM apartmens 
        WHERE price > 200 
        ORDER BY price ASC 
        LIMIT 5
    """)
    top_deals = cursor.fetchall()
    for idx, (title, price, link) in enumerate(top_deals, 1):
        print(f"{idx}. [{price} €] {title[:40]}...")
        print(f"Link: {link}\n")

    connect.close()

if __name__ == "__main__":
    run_analytics()