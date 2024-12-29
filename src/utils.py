"Module to centralize the util function for the app"

from datetime import datetime
import logging
import os
from pathlib import Path

from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.prompt import SYSTEM_PROMPT

logger = logging.getLogger(__name__)

load_dotenv()
DB_CONNECTION_URL = os.getenv("DB_CONNECTION_URL")
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


def get_session() -> Session:
    """Get the db session

    Returns:
        Session: Session object for sqlalchemy
    """
    # Create an engine
    engine = create_engine(DB_CONNECTION_URL)

    # Create a session maker
    session = sessionmaker(bind=engine)

    # Return the session
    return session()


def get_llm(
    model: str = GEMINI_MODEL, system_instruction: str = SYSTEM_PROMPT
) -> genai.GenerativeModel:
    """Retrieve an LLM instance.

    Args:
        model (str, optional): The specific llm model. Defaults to GEMINI_MODEL.
        system_instruction (str, optional): The system instructions. Defaults to SYSTEM_PROMPT.

    Returns:
        genai.GenerativeModel: The resulting model based on the input settings.
    """
    # Configure safety settings
    safety_settings = {
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    }

    # Configure Google-Generative AI package with API key
    genai.configure(api_key=GEMINI_API_KEY)

    # Configure the model
    llm = genai.GenerativeModel(
        model,
        safety_settings=safety_settings,
        system_instruction=system_instruction,
    )

    return llm


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
