"""Controller module for bazels"""

import asyncio
import json
import logging
from pathlib import Path
import random
import os

from discord import Message
from dotenv import load_dotenv
import google.generativeai as genai
from sqlalchemy.orm import Session

from src.database import bazels_db_functions
from src.controllers import image_generation
from src.prompts.bazel_flavours import (
    BAZEL_IMAGE_FLAVOURS,
    BAZEL_FLAVOURS,
)
from src.prompts.system import SYSTEM_PROMPT_IMAGE_GENERATION
from src.utils.functions import create_image_save_path_from_bazel, get_session, get_llm
from src.utils.custom_types import (
    BazelFlavour,
    BazelGenerationIntermediateModel,
    BazelImageDescriptionModel,
    BazelModel,
    BazelType,
)


logger = logging.getLogger(__name__)

# Load in .env variables
load_dotenv()
LLM = os.getenv("LLM")
BAZEL_IMAGE_WIDTH = int(os.getenv("BAZEL_IMAGE_WIDTH"))
BAZEL_IMAGE_HEIGHT = int(os.getenv("BAZEL_IMAGE_HEIGHT"))
BAZEL_IMAGE_SAVE_PATH = os.getenv("BAZEL_IMAGE_SAVE_PATH")
MAX_BAZEL_LENGTH = int(os.getenv("MAX_BAZEL_LENGTH"))
MAX_BAZELS_IN_CONTEXT = int(os.getenv("MAX_BAZELS_IN_CONTEXT"))


def populate_database(messages: list[Message], session: Session = get_session()) -> int:
    """Populating the database with new messages

    Args:
        messages (list[Message]): List of messages from a discord channel.
        session (Session, optional): The session. Defaults to get_session().

    Returns:
        int: Amount of added bazels
    """
    logger.info(f"Populating database with {len(messages)} messages...")

    added_bazels = 0

    # Check if db needs to be populated
    if bazels_db_functions.count(session) == len(messages):
        logger.info("Database already populated")
        return added_bazels
    # Add the bazels
    for message in messages:
        try:
            result = bazels_db_functions.add(message.content, session)

            if result == 1:
                added_bazels += 1
        except Exception as exc:
            logger.error(f"Bazel could not be added: {exc}")

    logger.info(f"Added {added_bazels} new bazels")
    return added_bazels


async def generate_bazel(
    nr_bazels: int = 10,
    user_context: str = "",
    bazel_type: BazelType = BazelType.NORMAL,
    generate_image: bool = False,
    session: Session = get_session(),
) -> BazelModel:
    """Generate a bazel

    Args:
        nr_bazels (int, optional): Number of bazels to be taken as context. Defaults to 10.
        user_context (str, optional): The user context when a custom bazel is requested. Defaults to "".
        bazel_type (BazelType, optional): Bazel type. Defaults to BazelType.NORMAL.
        generate_image (bool, optional): Determines if an image will be generated for the Bazel. Defaults to False.
        session (Session, optional): The session. Defaults to get_session().

    Returns:
        BazelModel: The generated bazel
    """
    logger.info("Generating bazel...")
    try:
        # Get bazel context
        bazel_context = generate_bazel_context(nr_bazels=nr_bazels, session=session)

        # Get random text bazel flavour
        bazel_flavour = get_random_bazel_flavour()

        # Formatting user prompt
        prompt = format_prompt(
            context=bazel_context,
            bazel_flavour=bazel_flavour,
            bazel_type=bazel_type,
            user_context=user_context,
        )

        # Generate bazel
        generation_config = genai.GenerationConfig(
            response_mime_type="application/json",
            response_schema=BazelGenerationIntermediateModel,
        )

        llm = get_llm()
        response = llm.generate_content(prompt, generation_config=generation_config)

        # Load new bazel in the intermediate pydantic Model
        new_intermediate_bazel = BazelGenerationIntermediateModel(
            **json.loads(response.text)
        )

        # Add bazel flavour to eventual bazel
        new_bazel = BazelModel(
            text=new_intermediate_bazel.text,
            text_english=new_intermediate_bazel.text_english,
            bazel_flavour=bazel_flavour,
        )
        logger.info("Bazel successfully generated!")

        # Generate image of the bazel if needed
        if generate_image:
            task = asyncio.create_task(generate_image_for_bazel(bazel=new_bazel))
            await task
        return new_bazel
    except Exception as exc:
        logger.error(f"Bazel could not be generated: {exc}")
        raise ValueError(f"Bazel could not be generated: {exc}") from exc


