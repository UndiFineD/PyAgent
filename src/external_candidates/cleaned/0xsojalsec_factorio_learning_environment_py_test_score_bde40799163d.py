# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_factorio_learning_environment.py\tests.py\actions.py\test_score_bde40799163d.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-factorio-learning-environment\tests\actions\test_score.py


def test_get_score(game):
    score, _ = game.score()

    assert isinstance(score, int)
