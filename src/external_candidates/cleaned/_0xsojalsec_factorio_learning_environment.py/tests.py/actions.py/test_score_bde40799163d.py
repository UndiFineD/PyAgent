# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-factorio-learning-environment\tests\actions\test_score.py
def test_get_score(game):
    score, _ = game.score()
    assert isinstance(score, int)
