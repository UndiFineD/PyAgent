# Extracted from: C:\DEV\PyAgent\.external\cache\work\copilot_tmp\chunk_0_test_print.py
# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-factorio-learning-environment\tests\actions\test_print.py
# NOTE: extracted with static-only rules; review before use


def test_print_tuple(game):
    """

    Print a tuple

    """

    r = game.print("Hello", "World", (1, 2, 3))

    assert r == "Hello\tWorld\t(1, 2, 3)"
