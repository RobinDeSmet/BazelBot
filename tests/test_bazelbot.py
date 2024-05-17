import os
import pytest

from dotenv import load_dotenv
from llama_index.llms.ollama import Ollama
from src.models import Bazel
from src import bazels_controller

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

    print(f"There are {amount_of_bazels} bazels in the test database")

    assert amount_of_bazels == 10


def test_format_answer():
    # Success
    raw_answer = "Gibber1sh ----- ANSWER ----- G1bberish!"

    answer = bazels_controller.format_the_answer(raw_answer)

    assert answer == " ANSWER "

    # Fail
    raw_answer = "Gibber1sh ANSWER G1bberish!"

    with pytest.raises(IndexError):
        answer = bazels_controller.format_the_answer(raw_answer)

    # TODO: EXPAND TEST WITH REGRESSION FAILURES


def test_generate_bazel_context(setup_database):
    # Test to make sure that the bazel context is correctly generated
    session = (
        setup_database  # You have to give the test session to the controller functions!
    )

    context = bazels_controller.generate_bazel_context(session=session)

    print(f"\n{context}")

    assert context


# def test_generate_bazel(setup_database):
#     # Get test session
#     session = setup_database

#     # Set up the LLM
#     llm = Ollama(
#         model=LLM,
#         request_timeout=OLLAMA_REQUEST_TIMEOUT,
#         base_url=OLLAMA_BASE_URL,
#     )

#     # Get bazel context
#     bazel_context = bazels_controller.generate_bazel_context(session=session)

#     question = f"""
#             VRAAG: Combineer woorden van de gegeven context en maak er een nieuwe zin mee.
#                    De zin mag maximaal bestaan uit 25 woorden.
#                    De nieuwe zin mag seksueel getint zijn en je kan er zeer creatief mee omspringen.
#             FORMAT: Het antwoord moet als volgt geformuleerd worden: ----- <de nieuwe zin> -----
#             CONTEXT:
#             {bazel_context}
#             """

#     # Generate the answer
#     answer = llm.complete(question)

#     print(answer)

#     answer = str(answer).split("-----")[1].replace('"', " ").lower()

#     print(answer)

#     # Check
#     assert answer
#     assert len(answer.split(" ")) <= 25
