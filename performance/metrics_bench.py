#!/usr/bin/env python3
"""Simple benchmark comparing sync loop vs runtime-based async loop."""
import asyncio
import time

from observability.stats import metrics_engine


def sync_bench(duration: float = 1.0) -> int:
    """Run a tight loop for the given duration and count iterations."""
    metrics_engine.counter = 0
    end = time.time() + duration
    while time.time() < end:
        metrics_engine.counter += 1
    return metrics_engine.counter


def async_bench(duration: float = 1.0) -> int:
    """Start an async loop that increments a counter, then wait for the duration."""
    metrics_engine.counter = 0

    metrics_engine.start_async_loop()

    async def waiter() -> None:
        await asyncio.sleep(duration)
    asyncio.run(waiter())
    return metrics_engine.counter


if __name__ == "__main__":
    print("sync result", sync_bench())
    print("async result", async_bench())
