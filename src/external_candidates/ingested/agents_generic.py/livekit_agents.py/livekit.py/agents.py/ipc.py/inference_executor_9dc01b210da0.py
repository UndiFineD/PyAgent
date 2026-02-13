# Extracted from: C:\DEV\PyAgent\.external\agents_generic\livekit-agents\livekit\agents\ipc\inference_executor.py
from __future__ import annotations

from typing import Protocol


class InferenceExecutor(Protocol):
    async def do_inference(self, method: str, data: bytes) -> bytes | None: ...
