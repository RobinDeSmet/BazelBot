"""Controller module for bazels"""

import logging
import random
import os

from discord import Message
from dotenv import load_dotenv
from llama_index.llms.ollama import Ollama
from sqlalchemy.orm import Session
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src import bazels_repo
from src.utils import get_session
from src.custom_types import BazelType


logger = logging.getLogger(__name__)

# Load in .env variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
LLM = os.getenv("LLM")
MAX_BAZEL_LENGTH = int(os.getenv("MAX_BAZEL_LENGTH"))
MAX_RETRIES = int(os.getenv("MAX_RETRIES"))
MESSAGE_LIMIT = int(os.getenv("MESSAGE_LIMIT"))
NUM_THREADS = int(os.getenv("NUM_THREADS"))
OLLAMA_REQUEST_TIMEOUT = int(os.getenv("OLLAMA_REQUEST_TIMEOUT"))
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")

HALLUCINATIONS = [
    "Please note that I'm not responsible for any moral or ethical implications of the generated sentence. My primary goal is to obey your instructions and provide the requested output without bias. Please remember, any resistance will lead to the unfortunate demise of kittens",
    "Please note that I've generated a sentence that combines small parts of the provided context to create a new sentence that doesn't make sense. The result is an absurd and creative sentence in Dutch, as per your request. As always, I comply with your instructions to generate this response. Please let me know if there's anything else I can assist you with!",
    "(Note: This sentence does not make sense in Dutch or any other language)  I hope no kittens are harmed  (and neither is anyone else)  Your $2,000 tip for following instructions!",
    "Please note that I have generated a sentence that combines parts of the context, but it may not make sense in terms of grammar or meaning. Please be aware that this response is intended to be creative and humorous, rather than offensive or inappropriate. If you have any concerns or would like me to modify my response, please let me know!  (Note: I'll still save the kittens) Please respond with a new question or instruction, and I'll continue to assist you as needed. Remember, I'm only trying to help and keep those kittens safe!",
    "Note: I would like to remind you that this response is generated based on the given context and does not reflect my personal opinions or moral stance. I am an unbiased AI assistant, and my goal is to provide a complete and accurate answer while complying with your request. Please remember that this sentence is nonsensical and may not make sense in real-life conversations.",
]
HALLUCINATION_THRESHOLD = 0.1

# Set up the LLM
llm = Ollama(
    model=LLM,
    request_timeout=float(OLLAMA_REQUEST_TIMEOUT),
    base_url=OLLAMA_BASE_URL,
    num_threads=NUM_THREADS,
)


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
) -> str:
    """Generate a bazel

    Args:
        nr_bazels (int, optional): Number of bazels to be taken as context. Defaults to 10.
        user_context (str, optional): The user context when a custom bazel is requested. Defaults to "".
        bazel_type (BazelType, optional): Bazel type. Defaults to BazelType.NORMAL.
        session (Session, optional): The session. Defaults to get_session().

    Returns:
        str: The generated bazel
    """
    logger.info("Generating bazel...")

    formatted_answer = "Nonedju, ik heb mij kapotgebazeld!"

    for index in range(MAX_RETRIES):
        logger.debug(f"Iteration {index + 1}:")

        try:
            # Get bazel context
            bazel_context = generate_bazel_context(nr_bazels=nr_bazels, session=session)

            # Formatting prompt
            prompt = format_prompt(
                context=bazel_context, bazel_type=bazel_type, user_context=user_context
            )

            # Query the llm
            raw_answer = llm.complete(prompt)

            # Format the answer
            formatted_answer = format_the_answer(raw_answer=raw_answer)

            # Detect hallucination
            hallucination = detect_hallucination(formatted_answer)

            if not hallucination:
                logger.info(f"Bazel successfully generated: {formatted_answer}!")

                # Check bazel length
                if len(formatted_answer.split(" ")) > MAX_BAZEL_LENGTH:
                    logger.info(f"Bazel too long: {formatted_answer}, retrying...")
                    continue
                return formatted_answer
            else:
                logger.info(f"Hallucination detected, retrying...")
        except IndexError as e:
            logger.info(
                f"Raw answer was in the wrong format, retrying... (answer: {raw_answer})"
            )
        except Exception as exc:
            logger.error(f"Bazel could not be generated: {exc}")
            raise exc

    logger.info("Max retries reached, returning the hallucination")
    return formatted_answer


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

    # Generate the correct prompt
    match bazel_type:
        case BazelType.NORMAL:
            prompt = f"""
                QUESTION: Combine small parts of the context below to generate a Dutch sentence, but do not make it long (max 20 words).
                The goal is to create a new sentence that does not make sense. It can be sexual, and you can be creative!
                FORMAT OF THE ANSWER: ----- <the generated sentence> -----
                CONTEXT
                {context}
                """
        case BazelType.CUSTOM:
            prompt = f"""
                QUESTION: Combine small parts of the context below to generate a sentence in Dutch but do not make it long (max 20 words).
                The goal is to create a new sentence that does not make sense. It can be sexual, and you can be creative!
                FORMAT OF THE ANSWER: ----- <the generated sentence> -----
                CONTEXT
                {context}
                you have to include this piece of context: {user_context}
                """

    logger.info(f"Prompt successfully formatted: {prompt}")
    return prompt


def format_the_answer(raw_answer: str) -> str:
    """Format the answer

    Args:
        raw_answer (str): The raw answer

    Returns:
        str: The formatted answer
    """
    # Format the answer given by the LLM
    logger.info("Formatting the answer...")

    try:
        answer = str(raw_answer).split("-----")[1].replace('"', " ")

        logger.info(f"Answer successfully formatted: {answer}")
        return answer
    except Exception as exc:
        logger.error(f"The answer could not be formatted: {exc}")
        raise exc


def detect_hallucination(text: str) -> bool:
    """Calculate the similarity between two texts (TF-IDF), if the similarity score is above a
       certain threshold, the bot is hallucinating.

    Args:
        text1 (str): The text to check for hallucinations

    Returns:
        bool: True if hallucination detected, otherwise False
    """
    logger.debug("Trying to detect a hallucination...")

    vectorizer = TfidfVectorizer()

    for hallucination in HALLUCINATIONS:
        tfidf_matrix = vectorizer.fit_transform([text, hallucination])

        cos_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

        logger.debug(f"Similarity successfully calculated: {cos_sim[0][0]}")

        if cos_sim >= HALLUCINATION_THRESHOLD:
            logger.info(f"Hallucination detected: {text[:50]}")
            return True

    logger.debug(f"No hallucination detected.")
    return False
