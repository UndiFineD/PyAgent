import asyncio

import src.runtime as _rt


async def inner() -> None:
    """Test that spawn_task can run a simple async function."""
    event = asyncio.Event()

    async def worker() -> None:
        """Example worker that sets the event."""
        event.set()

    _rt.spawn_task(worker())
    await asyncio.wait_for(event.wait(), timeout=1.0)


if __name__ == "__main__":
    asyncio.run(inner())
    # shutdown tokio runtime to avoid threads touching Python after
    # interpreter exit

    _rt._shutdown_runtime()
    print("success")
