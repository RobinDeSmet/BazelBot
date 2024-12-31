from src.database import bazels_db_functions
from src.database.models import Bazel
from src.controllers import bazels_controller
from tests.conftest import TOTAL_NR_BAZELS, MAX_BAZELS_IN_CONTEXT


def test_database_connection(setup_database):
    # Test to make sure that we can connect to the database
    session = setup_database

    amount_of_bazels = session.query(Bazel).count()

    print(f"There are {amount_of_bazels} bazels in the test database")

    assert amount_of_bazels == TOTAL_NR_BAZELS


def test_generate_bazel_context(setup_database):
    # Test to make sure that the bazel context is correctly generated
    session = (
        setup_database  # You have to give the test session to the controller functions!
    )

    # Stress test the bazelcontext generation
    for index in range(10):
        print(f"Stress test iteration {index}")

        context = bazels_controller.generate_bazel_context(session=session)

        assert context
        assert len(context.split("\n")) == 11

    # Test bazelcontext with nr_bazels < max allowed nr of bazels in context
    context = bazels_controller.generate_bazel_context(nr_bazels=2, session=session)

    print(f"NR_BAZELS=2 context: \n{context}")
    assert context
    assert len(context.split("\n")) == 3

    # Test bazelcontext with nr_bazels > max allowed nr of bazels in context
    context = bazels_controller.generate_bazel_context(nr_bazels=100, session=session)

    print(f"NR_BAZELS=25 context: \n{context}")

    assert context
    assert len(context.split("\n")) == MAX_BAZELS_IN_CONTEXT + 1


def test_bazel_crud_works(setup_database):
    # Get test session
    session = setup_database

    bazel_content = "New bazel that has to be added!!"

    # Add bazel
    result = bazels_db_functions.add(bazel_content, session)

    assert result == 1

    # Add duplicate bazel
    result = bazels_db_functions.add(bazel_content, session)

    assert result == 0

    # Retrieve bazel
    bazel = bazels_db_functions.get(bazel_content, session)

    assert bazel.content_hash == bazels_db_functions.generate_content_hash(
        bazel_content
    )

    # List bazels
    bazels = bazels_db_functions.list(session)

    assert len(bazels) == TOTAL_NR_BAZELS + 1

    # Cleanup
    bazels_db_functions.delete(bazel_content, session)

    # Check if bazel is successfully deleted
    assert bazels_db_functions.count(session) == TOTAL_NR_BAZELS
