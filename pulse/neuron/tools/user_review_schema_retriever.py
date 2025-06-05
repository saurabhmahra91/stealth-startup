import json
from pathlib import Path

from crewai.tools import BaseTool
from pydantic import BaseModel

from .config import REVIEWS_DB_PATH, REVIEWS_TABLE_NAME
from .utils import sqlite3_execute


class NoArgs(BaseModel):
    """
    Input schema for GetProductTableSchema tool.
    """


class GetUserReviewsTableSchema(BaseTool):
    name: str = "get_user_reviews_table_schema"
    description: str = "Retrieves the schema for the user_reviews table in the SQLite3 database."
    inputs: type[BaseModel] = NoArgs  # No inputs required

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _run(self) -> str:
        """
        Retrieves the schema for the beauty_products table.
        """
        rows = sqlite3_execute(f"PRAGMA table_info({REVIEWS_TABLE_NAME});", REVIEWS_DB_PATH)
        return json.dumps(rows)
