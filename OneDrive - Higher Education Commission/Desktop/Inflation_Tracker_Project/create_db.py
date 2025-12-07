import pandas as pd
import sqlite3
import os

excel_file = 'SPI-Monthly-Prices-1.xlsx'
db_file = 'inflation_tracker.db'

def create_database():
    # Read the excel file, skipping the first row (title)
    # Header is in the second row (index 1)
    df = pd.read_excel(excel_file, header=1)
    
    # Rename columns to match our desired schema
    # The dataframe will have columns based on the merged headers which might be messy.
    # It's safer to rename by index since we inspected the structure.
    
    # Current columns based on inspection:
    # 0: S. No.
    # 1: Description
    # 2: Unit
    # 3-19: Cities
    # 20: Avg Nov 25
    # 21: Avg Oct 25
    # 22: Avg Nov 24
    # 23: % change 1
    # 24: % change 2
    
    column_mapping = {
        df.columns[1]: 'item_name',
        df.columns[2]: 'unit',
        df.columns[3]: 'islamabad',
        df.columns[4]: 'rawalpindi',
        df.columns[5]: 'gujranwala',
        df.columns[6]: 'sialkot',
        df.columns[7]: 'lahore',
        df.columns[8]: 'faisalabad',
        df.columns[9]: 'sargodha',
        df.columns[10]: 'multan',
        df.columns[11]: 'bahawalpur',
        df.columns[12]: 'karachi',
        df.columns[13]: 'hyderabad',
        df.columns[14]: 'sukkur',
        df.columns[15]: 'larkana',
        df.columns[16]: 'peshawar',
        df.columns[17]: 'bannu',
        df.columns[18]: 'quetta',
        df.columns[19]: 'khuzdar',
        df.columns[20]: 'avg_price_nov_25',
        df.columns[21]: 'avg_price_oct_25',
        df.columns[22]: 'avg_price_nov_24',
        df.columns[23]: 'change_nov_25_oct_25',
        df.columns[24]: 'change_nov_25_nov_24'
    }
    
    # Select only the columns we need (skip S. No.)
    selected_columns = list(column_mapping.keys())
    df_clean = df[selected_columns].rename(columns=column_mapping)
    
    # Clean up data: replace non-numeric values with None (NULL in SQL) for price columns
    price_cols = [
        'islamabad', 'rawalpindi', 'gujranwala', 'sialkot', 'lahore', 'faisalabad', 
        'sargodha', 'multan', 'bahawalpur', 'karachi', 'hyderabad', 'sukkur', 
        'larkana', 'peshawar', 'bannu', 'quetta', 'khuzdar', 
        'avg_price_nov_25', 'avg_price_oct_25', 'avg_price_nov_24', 
        'change_nov_25_oct_25', 'change_nov_25_nov_24'
    ]
    
    for col in price_cols:
        df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
    
    # Connect to SQLite database
    if os.path.exists(db_file):
        os.remove(db_file) # Start fresh
        
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # Create table
    create_table_sql = """
    CREATE TABLE monthly_prices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT,
        unit TEXT,
        islamabad REAL,
        rawalpindi REAL,
        gujranwala REAL,
        sialkot REAL,
        lahore REAL,
        faisalabad REAL,
        sargodha REAL,
        multan REAL,
        bahawalpur REAL,
        karachi REAL,
        hyderabad REAL,
        sukkur REAL,
        larkana REAL,
        peshawar REAL,
        bannu REAL,
        quetta REAL,
        khuzdar REAL,
        avg_price_nov_25 REAL,
        avg_price_oct_25 REAL,
        avg_price_nov_24 REAL,
        change_nov_25_oct_25 REAL,
        change_nov_25_nov_24 REAL
    );
    """
    cursor.execute(create_table_sql)
    
    # Insert data
    df_clean.to_sql('monthly_prices', conn, if_exists='append', index=False)
    
    print(f"Database {db_file} created successfully with {len(df_clean)} records.")
    
    # Verify
    cursor.execute("SELECT COUNT(*) FROM monthly_prices")
    count = cursor.fetchone()[0]
    print(f"Verified count: {count}")
    
    conn.close()

if __name__ == "__main__":
    create_database()
