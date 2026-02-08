# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\agents_generic.py\livekit_agents.py\livekit.py\agents.py\ipc.py\inference_executor_9dc01b210da0.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\agents_generic\livekit-agents\livekit\agents\ipc\inference_executor.py

from __future__ import annotations

from typing import Protocol


class InferenceExecutor(Protocol):
    async def do_inference(self, method: str, data: bytes) -> bytes | None: ...
