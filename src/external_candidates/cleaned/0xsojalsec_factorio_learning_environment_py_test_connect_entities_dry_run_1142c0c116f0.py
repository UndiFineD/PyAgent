# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_factorio_learning_environment.py\tests.py\actions.py\test_connect_entities_dry_run_1142c0c116f0.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-factorio-learning-environment\tests\actions\test_connect_entities_dry_run.py

import pytest

from fle.env.entities import Position

from fle.env.game_types import Prototype


@pytest.fixture()
def game(configure_game):
    return configure_game(inventory={"transport-belt": 12})


def test_dry_run(game):
    position_1 = Position(x=3, y=1)

    position_2 = Position(x=2, y=4)

    belts = game.connect_entities(position_1, position_2, Prototype.TransportBelt, dry_run=True)

    assert game.inspect_inventory()[Prototype.TransportBelt] == 12

    assert len(game.get_entities()) == 0

    assert isinstance(belts, dict)

    assert belts["number_of_entities_available"] == 12

    assert belts["number_of_entities_required"] < 12

    position_1 = Position(x=0, y=0)

    position_2 = Position(x=0, y=25)

    belts = game.connect_entities(position_1, position_2, Prototype.TransportBelt, dry_run=True)

    assert game.inspect_inventory()[Prototype.TransportBelt] == 12

    assert len(game.get_entities()) == 0

    assert isinstance(belts, dict)

    assert belts["number_of_entities_available"] == 12

    assert belts["number_of_entities_required"] > 12


def test_connect_without_enough(game):
    position_1 = Position(x=0, y=0)

    position_2 = Position(x=0, y=25)

    try:
        belts = game.connect_entities(position_1, position_2, Prototype.TransportBelt)

    except Exception as e:
        exception_message = str(e)

        assert (
            "You do not have enough transport-belt in you inventory to complete this connection. Required number - 26, Available in inventory - 12"
            in exception_message
        )

        pass

    assert game.inspect_inventory()[Prototype.TransportBelt] == 12

    assert len(game.get_entities()) == 0

    position_1 = Position(x=3, y=1)

    position_2 = Position(x=0, y=4)

    belts = game.connect_entities(position_1, position_2, Prototype.TransportBelt)

    assert game.inspect_inventory()[Prototype.TransportBelt] < 12

    assert len(game.get_entities()) != 0

    assert len(belts.belts) != 0
