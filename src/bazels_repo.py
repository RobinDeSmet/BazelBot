"""Repo module to talk to the database for the bazels"""

import logging
import hashlib

from sqlalchemy import func
from sqlalchemy.orm import Session

from src.utils import get_session
from src.models import Bazel

logger = logging.getLogger(__name__)


def add(bazel_content: str):
    """Add a bazel to the db

    Args:
        bazel_content (str): The content that we want to add
    """
    logger.info(f"Adding bazel: {bazel_content}...")
    try:
        # Retrieve session
        session = get_session()

        # Generate content hash
        content_hash = hashlib.sha256(bazel_content.encode("utf-8")).hexdigest()

        # Create bazel object
        bazel = Bazel(content=bazel_content, content_hash=content_hash)

        # Add bazel object
        session.add(bazel)
        session.commit()

        logger.info("Bazel successfully added!")
    except Exception as exc:
        if exc.__class__.__name__ == "IntegrityError":
            logger.info("Bazel already present in the database!")
        else:
            logger.info(f"Bazel could not be added: {exc}")
    finally:
        # Close the session
        session.close()


def add_bazels(bazels: list[str]):
    """Add multiple bazels to the db

    Args:
        bazels (list[str]): List of new content for the bazels
    """
    logger.info(f"Adding {len(bazels)} bazels...")

    for bazel in bazels:
        add(bazel)

    logger.info(f"{len(bazels)} Bazels successfully added!")


def get(bazel_id: int) -> Bazel:
    """Retrieve a bazel based on its id

    Args:
        bazel_id (int): the id of the basel

    Returns:
        Bazel: Bazel object
    """
    logger.info(f"Retrieving bazel with ID: {bazel_id}...")
    try:
        # Retrieve session
        session = get_session()

        # Get bazel object
        bazel = session.query(Bazel).filter_by(id=bazel_id).first()

        logger.info("Bazel successfully retrieved!")

        return bazel
    except Exception as exc:
        logger.info(f"Bazel could not be retrieved: {exc}")
    finally:
        # Close the session
        session.close()


def list_bazels(session: Session) -> list[Bazel]:
    """Get all the bazels

    Returns:
        list[Bazel]: List of bazels
    """
    logger.info("Retrieving all bazels...")
    try:
        # Add bazel object
        bazels = session.query(Bazel).all()

        logger.info(f"{len(bazels)} Bazels successfully retrieved!")

        return bazels
    except Exception as exc:
        logger.info(f"Bazels could not be retrieved: {exc}")
        return None
    finally:
        # Close the session
        session.close()


def count() -> int:
    """Count the amount of bazels in the db

    Returns:
        int: The amount of bazels in the db
    """
    logger.info("Counting all bazels...")
    try:
        # Retrieve session
        session = get_session()

        # Add bazel object
        bazel_count = session.query(func.count(Bazel.id)).scalar()

        logger.info(f"There are {bazel_count} bazels in the db!")

        return bazel_count
    except Exception as exc:
        logger.info(f"Bazels could not be counted: {exc}")
    finally:
        # Close the session
        session.close()
