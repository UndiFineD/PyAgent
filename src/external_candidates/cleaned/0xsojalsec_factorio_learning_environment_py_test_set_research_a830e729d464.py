# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_factorio_learning_environment.py\tests.py\actions.py\test_set_research_a830e729d464.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-factorio-learning-environment\tests\actions\test_set_research.py

import pytest

from fle.env.game_types import Technology


@pytest.fixture()
def game(configure_game):
    return configure_game(all_technologies_researched=False)


def test_set_research(game):
    ingredients = game.set_research(Technology.Automation)

    assert ingredients[0].count == 10


def test_fail_to_research_locked_technology(game):
    try:
        game.set_research(Technology.Automation2)

    except Exception:
        assert True

        return

    assert False, "Was able to research locked technology. Expected exception."
