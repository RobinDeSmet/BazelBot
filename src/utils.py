"Module to centralize the util function for the app"

import logging
import os

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


def get_llm() -> genai.GenerativeModel:
    """Retrieve the LLM.

    Returns:
        genai.GenerativeModel: The resulting model.
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
        GEMINI_MODEL,
        safety_settings=safety_settings,
        system_instruction=SYSTEM_PROMPT,
    )

    return llm
