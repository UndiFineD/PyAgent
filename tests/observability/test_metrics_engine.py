import asyncio

import pytest

from observability.stats import metrics_engine  # type: ignore[import-not-found]


@pytest.mark.asyncio
async def test_async_tick_loop() -> None:
    """Test that the metrics engine's asynchronous tick loop can run and update the counter."""
    # reset state
    metrics_engine.counter = 0

    # start the migrated asynchronous loop
    metrics_engine.start_async_loop()

    # allow the loop a few ticks (each tick sleeps ~100ms)
    await asyncio.sleep(0.35)
    assert metrics_engine.counter >= 2
