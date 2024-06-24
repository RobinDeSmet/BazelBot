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
TOTAL_NR_BAZELS = 50


@pytest.fixture
def setup_database():
    """Fixture to set up the database with test data"""
    # Setup test connection
    engine = create_engine(DB_CONNECTION_URL)

    test_session_maker = sessionmaker(bind=engine)

    test_session = test_session_maker()

    # Delete the existing rows in the bazels table
    test_session.execute(delete(Bazel))

    # # Populate test database
    with open("tests/test_data.txt", "r") as file:
        bazels = file.readlines()

        for bazel in bazels:
            # Remove end of line character
            bazel = bazel.replace("\n", "")

            # Generate content hash
            content_hash = hashlib.sha256(bazel.encode("utf-8")).hexdigest()

            # Create bazel object
            bazel = Bazel(content=bazel, content_hash=content_hash)

            # Add bazel object
            test_session.add(bazel)
            test_session.commit()

    yield test_session
