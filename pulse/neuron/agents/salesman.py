from crewai import Agent
from crewai_tools import CodeInterpreterTool

from ..tools.product_retriever import RunSQLOnBeautyProductsTable
from ..tools.product_schema_retriever import GetProductTableSchema
from ..tools.user_review_retriever import SemanticUserReviewRetriever

salesman = Agent(
    role="SalesAgent",
    goal="Help the manager in enhancing the results that he's going to show to the user by providing him historical user reviews that are somewhat similar to current users requirements.",
    backstory="You are very experienced salesman and has information of user feedbacks on different product that your shop sells. These users reviews are a great resource because if a user with a particular attribute had some experience with a particular kind of product, you can use this information to enhance products to a new user.",
    tools=[RunSQLOnBeautyProductsTable(), GetProductTableSchema(), SemanticUserReviewRetriever(), CodeInterpreterTool()],
    max_iter=5,
    verbose=True,
    allow_delegation=True,

)
