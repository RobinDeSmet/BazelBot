import os
from dotenv import load_dotenv
from src import bazels_controller
from src.custom_types import BazelType
import pytest

load_dotenv()
DB_CONNECTION_URL = os.getenv("DB_CONNECTION_URL")
MAX_BAZEL_LENGTH = int(os.getenv("MAX_BAZEL_LENGTH"))


@pytest.mark.llm
def test_generate_normal_bazel(setup_database):
    # Get test session
    session = setup_database

    # Generate normal bazel
    bazel = bazels_controller.generate_bazel(session=session)
    print(bazel.text)

    # Check
    assert bazel
    assert (
        len(bazel.text.split(" ")) <= MAX_BAZEL_LENGTH
    )  # Bazel should not be too long


@pytest.mark.llm
def test_generate_custom_bazel(setup_database):
    # Get test session
    session = setup_database

    # Generate custom bazel
    user_context = "flamingo"
    custom_bazel = bazels_controller.generate_bazel(
        user_context=user_context, bazel_type=BazelType.CUSTOM, session=session
    )
    print(custom_bazel.text)

    # Check
    assert custom_bazel
    assert (
        len(custom_bazel.text.split(" ")) <= MAX_BAZEL_LENGTH
    )  # Bazel should not be too long
    assert (
        user_context.lower() in custom_bazel.text.lower()
    )  # Make sure that the user context is present in the custom bazel
