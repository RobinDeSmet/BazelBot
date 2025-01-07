from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import os

from dotenv import load_dotenv


load_dotenv()
DB_CONNECTION_URL = os.getenv("DB_CONNECTION_URL")


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
