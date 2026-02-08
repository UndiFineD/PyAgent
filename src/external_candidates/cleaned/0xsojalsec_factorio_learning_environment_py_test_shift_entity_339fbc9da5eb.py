# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_factorio_learning_environment.py\tests.py\actions.py\test_shift_entity_339fbc9da5eb.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-factorio-learning-environment\tests\actions\_test_shift_entity.py

import pytest

from entities import Direction, Position

from game_types import Prototype


@pytest.fixture()
def game(instance):
    instance.reset()

    yield instance.namespace

    instance.reset()


def test_shift_entity(game):
    """

    Place a boiler at (0, 0)

    :param game:

    :return:

    """

    # boilers_in_inventory = game.inspect_inventory()[Prototype.Pipe]

    entity = game.place_entity(Prototype.StoneFurnace, position=Position(x=5, y=0))

    entity = game.shift_entity(entity, Direction.RIGHT, distance=10)

    assert entity
