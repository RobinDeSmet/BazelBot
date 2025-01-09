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
    engine = create_engine(
        DB_CONNECTION_URL,
        pool_size=20,
        max_overflow=2,
        pool_timeout=30,
        pool_recycle=300,
        pool_pre_ping=True,
        pool_use_lifo=True,
        connect_args={
            "keepalives": 1,
            "keepalives_idle": 30,
            "keepalives_interval": 10,
            "keepalives_count": 5,
        },
    )

    # Create a session maker
    session = sessionmaker(bind=engine)

    # Return the session
    return session()
