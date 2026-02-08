# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_factorio_learning_environment.py\tests.py\actions.py\test_sleep_991cb4c8a197.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-factorio-learning-environment\tests\actions\test_sleep.py

import time

import pytest


@pytest.mark.parametrize("speed", range(1, 10))  # 10 independent items
def test_sleep(game, speed):
    game.instance.set_speed(speed)

    start = time.time()

    game.sleep(10)

    elapsed = time.time() - start

    assert elapsed * speed - 10 < 1, f"Sleep behaved unexpectedly at speed {speed}"
