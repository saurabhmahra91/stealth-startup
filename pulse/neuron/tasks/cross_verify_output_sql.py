from crewai import Task

from ..agents.proofreader import proofreader
from ..tools.config import PRODUCTS_DB_PATH
from ..tools.product_retriever import RunSQLOnBeautyProductsTable
from ..tools.product_schema_retriever import GetProductTableSchema

cross_verify_output_sql = Task(
    description="""
        Validate the final SQLite query by executing it with LIMIT 1 to check for correctness.
    """,
    expected_output="""
        Either "SQLIte Query OK" or "SQLite Query BAD" with the error
    """,
    agent=proofreader,
    tools=[
        RunSQLOnBeautyProductsTable(db_path=PRODUCTS_DB_PATH),
        GetProductTableSchema(db_path=PRODUCTS_DB_PATH),
    ],
    output_file="cross_verification.md"
)
