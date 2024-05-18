"Module to centralize the util function for the app"
import logging
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

logger = logging.getLogger(__name__)

load_dotenv()
DB_CONNECTION_URL = os.getenv("DB_CONNECTION_URL")


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
