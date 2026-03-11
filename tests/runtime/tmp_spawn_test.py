import asyncio

import runtime


async def inner() -> None:
    """Test that spawn_task can run a simple async function."""
    event = asyncio.Event()

    async def worker() -> None:
        """Example worker that sets the event."""
        event.set()

    runtime.spawn_task(worker())
    await asyncio.wait_for(event.wait(), timeout=1.0)

if __name__ == "__main__":
    asyncio.run(inner())
    # shutdown tokio runtime to avoid threads touching Python after
    # interpreter exit
    import runtime as _rt

    _rt._shutdown_runtime()
    print("success")
