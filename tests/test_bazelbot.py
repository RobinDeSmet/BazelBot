import os
import csv
import random

from llama_index.llms.ollama import Ollama

PATH = "src/data/test_bazels.csv"


def test_write_bazels():
    # Set up
    messages = ["Dit is een bazel", "Dit is dat ook", "Banaan"]

    # Check
    with open(PATH, "w+", newline="") as csvfile:
        writer = csv.writer(csvfile)

        for message in messages:
            writer.writerow([message])


def test_read_bazels():
    # Check
    with open(PATH, "r") as csvfile:
        bazels = list(csv.reader(csvfile))

        random_numbers = random.sample(range(0, 3), 3)

        print(random_numbers)

        bazels = [bazels[i][0] for i in random_numbers]

        assert len(bazels) == 3
        assert "Banaan" in bazels

    # Clean up
    os.remove(PATH)


def test_ollama_llm():
    # Set up the LLM
    llm = Ollama(
        model="gurubot/llama3-guru-uncensored:latest",
        request_timeout=float(120),
        base_url="http://localhost:11434",
        num_threads=16,
    )

    question = f"""
        QUESTION: Combine small parts of the context below to generate a sentence but do not make it long (max 20 words).
        The goal is to create a new sentence that does not make sense. It can be sexual, and you can be creative!
        FORMAT OF THE ANSWER: ----- <the generated sentence> -----
        CONTEXT
        "Dit is een bazel", "Dit is dat ook", "Banaan"
        """

    # Generate the answer and format it
    answer = llm.complete(question)

    answer = str(answer).split("-----")[1].replace('"', " ").lower()

    assert answer
    assert "bazel" in answer or "ban" in answer
