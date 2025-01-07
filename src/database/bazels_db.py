import logging

from sqlalchemy import func
from sqlalchemy.orm import Session

from src.database.session import get_session
from src.utils.functions import generate_content_hash
from src.database.models import Bazel

logger = logging.getLogger(__name__)


def add(bazel_content: str, session: Session) -> int:
    """Add a bazel to the db

    Args:
        bazel_content (str): The content that we want to add
        session (Session): The session

    Returns:
        int: 0=Already exists, 1=Added
    """
    logger.info(f"Adding bazel: {bazel_content}...")

    try:
        # Generate content hash
        content_hash = generate_content_hash(bazel_content)

        # Check if bazel already exists
        if exists(content_hash, session=session):
            logger.info("Bazel is already present in db!")
            return 0
        # Create bazel object
        new_bazel = Bazel(content=bazel_content, content_hash=content_hash)
        session.add(new_bazel)
        session.commit()

        logger.info("Bazel added to db")
        return 1
    except Exception as exc:
        logger.error(f"Bazel could not be added to the db: {exc}")
        raise exc


def list(session: Session) -> list[Bazel]:
    """Get all the bazels

    Args:
        session (Session): The session

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
        raise exc


def get(bazel_content: str, session: Session) -> Bazel:
    """Get a bazel

    Args:
        bazel_content (str): The content of the bazel
        session (Session): The session
    """
    logger.info(f"Retrieving bazel: {bazel_content}...")
    try:
        # Retrieve bazel object
        bazel = (
            session.query(Bazel).filter(Bazel.content == bazel_content).one_or_none()
        )

        logger.info(f"Bazel with ID: { bazel.id } successfully retrieved!")

        return bazel
    except Exception as exc:
        logger.info(f"Bazel could not be retrieved: {exc}")
        raise exc


def delete(bazel_content: str, session: Session):
    """Delete a bazel

    Args:
        bazel_content (str): The content of the bazel
        session (Session): The session
    """
    logger.info(f"Deleting bazel: {bazel_content}...")
    try:
        # Add bazel object
        bazels = session.query(Bazel).filter(Bazel.content == bazel_content).delete()

        logger.info(f"{len(bazels)} Bazel successfully deleted!")
    except Exception as exc:
        logger.info(f"Bazel could not be deleted: {exc}")


def count(session: Session = get_session()) -> int:
    """Count the amount of bazels in the db

    Args:
        session (Session): The session

    Returns:
        int: The amount of bazels in the db
    """
    logger.info("Counting all bazels...")
    try:
        # Add bazel object
        bazel_count = session.query(func.count(Bazel.id)).scalar()

        logger.info(f"There are {bazel_count} bazels in the db!")

        return bazel_count
    except Exception as exc:
        logger.info(f"Bazels could not be counted: {exc}")
        raise exc


def exists(bazel_content_hash: str, session: Session) -> bool:
    """Check if the bazel exists based on its hash

    Args:
        bazel_content_hash (str): Content hash
        session (Session): The session

    Returns:
        bool: True if exists, False if not
    """
    return (
        session.query(Bazel).filter_by(content_hash=bazel_content_hash).first()
        is not None
    )
