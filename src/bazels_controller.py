import logging
import random

from src import bazels_repo
from src.utils import get_session

from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


def generate_bazel_context(
    nr_bazels: int = 10, session: Session = get_session()
) -> str:
    # Generate the bazel context
    logger.info("Generating the bazel context...")
    bazel_context = ""

    try:
        # Get bazels
        bazels = bazels_repo.list_bazels(session=session)

        # Sample 10 random bazels
        random_numbers = random.sample(range(0, len(bazels)), nr_bazels)

        # Generate bazel context
        for i in random_numbers:
            bazel_context += f"- {bazels[i].content}\n"

        logger.info(f"Bazel context successfully generated: \n{bazel_context}")
        return bazel_context
    except Exception as exc:
        logger.error(f"The bazel context could not be generated: {exc}")
        raise exc


def format_the_answer(raw_answer: str) -> str:
    # Format the answer given by the LLM
    logger.info("Formatting the answer...")

    try:
        answer = str(raw_answer).split("-----")[1].replace('"', " ")

        logger.info(f"Answer successfully formatted: {answer}")
        return answer
    except Exception as exc:
        logger.error(f"The answer could not be formatted: {exc}")
        raise exc