async def generate_image_for_bazel(bazel: BazelModel, retries=2):
    """Generate an image for the given bazel.

    Args:
        bazel (BazelModel): The bazel in to generate an image for.
        retries (int, optional): Number of times we can retry to generate the bazel image. Defaults to 3.
    """
    logger.info(f"Generating image for bazel: {bazel.text_english}...")

    # Transfer bazel into image description
    llm = get_llm(system_instruction=SYSTEM_PROMPT_IMAGE_GENERATION)

    generation_config = genai.GenerationConfig(
        response_mime_type="application/json",
        response_schema=BazelImageDescriptionModel,
    )

    prompt = f"""
        Generate a detailed description for the image generation for this sentence: {bazel.text_english}

        ## Instructions
        {bazel.bazel_flavour.image_instructions}
        - If you do not follow these instructions, your task will fail!
        """
    response = llm.generate_content(prompt, generation_config=generation_config)

    new_bazel_image_description = BazelImageDescriptionModel(
        **json.loads(response.text)
    )
    logger.info(f"Bazel description: {new_bazel_image_description.description}")

    # Initialize the image model
    model_obj = image_generation.ImageModel(
        model="evil",
        seed="random",
        width=BAZEL_IMAGE_WIDTH,
        height=BAZEL_IMAGE_HEIGHT,
    )

    # Make sure the directory exists
    bazel_image_dir = Path(BAZEL_IMAGE_SAVE_PATH)
    if not bazel_image_dir.exists():
        bazel_image_dir.mkdir(parents=True, exist_ok=True)

    # Create image save path
    bazel_image_save_path = create_image_save_path_from_bazel(bazel.text_english)

    # Generate bazel image and save it locally
    for attempt in range(retries):
        try:
            await model_obj.generate(
                prompt=new_bazel_image_description.description,
                save=True,
                file=str(bazel_image_save_path),
            )
            logger.info("Bazel image successfully generated!")
            return
        except Exception as e:
            if attempt == retries - 1:
                logger.error(f"Error generating the bazel image: {e}")
                raise e
            else:
                logger.info(
                    f"Something went wrong when generating the bazel image: {e}. Retrying..."
                )


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
        bazels = bazels_db_functions.list(session=session)

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


def get_random_bazel_flavour() -> BazelFlavour:
    """Get a random bazel flavour based on the flavour type requested.

    Args:
        bazel_flavour_type (BazelFlavourType): The type of bazel flavour.

    Returns:
        BazelFlavour: The random bazel flavour.
    """
    logger.info("Generating a random bazel flavour...")

    # Text flavour
    # Setup the instructions and accompanied weights lists
    bazel_flavours = []
    weights = []
    for flavour, flavour_values in BAZEL_FLAVOURS.items():
        new_bazel_flavour = BazelFlavour(
            bazel_flavour_name=flavour,
            bazel_instructions=flavour_values["bazel_instructions"],
            image_instructions=flavour_values["image_instructions"],
            image_flavour_name=flavour,
        )
        bazel_flavours.append(new_bazel_flavour)
        weights.append(flavour_values["weight"])

    # Pick a random flavour
    random_flavour: BazelFlavour = random.choices(bazel_flavours, weights=weights, k=1)[
        0
    ]

    # Image flavour
    if random_flavour.image_instructions.lower() == "random":
        # Setup the instructions and accompanied weights lists
        bazel_image_instructions = []
        weights = []
        for flavour, flavour_values in BAZEL_IMAGE_FLAVOURS.items():
            bazel_image_instructions.append((flavour, flavour_values["instructions"]))
            weights.append(flavour_values["weight"])

        # Pick a random flavour
        random_image_flavour = random.choices(
            bazel_image_instructions, weights=weights, k=1
        )[0]

        # Update the image flavour name and instructions
        random_flavour.image_flavour_name = random_image_flavour[0]
        random_flavour.image_instructions = random_image_flavour[1]

    logger.info(f"Random flavour generated: {random_flavour}")
    return random_flavour


def format_prompt(
    context: str,
    bazel_flavour: BazelFlavour,
    user_context="",
    bazel_type: BazelType = BazelType.NORMAL,
) -> str:
    """Format the bazel prompt

    Args:
        context (str): Bazel context.
        text_bazel_flavour (str): The flavour of the textual bazel.
        user_context (str, optional): User context for a custom bazel. Defaults to "".
        bazel_type (BazelType, optional): Bazel type. Defaults to BazelType.NORMAL.

    Returns:
        str: The prompt
    """
    logger.info(f"Formatting the prompt for bazel type: {bazel_type}...")
    # Generate the correct prompt
    match bazel_type:
        case BazelType.NORMAL:
            prompt = f"""
                Hey Bazelbot, ik zou graag een bazel genereren aan de hand van onderstaande voorbeelden.

                ## Extra instructies
                {bazel_flavour.bazel_instructions}
                - Als je niet aan deze instructies voldoet faalt je taak!
                ## Bazel voorbeelden:
                {context}
                """
        case BazelType.CUSTOM:
            prompt = f"""
                Hey Bazelbot, ik zou graag een bazel genereren aan de hand van onderstaande voorbeelden.

                ## Extra instructies
                {bazel_flavour.bazel_instructions}
                - Zorg ervoor dat je dit zeker includeert in de bazel: {user_context}!
                - Als je niet aan deze instructies voldoet faalt je taak!
                ## Bazel voorbeelden:
                {context}
                """

    logger.info(f"Prompt successfully formatted: {prompt}")
    return prompt
