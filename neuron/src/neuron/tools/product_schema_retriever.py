import json
from pathlib import Path

from crewai.tools import BaseTool
from pydantic import BaseModel

from .config import PRODUCTS_TABLE_NAME
from .utils import sqlite3_execute


class NoArgs(BaseModel):
    """
    Input schema for GetProductTableSchema tool.
    """


class GetProductTableSchema(BaseTool):
    name: str = "get_product_table_schema"
    description: str = "Retrieves the schema for the beauty_products table in the SQLite3 database."
    inputs: type[BaseModel] = NoArgs  # No inputs required

    def __init__(self, db_path: Path, **kwargs):
        super().__init__(**kwargs)
        self.db_path = db_path
        self.table_name = PRODUCTS_TABLE_NAME

    def _run(self) -> str:
        """
        Retrieves the schema for the beauty_products table.
        """
        rows = sqlite3_execute(f"PRAGMA table_info({self.table_name});", self.db_path)
        return json.dumps(rows)
