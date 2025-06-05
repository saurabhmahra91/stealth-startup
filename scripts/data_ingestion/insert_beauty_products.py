"""
This script provides a function to ingest beauty product data from a CSV file into a SQLite database.

The main function, `ingest_beauty_products`, reads a CSV file containing beauty product information,
cleans the column names, creates (or replaces) a `beauty_products` table in the specified SQLite database,
and inserts all the data from the CSV. Existing data in the table is removed before new data is inserted.

Example usage:
    ingest_beauty_products(Path('input.csv'), Path('output.db'))

CSV columns expected:
    - product_id (TEXT, primary key)
    - name (TEXT)
    - category (TEXT)
    - description (TEXT)
    - top_ingredients (TEXT)
    - tags (TEXT)
    - price_USD (REAL)
    - margin (REAL)
"""

import csv
import sqlite3
from pathlib import Path


def ingest_beauty_products(csv_path: Path, db_path: Path):
    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)
        # Clean column names (remove spaces and special characters)
        columns = [col.strip().replace(" ", "_").replace("(", "").replace(")", "") for col in headers]
        rows = [row for row in reader]

    conn: sqlite3.Connection = sqlite3.connect(db_path)
    cursor: sqlite3.Cursor = conn.cursor()

    # Create table (if not exists)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS beauty_products (
            product_id TEXT PRIMARY KEY,
            name TEXT,
            category TEXT,
            description TEXT,
            top_ingredients TEXT,
            tags TEXT,
            usd_price REAL,
            margin REAL
        )
    """)

    # Remove all existing data (to mimic 'replace' behavior)
    cursor.execute("DELETE FROM beauty_products")

    # Prepare insert statement
    placeholders = ",".join(["?"] * len(columns))
    insert_sql = f"INSERT INTO beauty_products ({','.join(columns)}) VALUES ({placeholders})"

    # Insert data into the table
    cursor.executemany(insert_sql, rows)

    # Commit and close
    conn.commit()
    conn.close()


if __name__ == "__main__":
    # Example usage:
    ingest_beauty_products(Path("pulse/neuron/skincare catalog.csv"), Path("db.sqlite3"))
