import os
from discord import Message
import pytest

from dotenv import load_dotenv
from llama_index.llms.ollama import Ollama
from src.models import Bazel
from src import bazels_controller, bazels_repo
from src.types import BazelType

load_dotenv()
DB_CONNECTION_URL = os.getenv("DB_CONNECTION_URL")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")
NUM_THREADS = int(os.getenv("NUM_THREADS"))
OLLAMA_REQUEST_TIMEOUT = int(os.getenv("OLLAMA_REQUEST_TIMEOUT"))
LLM = os.getenv("LLM")

# Set up the LLM
llm = Ollama(
    model=LLM,
    request_timeout=OLLAMA_REQUEST_TIMEOUT,
    base_url=OLLAMA_BASE_URL,
)


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

    # Test bazelcontext with nr_bazels > bazels in db
    context = bazels_controller.generate_bazel_context(nr_bazels=20, session=session)

    print(f"\n{context}")

    assert context


def test_bazel_crud_works(setup_database):
    # Get test session
    session = setup_database

    bazel_content = "New bazel that has to be added!!"

    # Add bazel
    result = bazels_repo.add(bazel_content, session)

    assert result == 1

    # Add duplicate bazel
    result = bazels_repo.add(bazel_content, session)

    assert result == 0

    # Retrieve bazel
    bazel = bazels_repo.get(bazel_content, session)

    assert bazel.content_hash == bazels_repo.generate_content_hash(bazel_content)

    # List bazels
    bazels = bazels_repo.list(session)

    assert len(bazels) == 11

    # Cleanup
    bazels_repo.delete(bazel_content, session)

    # Check if bazel is successfully deleted
    assert bazels_repo.count(session) == 10


def test_generate_normal_bazel(setup_database):
    # Get test session
    session = setup_database

    # Generate normal bazel
    bazel = bazels_controller.generate_bazel(session=session)
    print(bazel)

    # Check
    assert bazel
    assert len(bazel.split(" ")) <= 50  # Bazel should not be too long


def test_generate_custom_bazel(setup_database):
    # Get test session
    session = setup_database

    # Generate custom bazel
    user_context = "Apennootje"
    custom_bazel = bazels_controller.generate_bazel(
        user_context=user_context, bazel_type=BazelType.CUSTOM, session=session
    )
    print(custom_bazel)

    # Check
    assert custom_bazel
    assert len(custom_bazel.split(" ")) <= 50  # Bazel should not be too long
    assert (
        user_context in custom_bazel
    )  # Make sure that the user context is present in the custom bazel
