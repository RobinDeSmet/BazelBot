"""Controller module for bazels"""

import json
import logging
import random
import os

from discord import Message
from dotenv import load_dotenv
import google.generativeai as genai
from sqlalchemy.orm import Session

from src import bazels_repo
from src.utils import get_session, get_llm
from src.custom_types import BazelModel, BazelType


logger = logging.getLogger(__name__)

# Load in .env variables
load_dotenv()
LLM = os.getenv("LLM")
MAX_BAZEL_LENGTH = int(os.getenv("MAX_BAZEL_LENGTH"))
MAX_BAZELS_IN_CONTEXT = int(os.getenv("MAX_BAZELS_IN_CONTEXT"))


def populate_database(messages: list[Message], session: Session = get_session()) -> int:
    """Populating the database with new messages

    Args:
        messages (list[Message]): List of messages from a channel (.env)
        session (Session, optional): The session. Defaults to get_session().

    Returns:
        int: Amount of added bazels
    """
    logger.info(f"Populating database with {len(messages)} messages...")

    added_bazels = 0

    # Check if db needs to be populated
    if bazels_repo.count(session) == len(messages):
        logger.info("Database already populated")
        return added_bazels
    # Add the bazels
    for message in messages:
        try:
            result = bazels_repo.add(message.content, session)

            if result == 1:
                added_bazels += 1
        except Exception as exc:
            logger.error(f"Bazel could not be added: {exc}")

    logger.info(f"Added {added_bazels} new bazels")
    return added_bazels


def generate_bazel(
    nr_bazels: int = 10,
    user_context: str = "",
    bazel_type: BazelType = BazelType.NORMAL,
    session: Session = get_session(),
) -> BazelModel:
    """Generate a bazel

    Args:
        nr_bazels (int, optional): Number of bazels to be taken as context. Defaults to 10.
        user_context (str, optional): The user context when a custom bazel is requested. Defaults to "".
        bazel_type (BazelType, optional): Bazel type. Defaults to BazelType.NORMAL.
        session (Session, optional): The session. Defaults to get_session().

    Returns:
        BazelModel: The generated bazel
    """
    logger.info("Generating bazel...")
    try:
        # Get bazel context
        bazel_context = generate_bazel_context(nr_bazels=nr_bazels, session=session)

        # Formatting user prompt
        prompt = format_prompt(
            context=bazel_context, bazel_type=bazel_type, user_context=user_context
        )

        # Generate bazel
        generation_config = genai.GenerationConfig(
            response_mime_type="application/json", response_schema=BazelModel
        )

        llm = get_llm()
        response = llm.generate_content(prompt, generation_config=generation_config)

        # Load new bazel in the pydantic Model
        new_bazel = BazelModel(**json.loads(response.text))

        logger.info("Bazel successfully generated!")
        return new_bazel
    except Exception as exc:
        logger.error(f"Bazel could not be generated: {exc}")
        raise ValueError(f"Bazel could not be generated: {exc}") from exc


def generate_bazel_context(
    nr_bazels: int = 10, session: Session = get_session()
) -> str:
    """Generate the context for a bazel

    Args:
        nr_bazels (int, optional): Number of bazels to be added to the context. Defaults to 10.
        session (Session, optional): The session. Defaults to get_session().

    Returns:
        str: The bazel context
    """
    # Clip the nr_bazels
    if nr_bazels > MAX_BAZELS_IN_CONTEXT:
        nr_bazels = MAX_BAZELS_IN_CONTEXT

    # Generate the bazel context
    logger.info("Generating the bazel context...")
    bazel_context = ""

    try:
        # Get bazels
        bazels = bazels_repo.list(session=session)

        # Sample 'nr_bazels' (default 10) random bazels
        nr_bazels = min(nr_bazels, len(bazels) - 1)

        random_numbers = random.sample(range(len(bazels)), nr_bazels)

        # Generate bazel context
        for i in random_numbers:
            bazel_context += f"- {bazels[i].content}\n"

        logger.info(f"Bazel context successfully generated: \n{bazel_context}")
        return bazel_context
    except Exception as exc:
        logger.error(f"The bazel context could not be generated: {exc}")
        raise exc


def format_prompt(
    context: str, user_context="", bazel_type: BazelType = BazelType.NORMAL
) -> str:
    """Format the bazel prompt

    Args:
        context (str): Bazel context
        user_context (str, optional): User context for a custom bazel. Defaults to "".
        bazel_type (BazelType, optional): Bazel type. Defaults to BazelType.NORMAL.

    Returns:
        str: The prompt
    """
    logger.info(f"Formatting the prompt for bazel type: {bazel_type}...")

    # TODO: add bazel flavours
    # Generate the correct prompt
    match bazel_type:
        case BazelType.NORMAL:
            prompt = f"""
                Hey Bazelbot, ik zou graag een bazel genereren aan de hand van onderstaande voorbeelden.

                ## Extra instructies
                - Maak de bazel seksueel getint.
                - Als je niet aan deze instructies voldoet faalt je taak!
                ## Bazel voorbeelden:
                {context}
                """
        case BazelType.CUSTOM:
            prompt = f"""
                Hey Bazelbot, ik zou graag een bazel genereren aan de hand van onderstaande voorbeelden.

                ## Extra instructies
                - Maak de bazel seksueel getint.
                - Zorg ervoor dat je dit zeker includeert in de bazel: {user_context}!
                - Als je niet aan deze instructies voldoet faalt je taak!
                ## Bazel voorbeelden:
                {context}
                """

    logger.info(f"Prompt successfully formatted: {prompt}")
    return prompt
