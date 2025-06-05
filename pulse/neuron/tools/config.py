import os
from pathlib import Path

PRODUCTS_DB_PATH = Path(os.environ.get("PRODUCTS_SQLITE3_DB_PATH", "../db.sqlite3"))
PRODUCTS_TABLE_NAME = os.environ.get("PRODUCTS_TABLE_NAME", "beauty_products")

REVIEWS_DB_PATH = Path(os.environ.get("REVIEWS_SQLITE3_DB_PATH", "../db.sqlite3"))
REVIEWS_TABLE_NAME = os.environ.get("REVIEWS_TABLE_NAME", "user_reviews")