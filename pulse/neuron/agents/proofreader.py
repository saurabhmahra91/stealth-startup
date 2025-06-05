from crewai import Agent
from crewai_tools import CodeInterpreterTool
from ..tools.product_retriever import RunSQLOnBeautyProductsTable


proofreader = Agent(
    role="Proofreader",
    goal="Help your manager by actually running the sql he has gotten so far and testing it. if it gives error, you report to your manager with the specific error",
    backstory="You are a software engineering tester who makes sure no wrong SQL query error is given to the user.",
    tools=[RunSQLOnBeautyProductsTable(), CodeInterpreterTool()],
    verbose=True,
    max_iter=5,
    allow_delegation=True,
)
