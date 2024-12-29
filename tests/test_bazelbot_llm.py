import os
from pathlib import Path
from dotenv import load_dotenv
from src import bazels_controller
from src.custom_types import BazelType
import pytest

load_dotenv()
DB_CONNECTION_URL = os.getenv("DB_CONNECTION_URL")
MAX_BAZEL_LENGTH = int(os.getenv("MAX_BAZEL_LENGTH"))
BAZEL_IMAGE_SAVE_PATH = os.getenv("BAZEL_IMAGE_SAVE_PATH")


@pytest.mark.llm
def test_generate_normal_bazel(setup_database):
    # Get test session
    session = setup_database

    # Generate normal bazel
    bazel = bazels_controller.generate_bazel(session=session)
    print(bazel)

    # Check
    assert bazel
    assert (
        len(bazel.text.split(" ")) <= MAX_BAZEL_LENGTH
    )  # Bazel should not be too long

    # Check that there is no generated image
    file_path = Path(BAZEL_IMAGE_SAVE_PATH, "bazel_image.png")
    assert not file_path.exists()


@pytest.mark.llm
def test_generate_custom_bazel(setup_database):
    # Get test session
    session = setup_database

    # Generate custom bazel
    user_context = "flamingo"
    custom_bazel = bazels_controller.generate_bazel(
        user_context=user_context, bazel_type=BazelType.CUSTOM, session=session
    )
    print(custom_bazel)

    # Check
    assert custom_bazel
    assert (
        len(custom_bazel.text.split(" ")) <= MAX_BAZEL_LENGTH
    )  # Bazel should not be too long
    assert (
        user_context.lower() in custom_bazel.text.lower()
    )  # Make sure that the user context is present in the custom bazel

    # Check that there is no generated image
    file_path = Path(BAZEL_IMAGE_SAVE_PATH, "bazel_image.png")
    assert not file_path.exists()


@pytest.mark.llm
def test_generate_bazel_with_image(setup_database):
    # Get test session
    session = setup_database

    # Generate normal bazel
    bazel = bazels_controller.generate_bazel(generate_image=True, session=session)
    print(bazel)

    # Check
    assert bazel
    assert (
        len(bazel.text.split(" ")) <= MAX_BAZEL_LENGTH
    )  # Bazel should not be too long

    # Check if the file exists
    file_path = Path(BAZEL_IMAGE_SAVE_PATH, "bazel_image.png")
    assert file_path.exists() and file_path.is_file()

    # Cleanup the file
    file_path.unlink()
