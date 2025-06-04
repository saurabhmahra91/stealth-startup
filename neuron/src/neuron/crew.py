from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators


@CrewBase
class Neuron:
    """Neuron crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def product_matcher(self) -> Agent:
        return Agent(
            config=self.agents_config["product_matcher"],  # type: ignore[index]
            verbose=True,
        )

    @agent
    def salesman(self) -> Agent:
        return Agent(
            config=self.agents_config["salesman"],  # type: ignore[index]
            verbose=True,
        )

    @agent
    def manager(self) -> Agent:
        return Agent(
            config=self.agents_config["manager"],  # type: ignore[index]
            verbose=True,
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def prepare_sql_for_relevant_products(self) -> Task:
        return Task(
            config=self.tasks_config["prepare_sql_for_relevant_products"],  # type: ignore[index]
        )

    @task
    def find_simialr_user_reviews(self) -> Task:
        return Task(
            config=self.tasks_config["find_simialr_user_reviews"],  # type: ignore[index]
        )

    @task
    def get_relevant_products(self) -> Task:
        return Task(
            config=self.tasks_config["get_relevant_products"],  # type: ignore[index]
            output_file="relevant_products.json",
        )

    @task
    def cross_verify_output_sql(self) -> Task:
        return Task(
            config=self.tasks_config["cross_verify_output_sql"],  # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Neuron crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
