from crewai import Task

from ..agents.manager import manager
from ..tools.user_review_retriever import SemanticUserReviewRetriever
from ..tools.user_review_schema_retriever import GetUserReviewsTableSchema


find_similar_user_reviews = Task(
    description="""
        Search the user_reviews database for relevant reviews based on user attributes or shortlisted products.
    """,
    expected_output="""
        List of similar user reviews as dicts with keys: product, rating, review, age, skin_type
    """,
    agent=manager,
    tools=[SemanticUserReviewRetriever(), GetUserReviewsTableSchema()],
    output_file="find_similar_user_reviews.md",
)
