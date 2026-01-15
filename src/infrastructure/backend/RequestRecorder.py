#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Auto-extracted class from agent_backend.py"""

from __future__ import annotations
from src.core.base.version import VERSION
from .RecordedRequest import RecordedRequest
from typing import Any
import json
import threading
import time
import uuid

__version__ = VERSION







class RequestRecorder:
    """Records and replays requests for debugging and testing.

    Captures request / response pairs for later replay, enabling
    offline testing and debugging.

    Example:
        recorder=RequestRecorder()
        recorder.record("prompt", "github-models", "response", latency_ms=150)

        # Later, replay:
        for req in recorder.get_recordings():
            print(f"{req.prompt} -> {req.response}")
    """

    def __init__(self, max_recordings: int = 1000) -> None:
        """Initialize request recorder.

        Args:
            max_recordings: Maximum recordings to keep.
        """
        self.max_recordings = max_recordings
        self._recordings: list[RecordedRequest] = []
        self._lock = threading.Lock()

    def record(
        self,
        prompt: str,
        backend: str,
        response: str | None = None,
        latency_ms: int = 0,
        success: bool = True,
        metadata: dict[str, Any] | None = None,
    ) -> RecordedRequest:
        """Record a request.

        Args:
            prompt: Request prompt.
            backend: Backend used.
            response: Response received.
            latency_ms: Request latency.
            success: Whether request succeeded.
            metadata: Additional metadata.

        Returns:
            RecordedRequest: The recorded request.
        """
        recording = RecordedRequest(
            request_id=str(uuid.uuid4()),
            timestamp=time.time(),
            prompt=prompt,
            backend=backend,
            response=response,
            latency_ms=latency_ms,
            success=success,
            metadata=metadata or {},
        )

        with self._lock:
            self._recordings.append(recording)
            # Trim to max size
            if len(self._recordings) > self.max_recordings:
                self._recordings = self._recordings[-self.max_recordings:]

        return recording

    def get_recordings(
        self,
        backend: str | None = None,
        success_only: bool = False,
    ) -> list[RecordedRequest]:
        """Get recorded requests.

        Args:
            backend: Filter by backend.
            success_only: Only return successful requests.

        Returns:
            List[RecordedRequest]: Matching recordings.
        """
        with self._lock:
            recordings = self._recordings.copy()

        if backend:
            recordings = [r for r in recordings if r.backend == backend]
        if success_only:
            recordings = [r for r in recordings if r.success]

        return recordings

    def replay(self, request_id: str) -> RecordedRequest | None:
        """Get recording by ID for replay.

        Args:
            request_id: Recording ID.

        Returns:
            Optional[RecordedRequest]: Recording or None.
        """
        with self._lock:
            for recording in self._recordings:
                if recording.request_id == request_id:
                    return recording
        return None

    def export_recordings(self) -> str:
        """Export recordings as JSON.

        Returns:
            str: JSON string of recordings.
        """
        with self._lock:
            data: list[dict[str, Any]] = [
                {
                    "request_id": r.request_id,
                    "timestamp": r.timestamp,
                    "prompt": r.prompt,
                    "backend": r.backend,
                    "response": r.response,
                    "latency_ms": r.latency_ms,
                    "success": r.success,
                    "metadata": r.metadata,
                }
                for r in self._recordings
            ]
        return json.dumps(data, indent=2)

    def clear(self) -> int:
        """Clear all recordings.

        Returns:
            int: Number of recordings cleared.
        """
        with self._lock:
            count = len(self._recordings)
            self._recordings.clear()
        return count
