# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_factorio_learning_environment.py\tests.py\actions.py\test_get_prototype_recipe_5a570cc7fe6d.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-factorio-learning-environment\tests\actions\test_get_prototype_recipe.py

import pytest

from fle.env.game_types import Prototype


@pytest.fixture()
def game(configure_game):
    return configure_game(inventory={"assembling-machine-1": 1})


def test_get_recipe(game):
    recipe = game.get_prototype_recipe(Prototype.IronGearWheel)

    assert recipe.ingredients[0].name == "iron-plate"

    assert recipe.ingredients[0].count == 2
