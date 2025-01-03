import os
import time
from dotenv import load_dotenv
from src.controllers import bazels_controller
from src.utils.custom_types import BazelType
import pytest

from src.utils.functions import create_image_save_path_from_bazel

load_dotenv()
DB_CONNECTION_URL = os.getenv("DB_CONNECTION_URL")
MAX_BAZEL_LENGTH = int(os.getenv("MAX_BAZEL_LENGTH"))
BAZEL_IMAGE_SAVE_PATH = os.getenv("BAZEL_IMAGE_SAVE_PATH")


@pytest.mark.llm
@pytest.mark.asyncio
async def test_generate_normal_bazel(setup_database):
    # Get test session
    session = setup_database

    # Generate normal bazel
    bazel = await bazels_controller.generate_bazel(session=session)
    print(bazel)

    # Check
    assert bazel
    assert (
        len(bazel.text.split(" ")) <= MAX_BAZEL_LENGTH
    )  # Bazel should not be too long

    # Check that there is no generated image
    bazel_image_save_path = create_image_save_path_from_bazel(bazel.text_english)
    assert not bazel_image_save_path.exists()


@pytest.mark.llm
@pytest.mark.asyncio
async def test_generate_custom_bazel(setup_database):
    # Get test session
    session = setup_database

    # Generate custom bazel
    user_context = "flamingo"
    custom_bazel = await bazels_controller.generate_bazel(
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
    bazel_image_save_path = create_image_save_path_from_bazel(custom_bazel.text_english)
    assert not bazel_image_save_path.exists()


@pytest.mark.llm
@pytest.mark.asyncio
async def test_generate_bazel_with_image(setup_database):
    # Get test session
    session = setup_database

    for _ in range(20):
        # Generate normal bazel
        bazel = await bazels_controller.generate_bazel(
            generate_image=True, session=session
        )
        print(bazel)

        # Check
        assert bazel
        assert (
            len(bazel.text.split(" ")) <= MAX_BAZEL_LENGTH
        )  # Bazel should not be too long

        # Check if the file exists
        bazel_image_save_path = create_image_save_path_from_bazel(bazel.text_english)
        assert bazel_image_save_path.exists() and bazel_image_save_path.is_file()

        # Sleep to not overstep the rate limit (10 requests/min)
        time.sleep(30)
