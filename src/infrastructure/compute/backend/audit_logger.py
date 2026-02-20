#!/usr/bin/env python3
from __future__ import annotations
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


import json
import logging
import threading
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class AuditLogger:
    """Logs backend requests for audit and compliance.
    Records request metadata, responses, and timing for
    audit trail and compliance requirements.

    Example:
        audit = AuditLogger()
        audit.log_request("github-models", "prompt", "response", 150)
    """

    def __init__(self, log_file: Path | None = None) -> None:
        """Initialize audit logger.
        Args:
            log_file: Path to audit log file.
        """
        self.log_file = log_file
        self._lock = threading.Lock()


    def log_request(
        self,
        backend: str,
        prompt: str,
        response: str,
        latency_ms: int,
        success: bool = True,
        request_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """Log a request for audit.
        Args:
            backend: Backend used.
            prompt: Request prompt (may be truncated for privacy).
            response: Response received (may be truncated).
            latency_ms: Request latency.
            success: Whether request succeeded.
            request_id: Optional request ID.
            metadata: Additional metadata.
        """
        entry: dict[str, Any] = {
            "timestamp": datetime.now(UTC).isoformat(),
            "request_id": request_id or str(uuid.uuid4()),
            "backend": backend,
            "prompt_length": len(prompt),
            "prompt_preview": prompt[:100] + "..." if len(prompt) > 100 else prompt,
            "response_length": len(response),
            "latency_ms": latency_ms,
            "success": success,
            "metadata": metadata or {},
        }
        with self._lock:
            if self.log_file:
                try:
                    with open(self.log_file, "a", encoding="utf-8") as f:
                        f.write(json.dumps(entry) + "\n")
                except OSError as e:
                    logging.warning(f"Failed to write audit log: {e}")
            logging.debug(f"Audit: {entry['request_id']} - {backend} - {latency_ms}ms")


    def get_recent_entries(self, count: int = 100) -> list[dict[str, Any]]:
        """Get recent audit log entries.
        
        Args:
            count: Number of entries to return.

        Returns:
            List[Dict]: Recent audit entries.
        """
        if not self.log_file or not self.log_file.exists():
            return []

        entries: list[dict[str, Any]] = []
        with self._lock:
            try:
                with open(self.log_file, encoding="utf-8") as f:
                    for line in f:
                        try:
                            entries.append(json.loads(line.strip()))
                        except json.JSONDecodeError:
                            continue
            except OSError:
                return []

        return entries[-count:]
