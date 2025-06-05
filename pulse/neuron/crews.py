# Import agents
from crewai import Agent, Crew, Process, Task

from .agents.manager import manager
from .agents.product_matcher import product_matcher
from .agents.proofreader import proofreader
from .agents.salesman import salesman

# Imp.ort tasks
from .tasks.cross_verify_output_sql import cross_verify_output_sql
from .tasks.find_similar_user_reviews import find_similar_user_reviews
from .tasks.get_relevant_products import get_relevant_products
from .tasks.prepare_sql_for_relevant_products import prepare_sql_for_relevant_products
from .tasks.prepare_sql_for_close_user_reviews import prepare_sql_for_close_user_reviews


class Neuron:
    """Neuron crew"""

    def agent_manager(self) -> Agent:
        return manager

    def agent_product_matcher(self) -> Agent:
        return product_matcher

    def agent_proofreader(self) -> Agent:
        return proofreader

    def agent_salesman(self) -> Agent:
        return salesman

    def task_get_relevant_products(self) -> Task:
        return get_relevant_products

    def task_prepare_sql(self) -> Task:
        return prepare_sql_for_relevant_products

    def task_cross_verify_sql(self) -> Task:
        return cross_verify_output_sql

    def task_find_reviews(self) -> Task:
        return find_similar_user_reviews

    def task_prepare_sql_for_close_user_reviews(self) -> Task:
        return prepare_sql_for_close_user_reviews

    def crew(self) -> Crew:
        return Crew(
            agents=[
                self.agent_manager(),
                self.agent_product_matcher(),
                self.agent_proofreader(),
                self.agent_salesman(),
            ],
            tasks=[
                self.task_prepare_sql(),
                self.task_cross_verify_sql(),
                self.task_find_reviews(),
                self.task_prepare_sql_for_close_user_reviews(),
                self.task_get_relevant_products(),
            ],
            process=Process.sequential,
            verbose=True,
        )
