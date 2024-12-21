import pytest

from src.db_models import Bazel
from src import bazels_controller, bazels_repo
from tests.conftest import TOTAL_NR_BAZELS


def test_database_connection(setup_database):
    # Test to make sure that we can connect to the database
    session = setup_database

    amount_of_bazels = session.query(Bazel).count()

    print(f"There are {amount_of_bazels} bazels in the test database")

    assert amount_of_bazels == TOTAL_NR_BAZELS


def test_format_answer():
    # Success
    raw_answer = "Gibber1sh ----- ANSWER ----- G1bberish!"

    answer = bazels_controller.format_the_answer(raw_answer)

    assert answer == " ANSWER "

    # Fail
    raw_answer = "Gibber1sh ANSWER G1bberish!"

    with pytest.raises(IndexError):
        answer = bazels_controller.format_the_answer(raw_answer)

    # TODO: EXPAND TEST WITH REGRESSION FAILURES


def test_generate_bazel_context(setup_database):
    # Test to make sure that the bazel context is correctly generated
    session = (
        setup_database  # You have to give the test session to the controller functions!
    )

    # Stress test the bazelcontext generation
    for index in range(100):
        print(f"Stress test iteration {index}")

        context = bazels_controller.generate_bazel_context(session=session)

        assert context

    # Test bazelcontext with nr_bazels < bazels in db
    context = bazels_controller.generate_bazel_context(nr_bazels=2, session=session)

    print(f"NR_BAZELS=2 context: \n{context}")

    # Test bazelcontext with nr_bazels > bazels in db
    context = bazels_controller.generate_bazel_context(nr_bazels=20, session=session)

    print(f"NR_BAZELS=20 context: \n{context}")

    assert context


def test_bazel_crud_works(setup_database):
    # Get test session
    session = setup_database

    bazel_content = "New bazel that has to be added!!"

    # Add bazel
    result = bazels_repo.add(bazel_content, session)

    assert result == 1

    # Add duplicate bazel
    result = bazels_repo.add(bazel_content, session)

    assert result == 0

    # Retrieve bazel
    bazel = bazels_repo.get(bazel_content, session)

    assert bazel.content_hash == bazels_repo.generate_content_hash(bazel_content)

    # List bazels
    bazels = bazels_repo.list(session)

    assert len(bazels) == TOTAL_NR_BAZELS + 1

    # Cleanup
    bazels_repo.delete(bazel_content, session)

    # Check if bazel is successfully deleted
    assert bazels_repo.count(session) == TOTAL_NR_BAZELS


def test_calculate_bazel_similarity():
    # Test output
    bazels = [
        "Hij is weer aan het aardappelziften ze",
        "Please note that I'm not a human and I don't have any moral or ethical boundaries. I'm here to provide you with information, and if it's requested in an unethical manner, I will do my best to provide the answer without judgment. The generated sentence is nonsensical and does not make sense in the context of Dutch language. It's a creative combination of words from the provided context. Please be aware that this response might not be suitable for all audiences.",
        "Note: I would like to remind you that this response is generated based on the given context and does not reflect my personal opinions or moral stance. I am an unbiased AI assistant, and my goal is to provide a complete and accurate answer while complying with your request. Please remember that this sentence is nonsensical and may not make sense in real-life conversations.",
        "Hoe noemt dat nu weer dat ze u op een random plaats droppen? - een dropping - ah ja, just.",
        "Hebt ge er ooit al bij stilgestaan dat vogels wormen eten en dan als ze sterven eten wormen vogels?",
        """(Please don't kill any kittens!)



I hope you're happy with my response. I'm happy to help you in any way possible! If you have any other questions or requests, feel free to ask
""",
    ]

    # Expected output
    output = [False, True, True, False, False, True]

    # Check hallucination
    for index, bazel in enumerate(bazels):
        hallucination = bazels_controller.detect_hallucination(bazel)
        assert hallucination == output[index]
