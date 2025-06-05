import sqlite3
from pathlib import Path

from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from .config import REVIEWS_DB_PATH, REVIEWS_TABLE_NAME


class LexicalUserReviewSearchInput(BaseModel):
    """
    Input schema for LexicalUserReviewSearch tool.
    """
    product_like: str = Field(description="The search term to search in the product column")
    review_like: str = Field(description="The search term to search in the review column")
    age_min: int = Field(description="The minimum age of user's age range for filetering rows")
    age_max: int = Field(description="The maxium age of user's age range for filtering rows")
    skin_type_like: str = Field(description="The search term to search in the skin_type column")


class LexicalUserReviewSearch(BaseTool):
    name: str = "lexical_user_review_retriever"
    description: str = "Retrieves user reviews from the SQLite3 database using lexical search"
    args_schema: type[BaseModel] = LexicalUserReviewSearchInput

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _check_table_exists(self, cursor: sqlite3.Cursor):
        """
        Raises a ValueError if the specified table does not exist in the database.
        """
        cursor.execute(
            """
            SELECT name FROM sqlite_master WHERE type='table' AND name=?
        """,
            (REVIEWS_TABLE_NAME,),
        )
        return not cursor.fetchone()

    def _run(self, product_like: str, review_like: str, age_min: int, age_max: int, skin_type_like: str):
        conn = sqlite3.connect(REVIEWS_DB_PATH)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        if self._check_table_exists(cur):
            conn.close()
            raise ValueError(f"Table '{REVIEWS_TABLE_NAME}' does not exist in the database '{REVIEWS_DB_PATH}'.")

        query = f"""
            SELECT * FROM {REVIEWS_TABLE_NAME}
            WHERE LOWER(product) LIKE LOWER(?)
            AND LOWER(review) LIKE LOWER(?)
            AND age BETWEEN ? AND ?
            AND LOWER(skin_type) LIKE LOWER(?)
        """
        params = [
            f"%{product_like}%",
            f"%{review_like}%",
            age_min,
            age_max,
            f"%{skin_type_like}%",
        ]

        cur.execute(query, params)
        rows = cur.fetchall()
        conn.close()

        return [{k: row[k] for k in row.keys()} for row in rows] if rows else []


class SemanticUserReviewRetrieverInput(BaseModel):
    query: str = Field(description="The query string to search relevant documents for")


class SemanticUserReviewRetriever(BaseTool):
    name: str = "semantic_user_review_retriever"
    description: str = "Retrieves user reviews from the using semantic search"
    args_schema: type[BaseModel] = SemanticUserReviewRetrieverInput

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _run(self, query: str):
        from .semantic_search.search import search
        return search(query=query, k=50)
