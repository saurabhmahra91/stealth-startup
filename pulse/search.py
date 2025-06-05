import importlib
import json
import os
import sys

from crewai import CrewOutput
from memory import valkey_client
from neuron.crews import Neuron


def run_for_user(user_id, user_input):
    history = get_chat_history(user_id)

    history.append({"user": user_input})

    inputs = {"user_message": user_input, "conversation_history": history}

    neuron = Neuron()
    crew = neuron.crew()

    print("############################")
    print("The agents and their attributes")
    print([agent.role for agent in crew.agents])
    print("############################")
    print("The tasks and their attributes")
    print([task.description for task in crew.tasks])

    result: CrewOutput = crew.kickoff(inputs=inputs)

    del crew
    del neuron

    print("##############################")
    print("Raw result from the crew ==== \n\n")
    print(type(result.json))
    print(result.json)

    if result.json is None:
        return {"sql_query": "", "justification": "Error", "follow_up": "Error"}

    parsed_results = json.loads(result.json)

    justification = parsed_results["justification"]
    sql_query = parsed_results["sql_query"]
    follow_up = parsed_results["follow_up_question"]

    history.append({"manager": {"justification": justification, "sql_query": sql_query, "follow_up": follow_up}})
    save_chat_history(user_id, history)

    return {"sql_query": sql_query, "justification": justification, "follow_up": follow_up}


def get_chat_history(user_id):
    key = user_id

    if valkey_client.exists(key):
        res = valkey_client.get(key)
        return json.loads(res)
    else:
        return []


def save_chat_history(user_id, history):
    key = user_id
    valkey_client.set(key, json.dumps(history), ex=60 * 60 * 24)


def user_exists(user_id):
    return valkey_client.exists(f"{user_id}") == 1


def flush_user_memory(user_id):
    valkey_client.delete(f"{user_id}")
