import asyncio

import runtime_py as runtime


def test_sleep_delay() -> None:
    """Test that runtime.sleep waits for at least the specified duration."""
    # check that sleep waits at least the given duration

    async def inner() -> None:
        """Measure elapsed time to verify sleep duration."""
        start = asyncio.get_event_loop().time()
        await runtime.sleep(50)  # 50 ms
        elapsed = asyncio.get_event_loop().time() - start
        assert elapsed >= 0.04  # allow small jitter

    asyncio.run(inner())
