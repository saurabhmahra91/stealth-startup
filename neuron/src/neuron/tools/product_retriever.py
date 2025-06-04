import json

from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from pathlib import Path
from .config import PRODUCTS_TABLE_NAME
from .utils import sqlite3_execute
import sqlite3


class ProductRetrieverArgs(BaseModel):
    """
    Input schema for GetProductTableSchema tool.
    """
    query: str = Field(description="The SQLite3 query to run. This should be a valid sqlite3 query.")


class RunSQLOnBeautyProductsTable(BaseTool):
    name: str = "run_sql_query_on_beauty_products_table"
    description: str = "Retrieves beauty product information from the SQLite3 database using a SQL query."

    inputs: type[BaseModel] = ProductRetrieverArgs

    def __init__(self, db_path: Path, **kwargs):
        super().__init__(**kwargs)
        self.table_name = PRODUCTS_TABLE_NAME
        self.name = f"run_sql_queries_on_table_{self.table_name}"
        self.db_path = db_path

    def _check_table_exists(self) -> bool:
        """
        Raises a ValueError if the specified table does not exist in the database.
        """
        return _check_table_exists(self.db_path, self.table_name)

    def forward(self, query: str) -> str:
        assert isinstance(query, str), "SQL query provided is not a string!"

        if self._check_table_exists():
            raise ValueError(f"Table '{self.table_name}' does not exist in the database '{self.db_path}'.")

        conn: sqlite3.Connection = sqlite3.connect(self.db_path)
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