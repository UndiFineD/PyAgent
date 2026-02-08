# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_factorio_learning_environment.py\tests.py\connect.py\test_connect_walls_2b0196fa33cb.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-factorio-learning-environment\tests\connect\test_connect_walls.py

import pytest

from fle.env.entities import Position

from fle.env.game_types import Prototype


@pytest.fixture()
def game(instance):
    instance.initial_inventory = {
        **instance.initial_inventory,
        "stone-wall": 100,
    }

    instance.reset()

    yield instance.namespace

    # instance.reset()


def test_connect_wall_line(game):
    start_position = Position(x=0, y=0)

    end_position = Position(x=5, y=0)

    wall = game.connect_entities(start_position, end_position, connection_type=Prototype.StoneWall)

    assert len(wall.entities) == 6
