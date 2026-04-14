import asyncio

import pytest

from runtime_py import emit, on


@pytest.mark.asyncio
async def test_event_bus() -> None:
    """Test that the event bus can register handlers and emit events to them."""
    events: list[tuple[str, int]] = []

    async def handler1(x: int) -> None:
        """Example handler that appends to the events list."""
        events.append(("h1", x))

    async def handler2(x: int) -> None:
        """Another handler that appends to the events list."""
        events.append(("h2", x))

    on("foo", handler1)
    on("foo", handler2)

    emit("foo", 42)
    # allow the spawned tasks to run
    await asyncio.sleep(0.01)

    assert ("h1", 42) in events
    assert ("h2", 42) in events
