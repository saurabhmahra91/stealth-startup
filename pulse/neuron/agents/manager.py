from crewai import Agent
from crewai_tools import CodeInterpreterTool
from ..tools.product_retriever import RunSQLOnBeautyProductsTable
from ..tools.product_schema_retriever import GetProductTableSchema


manager = Agent(
    role="Shop Manager",
    goal="Use the different agents to get the final SQL query which can be used to fetch products displayed to the user in frontend.",
    backstory="You are the manager of a shop who is very smart and coordinates the overall agent workflow. You help people find the right products for them that are available in your shop by providing the accurate sqlite3 query which should be used to get the tailored and relevant products. You have multiple agents that help you with the task.",
    tools=[RunSQLOnBeautyProductsTable(), GetProductTableSchema(), CodeInterpreterTool()],
    verbose=True,
    allow_delegation=True,
    max_iter=2,
)
