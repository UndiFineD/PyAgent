# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agents_generic.py\livekit_agents.py\livekit.py\agents.py\utils.py\aio.py\debug_925a2d120915.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agents_generic\livekit-agents\livekit\agents\utils\aio\debug.py

from __future__ import annotations

import asyncio

import time

from asyncio.base_events import _format_handle  # type: ignore

from typing import Any

from ...log import logger


def hook_slow_callbacks(slow_duration: float) -> None:
    _run = asyncio.events.Handle._run

    def instrumented(self: Any) -> Any:
        start = time.monotonic()

        val = _run(self)

        dt = time.monotonic() - start

        if dt >= slow_duration:
            logger.warning("Running %s took too long: %.2f seconds", _format_handle(self), dt)

        return val

    asyncio.events.Handle._run = instrumented  # type: ignore
