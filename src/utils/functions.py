from datetime import datetime
import hashlib
import logging
import os
from pathlib import Path

from dotenv import load_dotenv

logger = logging.getLogger(__name__)

load_dotenv()
GEMINI_MODEL = os.getenv("GEMINI_MODEL")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
BAZEL_IMAGE_SAVE_PATH = os.getenv("BAZEL_IMAGE_SAVE_PATH")


def configure_logging():
    """Configure the logger for the app"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)8s %(asctime)s %(name)24s %(message)s",
        datefmt="%H:%M:%S",
    )


def generate_content_hash(content: str) -> str:
    """Generate the content hash for a bazel

    Args:
        content (str): Content to be hashed

    Returns:
        str: The hashed content
    """
    # Generate content hash
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def create_image_save_path_from_bazel(bazel: str) -> Path:
    """Create a save path from a bazel.

    Args:
        bazel (str): Bazel in text format.

    Returns:
        Path: Output path created from the bazel
    """
    bazel_alphabetical = "".join(char for char in bazel if char.isalpha())
    current_date = datetime.now()
    formatted_date = current_date.strftime("%Y_%m_%d")

    bazel_image_path = Path(
        BAZEL_IMAGE_SAVE_PATH,
        formatted_date,
        f"bazel_image_{bazel_alphabetical[:20]}.png",
    )

    if not bazel_image_path.parent.exists():
        bazel_image_path.parent.mkdir(parents=True, exist_ok=True)

    return bazel_image_path
