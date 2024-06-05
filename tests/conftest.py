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
TOTAL_NR_BAZELS = 12


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
        "Misschien betekent die zak frieten dat ik een teelbal teveel heb",
        "Ne meter bierplank",
        "Zijn tepels ken ik blind!",
        "Ik ben kapitein en ik bel vanop de scheve schajuit",
        "Rooi vlag of niet, Patrick ga zwemmen!",
        "Zijn spaghetti begon uit zijn broek te vallen en hij was aan het panikeren",
        "Mensen die naar een dure schoenenwinkel gingen hadden meer kans om op de space titanic te zitten",
        "Zijn luchtbiertechniek is geweldig",
        "Piemelini",
        "Die koe is verkouden, hij heeft koerona",
        "Als mijn kat een koe was kon ik ze melken aan mijn stoof!",
        "Als mijn oma wielen had was ze een fiets.",
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
