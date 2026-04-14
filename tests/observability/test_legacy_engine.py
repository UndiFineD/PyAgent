import asyncio

import pytest

from observability.stats import legacy_engine


@pytest.mark.asyncio
async def test_legacy_engine_async_loop():
    """The migrated version should still increment the counter when started."""
    before = legacy_engine.get_count()
    legacy_engine.start_loop()  # schedule the async tick loop
    await asyncio.sleep(0.01)  # allow a tick to occur
    after = legacy_engine.get_count()
    assert after > before
