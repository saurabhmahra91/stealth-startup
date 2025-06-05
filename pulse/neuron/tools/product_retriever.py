import json
import sqlite3
from pathlib import Path

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from .config import PRODUCTS_TABLE_NAME, PRODUCTS_DB_PATH


class ProductRetrieverArgs(BaseModel):
    """
    Input schema for GetProductTableSchema tool.
    """
    query: str = Field(description="The SQLite3 query to run. This should be a valid sqlite3 query.")


class RunSQLOnBeautyProductsTable(BaseTool):
    name: str = "run_sql_query_on_beauty_products_table"
    description: str = "Retrieves beauty product information from the SQLite3 database using a SQL query."

    inputs: type[BaseModel] = ProductRetrieverArgs

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _check_table_exists(self) -> bool:
        """
        Raises a ValueError if the specified table does not exist in the database.
        """
        return _check_table_exists(PRODUCTS_DB_PATH, PRODUCTS_TABLE_NAME)

    def _run(self, query: str) -> str:
        assert isinstance(query, str), "SQL query provided is not a string!"

        if self._check_table_exists():
            raise ValueError(f"Table '{PRODUCTS_TABLE_NAME}' does not exist in the database '{PRODUCTS_DB_PATH}'.")

        conn: sqlite3.Connection = sqlite3.connect(PRODUCTS_DB_PATH)
        conn.row_factory = sqlite3.Row
        cur: sqlite3.Cursor = conn.cursor()
        cur.execute(query)
        rows: list = cur.fetchall()
        return json.dumps([dict(row) for row in rows])


def _check_table_exists(db_path: Path, table_name: str):
    """
    Raises a ValueError if the specified table does not exist in the database.
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute(
        """
        SELECT name FROM sqlite_master WHERE type='table' AND name=?
    """,
        (table_name,),
    )

    return not cur.fetchone()