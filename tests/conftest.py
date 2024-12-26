import pytest
import hashlib
import os

from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, delete

from src.db_models import Bazel

load_dotenv()

MAX_BAZELS_IN_CONTEXT = int(os.getenv("MAX_BAZELS_IN_CONTEXT"))
DB_CONNECTION_URL = os.getenv("DB_CONNECTION_URL")
TOTAL_NR_BAZELS = 50


@pytest.fixture(scope="function")
def setup_database():
    """Fixture to set up the database with test data."""
    # Setup test connection
    engine = create_engine(DB_CONNECTION_URL)
    TestSession = sessionmaker(bind=engine)
    test_session = TestSession()

    try:
        # Clear existing data in the bazels table
        test_session.execute(delete(Bazel))

        # Populate test database
        try:
            with open("tests/test_data.txt", "r") as file:
                bazels = file.readlines()

            bazel_objects = [
                Bazel(
                    content=bazel.strip(),
                    content_hash=hashlib.sha256(
                        bazel.strip().encode("utf-8")
                    ).hexdigest(),
                )
                for bazel in bazels
            ]

            # Add all records at once
            test_session.add_all(bazel_objects)
            test_session.commit()
        except FileNotFoundError:
            pytest.fail("Test data file not found: tests/test_data.txt")
        except Exception as e:
            pytest.fail(f"An error occurred while reading test data: {e}")

        # Yield the session to the test
        yield test_session
    finally:
        # Cleanup after test
        test_session.execute(delete(Bazel))
        test_session.commit()
        test_session.close()
