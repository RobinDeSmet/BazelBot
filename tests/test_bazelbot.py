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
    # Test to make sure that we can connect to the database
    session = setup_database

    amount_of_bazels = session.query(Bazel).count()

    assert amount_of_bazels == 10


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
            VRAAG: Combineer woorden van de gegeven context en maak er een nieuwe zin mee.
                   De zin mag maximaal bestaan uit 25 woorden.
                   De nieuwe zin mag seksueel getint zijn en je kan er zeer creatief mee omspringen.
            FORMAT: Het antwoord moet als volgt geformat worden: ----- <de nieuwe zin> -----
            CONTEXT:
            {bazel_context}
            """

    # Generate the answer and format it
    answer = llm.complete(question)

    print(answer)

    answer = str(answer).split("-----")[1].replace('"', " ").lower()

    print(answer)

    # Check
    assert answer
    assert len(answer.split(" ")) <= 25
