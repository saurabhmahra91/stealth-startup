import sqlite3
from pathlib import Path

from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class ReviewRetrieverInput(BaseModel):
    query: str = Field(description="The query to perform. This should be lexically close to your target documents")
    limit: int | None = Field(
        description="The maximum number of results to return. Defaults to 50 if not specified.", default=50
    )


class ReviewRetriever(BaseTool):
    name = "user_review_retriever"
    description = "Retrieves user reviews from the SQLite3 database using a lexical keyword search."
    args_schema: type[BaseModel] = ReviewRetrieverInput

    def __init__(self, db_path: Path, table_name: str, **kwargs):
        super().__init__(**kwargs)
        self.db_path = db_path
        self.table_name = table_name

    def _check_table_exists(self, cursor: sqlite3.Cursor):
        """
        Raises a ValueError if the specified table does not exist in the database.
        """
        cursor.execute(
            """
            SELECT name FROM sqlite_master WHERE type='table' AND name=?
        """,
            (self.table_name,),
        )
        return not cursor.fetchone()

    def _run(self, query: str, limit: int | None = 50):
        assert isinstance(query, str), "Search query provided is not a string!"
        if not isinstance(limit, int) or limit <= 0:
            limit = 10
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        if self._check_table_exists(cur):
            conn.close()
            raise ValueError(f"Table '{self.table_name}' does not exist in the database '{self.db_path}'.")

        keywords = query.strip().split()
        where_clauses = []
        params = []
        # Search in review fields: Reviewer, Age, Skin_Type, Product, Rating, Review
        for kw in keywords:
            clause = (
                "("
                + " OR ".join(
                    [
                        "Reviewer LIKE ?",
                        "Age LIKE ?",
                        "Skin_Type LIKE ?",
                        "Product LIKE ?",
                        "Rating LIKE ?",
                        "Review LIKE ?",
                    ]
                )
                + ")"
            )
            params.extend([f"%{kw}%"] * 6)
            where_clauses.append(clause)
        where_sql = " AND ".join(where_clauses)
        sql = f"""
            SELECT * FROM {self.table_name}
            WHERE {where_sql}
            LIMIT ?
        """
        cur.execute(sql, params + [limit])
        results = cur.fetchall()
        conn.close()

        if not results:
            return []

        output = []
        for row in results:
            output.append({k: row[k] for k in row})
        return output
