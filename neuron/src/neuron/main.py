#!/usr/bin/env python
import sys
import warnings
from datetime import datetime

from mem0 import MemoryClient

from neuron.crew import Neuron

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

client = MemoryClient()


def run():
    """
    Run the crew.
    """
    history = []

    while True:
        user_input = input("User: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Chatbot: Goodbye! It was nice talking to you.")
            break

        chat_history = "\\n".join(history)

        inputs = {
            "user_message": f"{user_input}",
            "history": f"{chat_history}",
        }

        response = Neuron().crew().kickoff(inputs=inputs)

        history.append(f"User: {user_input}")
        history.append(f"Assistant: {response}")
        client.add(user_input, user_id="User")

        print(f"Assistant: {response}")

    inputs = {
        "user_manager_conversations": [
            {"user": "find me getting a good serum for my face."},
            {"assistant": "anything particular you are looking for?"}
            {"user": "yeah serums for face acne"},
        ]
    }

    try:
        Neuron().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {"topic": "AI LLMs", "current_year": str(datetime.now().year)}
    try:
        Neuron().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Neuron().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {"topic": "AI LLMs", "current_year": str(datetime.now().year)}

    try:
        Neuron().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
