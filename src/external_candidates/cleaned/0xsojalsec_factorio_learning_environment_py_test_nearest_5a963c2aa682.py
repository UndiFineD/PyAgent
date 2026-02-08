# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_factorio_learning_environment.py\tests.py\actions.py\test_nearest_5a963c2aa682.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-factorio-learning-environment\tests\actions\test_nearest.py

from fle.env.entities import Position

from fle.env.game_types import Resource


def test_nearest_resource(game):
    """

    Test distance to the nearest coal resource.

    :param game:

    :return:

    """

    coal: Position = game.nearest(Resource.Coal)

    assert coal.y == -0.5

    assert coal.x == 15.5


def test_move_to_nearest(game):
    """

    Test that when the player moves to the nearest water resource, the nearest water resource remains the same.

    :param game:

    :return:

    """

    water: Position = game.nearest(Resource.Water)

    game.move_to(water)

    assert abs(water.x - game.nearest(Resource.Water).x) <= 1
