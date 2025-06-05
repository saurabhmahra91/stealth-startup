from crewai import Task

from ..agents.manager import manager
from ..tools.user_review_schema_retriever import GetUserReviewsTableSchema
from ..tools.user_review_retriever import SemanticUserReviewRetriever

prepare_sql_for_close_user_reviews = Task(
    description="""
        1. Interpret the natural language filter for user_reviews table
        2. Prepare a SQL query which can be run on the user_reviews table
        4. If the natural language did not mention, add a limit clause yourself (the limit should always be less than 50)
        5. Generate the final SQL query which can be used to query user_reviews table.
    """,
    expected_output="""a valid SQLite3 query for fetching rows from the user_reviews table""",
    agent=manager,
    tools=[
        GetUserReviewsTableSchema(),
        SemanticUserReviewRetriever()
    ],
    output_file="sql_for_close_user_reviews.md"
)

