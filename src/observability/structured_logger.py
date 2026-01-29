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


"""
StructuredLogger: JSON-based logging for Phase 144 observability.
Ensures machine-readable logs with mandatory AgentID and TraceID fields.
"""

from __future__ import annotations

import contextlib
import gzip
import json
import logging
import re
import shutil
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Pattern

from src.core.base.common.file_system_core import FileSystemCore
from src.core.base.lifecycle.version import VERSION

# Rust acceleration for hot-path logging
try:
    import rust_core as rc

    _RUST_ACCEL = True
except ImportError:
    rc = None  # type: ignore[assignment]
    _RUST_ACCEL = False

__version__: str = VERSION


class StructuredLogger:
    """JSON logger for PyAgent swarm observability.
    Phase 277: Added log hygiene with automated GZIP compression.
    """

    # regex for sensitive data masking (Phase 227)
    SENSITIVE_PATTERNS: list[Pattern[str]] = [
        re.compile(r"sk-[a-zA-Z0-9]{32,}"),  # OpenAI Keys
        re.compile(r"Bearer\s+[a-zA-Z0-9\-\._~+/]+=*"),  # Bearer Tokens
        re.compile(r"gh[ps]_[a-zA-Z0-9]{36}"),  # GitHub Tokens
    ]

    def __init__(
        self,
        agent_id: str,
        trace_id: str | None = None,
        log_file: str = "data/logs/structured.json",
    ) -> None:
        self.agent_id: str = agent_id
        self.trace_id: str = trace_id or f"trace_{int(time.time())}"
        self.log_file = Path(log_file)
        self._fs = FileSystemCore()
        self._ensure_log_dir()

    def _ensure_log_dir(self) -> None:
        self._fs.ensure_directory(self.log_file.parent)
        # Phase 277: Compress if > 100MB
        if self.log_file.exists() and self.log_file.stat().st_size > 100 * 1024 * 1024:
            self._compress_logs()

    def _compress_logs(self) -> None:
        """Compresses current log file to .json.gz (Phase 277)."""
        timestamp: str = datetime.now().strftime("%Y%m%d_%H%M%S")
        compressed_file: Path = self.log_file.with_name(f"{self.log_file.stem}_{timestamp}.json.gz")
        logging.info(f"StructuredLogger: Compressing log file ({self.log_file.name}) to {compressed_file.name}")

        try:
            with open(self.log_file, 'rb') as f_in:
                with gzip.open(compressed_file, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            self._fs.delete(self.log_file)  # Delete original
        except OSError as e:  # pylint: disable=broad-exception-caught, unused-variable
            logging.error(f"StructuredLogger compression failed: {e}")
            import traceback
            traceback.print_exc()

    def _mask_sensitive(self, text: str) -> str:
        """Automated masking for API keys and tokens (Phase 227)."""
        # Use Rust acceleration when available (2-3x faster)
        if _RUST_ACCEL and rc is not None:
            with contextlib.suppress(Exception):
                return rc.mask_sensitive_logs(text)
        # Python fallback
        masked: str = text
        for pattern in self.SENSITIVE_PATTERNS:
            masked = pattern.sub("[REDACTED]", masked)
        return masked

    def log(self, level: str, message: str, **kwargs: Any) -> None:
        """Log a structured entry."""
        timestamp: str = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

        # Fast path: Use Rust for building the log entry (includes masking)
        if _RUST_ACCEL and rc is not None:
            with contextlib.suppress(Exception):
                extra_json: str | None = json.dumps(kwargs) if kwargs else None
                entry_json = rc.build_log_entry_rust(
                    timestamp,
                    self.agent_id,
                    self.trace_id,
                    level,
                    message,
                    extra_json,
                )
                # Console logging (quick)
                std_logger: logging.Logger = logging.getLogger(f"PyAgent.{self.agent_id}")
                log_func: Any | Callable[..., None] = getattr(std_logger, level.lower(), std_logger.info)
                log_func(f"[{self.agent_id}] {message[:200]}")

                # File write
                try:
                    with open(self.log_file, "a", encoding="utf-8") as f:
                        f.write(entry_json + "\n")
                except OSError as e:  # pylint: disable=broad-exception-caught, unused-variable
                    logging.error(f"StructuredLogger failed to write: {e}")
                    import traceback
                    traceback.print_exc()
                return

        # Python fallback path
        clean_message: str = self._mask_sensitive(message)
        clean_kwargs: dict[str, str | Any] = {k: (self._mask_sensitive(str(v)) if isinstance(v, str) else v) for k, v in kwargs.items()}

        entry = {
            "timestamp": timestamp,
            "agent_id": self.agent_id,
            "trace_id": self.trace_id,
            "level": level.upper(),
            "message": clean_message,
            **clean_kwargs,
        }

        # Also log to standard logging for console visibility
        std_logger: logging.Logger = logging.getLogger(f"PyAgent.{self.agent_id}")
        log_func: Any | Callable[..., None] = getattr(std_logger, level.lower(), std_logger.info)
        log_func(f"[{self.agent_id}] {clean_message} {json.dumps(clean_kwargs) if clean_kwargs else ''}")

        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
        except OSError as e:  # pylint: disable=broad-exception-caught, unused-variable
            logging.error(f"StructuredLogger failed to write: {e}")
            import traceback
            traceback.print_exc()

    def info(self, message: str, **kwargs: Any) -> None:
        """Log an info message."""
        self.log("info", message, **kwargs)

    def error(self, message: str, **kwargs: Any) -> None:
        """Log an error message."""
        self.log("error", message, **kwargs)

    def warning(self, message: str, **kwargs: Any) -> None:
        """Log a warning message."""
        self.log("warning", message, **kwargs)

    def debug(self, message: str, **kwargs: Any) -> None:
        """Log a debug message."""
        self.log("debug", message, **kwargs)

    def success(self, message: str, **kwargs: Any) -> None:
        """Log a success message."""
        self.log("success", message, **kwargs)
