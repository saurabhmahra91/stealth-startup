"""
This script ingests user review data from a CSV file into a SQLite database.

The main function, `ingest_user_reviews`, reads a CSV file containing user reviews,
cleans the column names, creates (or replaces) a `user_reviews` table in the specified SQLite database,
and inserts all the data from the CSV. Existing data in the table is removed before new data is inserted.

Example usage:
    ingest_user_reviews(Path('verified_reviews.csv'), Path('db.sqlite3'))

CSV columns expected:
    - Reviewer (TEXT)
    - Age_and_Skin_Type (TEXT)
    - Product (TEXT)
    - Rating (TEXT)
    - Review (TEXT)
"""

from pathlib import Path
import csv
import sqlite3


def ingest_user_reviews(csv_path: Path, db_path: Path):
    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)
        # Clean column names (remove spaces and special characters)
        columns = [
            col.strip().replace(" ", "_").replace("/", "_").replace("%", "pct").replace("&", "and").replace("-", "_")
            for col in headers
        ]
        rows = [row for row in reader]

    conn: sqlite3.Connection = sqlite3.connect(db_path)
    cursor: sqlite3.Cursor = conn.cursor()

    # Create table (if not exists)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_reviews (
            Reviewer TEXT,
            Age TEXT,
            Skin_Type TEXT,
            Product TEXT,
            Rating TEXT,
            Review TEXT
        )
    """)

    # Remove all existing data (to mimic 'replace' behavior)
    cursor.execute("DELETE FROM user_reviews")

    # Prepare insert statement
    placeholders = ",".join(["?"] * len(columns))
    insert_sql = f"INSERT INTO user_reviews ({','.join(columns)}) VALUES ({placeholders})"

    # Insert data into the table
    cursor.executemany(insert_sql, rows)

    # Commit and close
    conn.commit()
    conn.close()


if __name__ == "__main__":
    # Example usage:
    ingest_user_reviews(Path("verified_reviews.csv"), Path("db.sqlite3"))
