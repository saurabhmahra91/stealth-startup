from crewai import Agent
from crewai_tools import CodeInterpreterTool
from ..tools.product_retriever import RunSQLOnBeautyProductsTable
from ..tools.product_schema_retriever import GetProductTableSchema


product_matcher = Agent(
    role="Product Matcher",
    goal="Help the manager who has a natural language query for a listing products by providing a sql query that shows the relevant results.",
    backstory="You help your manager in finding finding the correct products by giving him a sql query that returns what users should get",
    tools=[RunSQLOnBeautyProductsTable(), GetProductTableSchema(), CodeInterpreterTool()],
    verbose=True,
    max_iter=5,
    allow_delegation=True,
)
