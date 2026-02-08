# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_factorio_learning_environment.py\tests.py\actions.py\test_request_path_f59ccaf71946.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-factorio-learning-environment\tests\actions\test_request_path.py

from fle.env.entities import Position


def test_path(game):
    """

    Get a path from (0, 0) to (10, 0)

    :param game:

    :return:

    """

    path = game._request_path(Position(x=0, y=0), Position(x=10, y=0))

    assert path
