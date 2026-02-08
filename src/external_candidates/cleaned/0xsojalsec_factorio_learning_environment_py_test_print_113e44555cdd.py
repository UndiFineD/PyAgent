# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_factorio_learning_environment.py\tests.py\actions.py\test_print_113e44555cdd.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-factorio-learning-environment\tests\actions\test_print.py


def test_print_tuple(game):
    """

    Print a tuple

    """

    r = game.print("Hello", "World", (1, 2, 3))

    assert r == "Hello\tWorld\t(1, 2, 3)"
