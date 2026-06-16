import sqlite3
import json


def load_config():
    with open("config.json", "r") as file:
        config = json.load(file)
        return config
    

def run_analytics():
    config = load_config()
    # database connection
    connect = sqlite3.connect(config["database_name"])
    cursor = connect.cursor()

    print("=" * 50)
    print("ANALYTICS OF THE REAL ESTATE MARKET (BERLIN)")
    print("=" * 50)

    # How many listings are in the database
    cursor.execute("SELECT COUNT(*) FROM apartmens")
    total_apartments = cursor.fetchone()[0]
    print(f"Total apartments in database: {total_apartments}")

    # Average, maximum, and minimum price (excluding fake 0.0 prices)
    cursor.execute("SELECT AVG(price), MIN(price), MAX(price) FROM apartmens WHERE price > 0")
    avg_price, min_price, max_price = cursor.fetchone()
    if avg_price:
        print(f"Average rental cost: {avg_price:.2f} €")
        print(f"The cheapest apartment: {min_price:.2f} €")
        print(f"The most expensive apartment: {max_price:.2f} €")
    
    # How many listings were filtered out without a price (with a value of 0.0)
    cursor.execute("SELECT COUNT(*) FROM apartmens WHERE price = 0")
    zero_prices = cursor.fetchone()[0]
    print(f"Listings with hidden/non-standard pricing (0.0): {zero_prices}")

    print("-" * 50)
    print("Top 5 best deals (price > 200€)")
    print("-" * 50)

    # Display the 5 cheapest apartments and remove options cheaper than €200
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