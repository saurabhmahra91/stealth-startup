from crewai import Task

from ..agents.manager import manager
from ..tools.config import PRODUCTS_DB_PATH
from ..tools.product_retriever import RunSQLOnBeautyProductsTable
from ..tools.product_schema_retriever import GetProductTableSchema


from pydantic import BaseModel, Field


class FinalOutput(BaseModel):
    sql_query: str = Field(description="The SQLite3 compatible SQL query. If providing the follow_up_question, keep it such that running this sql wont give any rows (e.g. have a limit 0 clause)")
    justification: str = Field(description="A message for the user stating the reason why these products are selected or why follow up is required.")
    follow_up_question: str | None = Field(description="If more information is required and can be beneficial. Make sure to not ask more than two question in all turns of the conversation")


get_relevant_products = Task(
    description="""
        - Read the user's natural language query
        ```
        {user_message}
        ```
        and provide a SQL query, justification, and sample results.

        - Also read the conversation_history
        ```
        {conversation_history}
        ```
        with the user. If its the beginning of a conversation, ask 1-2 question to know better the user's requirements, instead of showing the results.
        Do not repeat this question loop more than 2 questions.

        - The result can be greatly enhanced if we show the user historical user reviews that match either the product's attributes or user's attributes.
        Note that this is just enhancement, and it does not mean that you should not return products if there were not close reviews found.

        - Make a decision whether you want to ask user more questions to get more close to the products he/she wants or do you want to display the results
        based on current query.

        -If you are asking a followup question / chatting with the user, the sql should not fetch zero rows (put a zero limit clause)
        -If you are showing the user few products while also asking a follow up ensure that the sql has the order by clause to sort the relevant only results in descreasing margin order.
        -If you are showing the user products, without the intent of a followup question, ensure that the sql has the order by clause to sort the relevant only results in descreasing margin order.
    """,
    expected_output="""
        A valid JSON with these keys:
        - follow_up_question
        - sql_query
        - justification
    """,
    agent=manager,
    tools=[
        RunSQLOnBeautyProductsTable(db_path=PRODUCTS_DB_PATH),
        GetProductTableSchema(db_path=PRODUCTS_DB_PATH),
    ],
    output_file="get_relevant_products.json",
    output_json=FinalOutput
)
