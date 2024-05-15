import pytest
import logging
import os
import hashlib

from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, delete

from src.models import Bazel

logger = logging.getLogger(__name__)

load_dotenv()
DB_CONNECTION_URL = os.getenv("DB_CONNECTION_URL")


@pytest.fixture
def setup_database():
    """Fixture to set up the database with test data"""
    # Setup test connection
    engine = create_engine(DB_CONNECTION_URL)

    test_session_maker = sessionmaker(bind=engine)

    test_session = test_session_maker()

    # Delete the existing rows in the bazels table
    test_session.execute(delete(Bazel))

    # Populate test database
    bazels = [
        "Ik ben een banaan",
        "Als mijn oma wielen had was ze een fiets",
        "Rimmstein",
        "Mijn haar is in de waar",
        "Rooi vlag of niet, Patrick ga zwemmen!",
    ]

    for bazel in bazels:
        # Generate content hash
        content_hash = hashlib.sha256(bazel.encode("utf-8")).hexdigest()

        # Create bazel object
        bazel = Bazel(content=bazel, content_hash=content_hash)

        # Add bazel object
        test_session.add(bazel)
        test_session.commit()

    yield test_session
