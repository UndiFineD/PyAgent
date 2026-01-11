#!/usr/bin/env python3

"""Auto-extracted class from agent_backend.py"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from queue import PriorityQueue
from typing import Any, Callable, Dict, List, Optional, Tuple
import hashlib
import json
import logging
import os
import re
import subprocess
import threading
import time
import uuid

class AuditLogger:
    """Logs backend requests for audit and compliance.

    Records request metadata, responses, and timing for
    audit trail and compliance requirements.

    Example:
        audit=AuditLogger()
        audit.log_request("github-models", "prompt", "response", 150)
    """

    def __init__(self, log_file: Optional[Path] = None) -> None:
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
        request_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
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

        entry: Dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
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
                except IOError as e:
                    logging.warning(f"Failed to write audit log: {e}")
            logging.debug(f"Audit: {entry['request_id']} - {backend} - {latency_ms}ms")

    def get_recent_entries(self, count: int = 100) -> List[Dict[str, Any]]:
        """Get recent audit log entries.

        Args:
            count: Number of entries to return.

        Returns:
            List[Dict]: Recent audit entries.
        """
        if not self.log_file or not self.log_file.exists():
            return []

        entries: List[Dict[str, Any]] = []
        with self._lock:
            try:
                with open(self.log_file, "r", encoding="utf-8") as f:
                    for line in f:
                        try:
                            entries.append(json.loads(line.strip()))
                        except json.JSONDecodeError:
                            continue
            except IOError:
                return []

        return entries[-count:]
