import sqlite3
from pathlib import Path


def sqlite3_execute(query: str, db_path: Path) -> list:
    """
    Executes a SQL query on the beauty_products table and returns the results.

    Args:
        query (str): The SQL query to execute.

    Returns:
        list[dict]: A list the results of the query.
    """
    connection: sqlite3.Connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    cursor: sqlite3.Cursor = connection.cursor()
    cursor.execute(query)
    rows: list = cursor.fetchall()
    connection.close()

    return [dict(row) for row in rows]