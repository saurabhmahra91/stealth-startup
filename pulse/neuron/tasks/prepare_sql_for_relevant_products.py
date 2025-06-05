from crewai import Task

from ..agents.manager import manager
from ..tools.config import PRODUCTS_DB_PATH
from ..tools.product_retriever import RunSQLOnBeautyProductsTable
from ..tools.product_schema_retriever import GetProductTableSchema

prepare_sql_for_relevant_products = Task(
    description="""
        1. Interpret the query you have received.
        2. Prepare intelligent SQL query and execute it to retrieve relevant SKUs from the beauty_products table.
        3. Retry and refine query up to 4 times if needed.
        4. Retrieve up to 50 matching SKUs.
        5. Generate a brief justification for the selected products.
    """,
    expected_output="""
        Three things --
        1. The SQL query (without LIMIT)
        2. Reasoning for product selection
        3. Sample products (with LIMIT)
    """,
    agent=manager,
    tools=[
        RunSQLOnBeautyProductsTable(db_path=PRODUCTS_DB_PATH),
        GetProductTableSchema(db_path=PRODUCTS_DB_PATH),
    ],
    output_file="get_relevant_products.md"
)
