# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_factorio_learning_environment.py\tests.py\actions.py\test_get_research_progress_52e52ed512bc.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-factorio-learning-environment\tests\actions\test_get_research_progress.py

import pytest

from fle.env.game_types import Technology


@pytest.fixture()
def game(configure_game):
    return configure_game(
        inventory={"assembling-machine-1": 1},
        merge=True,
        all_technologies_researched=False,
    )


def test_get_research_progress_automation(game):
    ingredients = game.get_research_progress(Technology.Automation)

    assert ingredients[0].count == 10


def test_get_research_progress_none_fail(game):
    try:
        game.get_research_progress()

    except:
        assert True

        return

    assert False, "Need to set research before calling get_research_progress() without an argument"


def test_get_research_progress_none(game):
    ingredients1 = game.set_research(Technology.Automation)

    ingredients2 = game.get_research_progress()

    assert len(ingredients1) == len(ingredients2)
