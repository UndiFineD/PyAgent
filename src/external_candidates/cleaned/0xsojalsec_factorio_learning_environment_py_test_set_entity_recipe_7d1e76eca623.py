# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_factorio_learning_environment.py\tests.py\actions.py\test_set_entity_recipe_7d1e76eca623.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-factorio-learning-environment\tests\actions\test_set_entity_recipe.py

import pytest

from fle.env.entities import Position

from fle.env.game_types import Prototype


@pytest.fixture()
def game(configure_game):
    return configure_game(inventory={"assembling-machine-1": 1})


def test_set_entity_recipe(game):
    # Place an assembling machine

    assembling_machine = game.place_entity(Prototype.AssemblingMachine1, position=Position(x=0, y=0))

    # Set a recipe for the assembling machine

    assembling_machine = game.set_entity_recipe(assembling_machine, Prototype.IronGearWheel)

    # Assert that the recipe of the assembling machine has been updated

    prototype_name, _ = Prototype.IronGearWheel.value

    assert assembling_machine.recipe == prototype_name
