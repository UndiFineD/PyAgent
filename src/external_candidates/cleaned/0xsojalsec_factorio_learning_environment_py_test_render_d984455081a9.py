# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_factorio_learning_environment.py\tests.py\actions.py\test_render_d984455081a9.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-factorio-learning-environment\tests\actions\test_render.py

import pytest

from fle.env.entities import Layer, Position

from fle.env.game_types import Prototype


@pytest.fixture()
def game(configure_game):
    return configure_game(
        inventory={
            "iron-chest": 1,
            "small-electric-pole": 20,
            "iron-plate": 10,
            "assembling-machine-1": 1,
            "pipe-to-ground": 10,
            "pipe": 30,
            "transport-belt": 50,
            "underground-belt": 30,
        }
    )


def test_basic_render(game):
    game.place_entity(Prototype.IronChest, position=Position(x=0, y=0))

    game.connect_entities(
        Position(x=0, y=-2),
        Position(x=15, y=5),
        {Prototype.Pipe, Prototype.UndergroundPipe},
    )

    game.connect_entities(Position(x=0, y=-10), Position(x=15, y=-10), {Prototype.SmallElectricPole})

    image = game._render(position=Position(x=0, y=5), layers=Layer.ALL)

    image.show()

    pass
