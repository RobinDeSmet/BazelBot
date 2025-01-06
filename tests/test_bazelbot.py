from src.database import bazels_db_functions
from src.database.models import Bazel
from src.controllers import bazels_controller
from src.prompts.bazel_flavours import (
    BAZEL_IMAGE_FLAVOURS,
    BAZEL_FLAVOURS,
)
from src.utils.custom_types import BazelFlavour, BazelType
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


def test_random_bazel_flavour_generation():
    selected_text_flavours = []
    selected_image_flavours = []
    for i in range(20):
        # Generate bazel flavour
        random_flavour = bazels_controller.get_random_bazel_flavour()
        print(f"{random_flavour}\n")

        # Check
        assert random_flavour.bazel_flavour_name in BAZEL_FLAVOURS

        RAW_FLAVOUR = BAZEL_FLAVOURS[random_flavour.bazel_flavour_name]

        assert random_flavour.bazel_instructions
        assert random_flavour.bazel_instructions == RAW_FLAVOUR["bazel_instructions"]

        RAW_IMAGE_INSTRUCTIONS = RAW_FLAVOUR["image_instructions"]

        if RAW_IMAGE_INSTRUCTIONS.lower() == "random":
            assert random_flavour.image_flavour_name in BAZEL_IMAGE_FLAVOURS
            assert random_flavour.image_instructions
            assert (
                random_flavour.image_instructions
                == BAZEL_IMAGE_FLAVOURS[random_flavour.image_flavour_name][
                    "instructions"
                ]
            )
        else:
            assert (
                random_flavour.image_flavour_name == random_flavour.bazel_flavour_name
            )
            assert random_flavour.image_flavour_name in BAZEL_FLAVOURS
            assert random_flavour.image_instructions
            assert random_flavour.image_instructions == RAW_IMAGE_INSTRUCTIONS

        if i < 5:
            selected_text_flavours.append(random_flavour.bazel_flavour_name)
            selected_image_flavours.append(random_flavour.image_flavour_name)

    assert len(set(selected_image_flavours)) == 5
    assert len(set(selected_text_flavours)) == 5
    assert len(bazels_controller.FILTER_TEXT_FLAVOURS) == 10
    assert len(bazels_controller.FILTER_IMAGE_FLAVOURS) == 5


def test_format_prompt(setup_database):
    context = bazels_controller.generate_bazel_context()
    user_context = "random words"

    random_flavour: BazelFlavour = bazels_controller.get_random_bazel_flavour()
    prompt_bazel = bazels_controller.format_prompt(
        context=context,
        bazel_flavour=random_flavour,
        user_context=user_context,
        bazel_type=BazelType.NORMAL,
    )
    print(prompt_bazel)

    assert prompt_bazel
    assert context in prompt_bazel
    assert user_context not in prompt_bazel
    assert random_flavour.bazel_instructions in prompt_bazel

    random_flavour: BazelFlavour = bazels_controller.get_random_bazel_flavour()
    prompt_custom_bazel = bazels_controller.format_prompt(
        context=context,
        bazel_flavour=random_flavour,
        user_context=user_context,
        bazel_type=BazelType.CUSTOM,
    )
    print(prompt_custom_bazel)

    assert prompt_custom_bazel
    assert context in prompt_custom_bazel
    assert user_context in prompt_custom_bazel
    assert random_flavour.bazel_instructions in prompt_custom_bazel
