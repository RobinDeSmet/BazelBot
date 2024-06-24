import os
from dotenv import load_dotenv
from llama_index.llms.ollama import Ollama
from src import bazels_controller
from src.custom_types import BazelType

load_dotenv()
DB_CONNECTION_URL = os.getenv("DB_CONNECTION_URL")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")
MAX_BAZEL_LENGTH = int(os.getenv("MAX_BAZEL_LENGTH"))
NUM_THREADS = int(os.getenv("NUM_THREADS"))
OLLAMA_REQUEST_TIMEOUT = int(os.getenv("OLLAMA_REQUEST_TIMEOUT"))
LLM = os.getenv("LLM")

# Set up the LLM
llm = Ollama(
    model=LLM,
    request_timeout=OLLAMA_REQUEST_TIMEOUT,
    base_url=OLLAMA_BASE_URL,
)


def test_generate_normal_bazel(setup_database):
    # Get test session
    session = setup_database

    # Generate normal bazel
    for index in range(10):
        print(f"\n\nStress test iteration: {index}")

        bazel = bazels_controller.generate_bazel(session=session)
        print(bazel)

        # Check
        assert bazel
        assert len(bazel.split(" ")) <= MAX_BAZEL_LENGTH  # Bazel should not be too long


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
    assert (
        len(custom_bazel.split(" ")) <= MAX_BAZEL_LENGTH
    )  # Bazel should not be too long
    assert (
        user_context.lower() in custom_bazel.lower()
    )  # Make sure that the user context is present in the custom bazel
