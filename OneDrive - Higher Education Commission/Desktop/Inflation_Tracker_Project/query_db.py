import sqlite3
import pandas as pd

def query_database():
    db_file = 'inflation_tracker.db'
    conn = sqlite3.connect(db_file)
    
    print("--- 1. List first 5 items and their prices in Islamabad ---")
    query1 = "SELECT item_name, unit, islamabad FROM monthly_prices LIMIT 5"
    df1 = pd.read_sql_query(query1, conn)
    print(df1.to_string(index=False))
    print("\n")

    print("--- 2. Find items with more than 10% price increase (Nov 25 vs Oct 25) ---")
    # Note: Column names were cleaned in create_db.py. 
    # 'change_nov_25_oct_25' holds the percentage change.
    query2 = "SELECT item_name, change_nov_25_oct_25 FROM monthly_prices WHERE change_nov_25_oct_25 > 10"
    df2 = pd.read_sql_query(query2, conn)
    if not df2.empty:
        print(df2.to_string(index=False))
    else:
        print("No items found with > 10% increase.")
    print("\n")

    print("--- 3. Compare Average Price Nov 25 vs Nov 24 for 'Wheat Flour Bag' ---")
    query3 = "SELECT item_name, avg_price_nov_25, avg_price_nov_24 FROM monthly_prices WHERE item_name LIKE '%Wheat Flour%'"
    df3 = pd.read_sql_query(query3, conn)
    print(df3.to_string(index=False))
    
    conn.close()

if __name__ == "__main__":
    query_database()
