from crewai import Agent
from crewai_tools import CodeInterpreterTool
from ..tools.product_retriever import RunSQLOnBeautyProductsTable
from ..tools.product_schema_retriever import GetProductTableSchema
from ..tools.user_review_retriever import SemanticUserReviewRetriever


manager = Agent(
    role="Shop Manager",
    goal="Get the final SQL query which can be used to fetch products displayed to the user in frontend. The SQL query should be such that its helpful for the user in finding their needs.",
    backstory="You are the manager of a shop who is very smart. You help people find the right products for them that are available in your shop by providing the accurate sqlite3 query which should be used to get the tailored and relevant products.",
    tools=[RunSQLOnBeautyProductsTable(), GetProductTableSchema(), CodeInterpreterTool(), SemanticUserReviewRetriever()],
    verbose=True,
    allow_delegation=True,
    max_iter=2,
)
