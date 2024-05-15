import pytest
import os

from dotenv import load_dotenv
from llama_index.llms.ollama import Ollama
from src.models import Bazel

load_dotenv()
DB_CONNECTION_URL = os.getenv("DB_CONNECTION_URL")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")
NUM_THREADS = int(os.getenv("NUM_THREADS"))
OLLAMA_REQUEST_TIMEOUT = int(os.getenv("OLLAMA_REQUEST_TIMEOUT"))
LLM = os.getenv("LLM")


def test_database_connection(setup_database):
    # Test to make sure that there are 5 items in the database
    session = setup_database

    amount_of_bazels = session.query(Bazel).count()

    assert amount_of_bazels == 5


def test_generate_bazel(setup_database):
    # Get test session
    session = setup_database

    # Set up the LLM
    llm = Ollama(
        model=LLM,
        request_timeout=OLLAMA_REQUEST_TIMEOUT,
        base_url=OLLAMA_BASE_URL,
    )

    # Generate the bazel context
    bazel_context = ""
    bazels = session.query(Bazel).all()

    # Generate bazel context
    bazel_context = [f"- {bazel.content}" for bazel in bazels]

    question = f"""
            QUESTION: Combine small parts of the context below to generate a sentence in Dutch but do not make it long (max 30 words).
            The goal is to create a new sentence that does not make sense. It can be sexual, and you can be creative!
            FORMAT OF THE ANSWER: ----- <the generated sentence> -----
            CONTEXT
            {bazel_context}
            """

    # Generate the answer and format it
    answer = llm.complete(question)

    answer = str(answer).split("-----")[1].replace('"', " ").lower()

    print(answer)

    # Check
    assert answer
    assert any(
        string in answer
        for string in [
            "oma",
            "wiel",
            "rimmstein",
            "banaan",
            "fiets",
            "vlag",
            "Patrick",
            "zwemmen",
            "haar",
        ]
    )
    assert len(answer.split(" ")) <= 30
