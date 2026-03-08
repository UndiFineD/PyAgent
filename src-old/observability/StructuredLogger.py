#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/observability/StructuredLogger.description.md

# StructuredLogger

**File**: `src\observability\StructuredLogger.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 13 imports  
**Lines**: 178  
**Complexity**: 10 (moderate)

## Overview

StructuredLogger: JSON-based logging for Phase 144 observability.
Ensures machine-readable logs with mandatory AgentID and TraceID fields.

## Classes (1)

### `StructuredLogger`

JSON logger for PyAgent swarm observability.
Phase 277: Added log hygiene with automated GZIP compression.

**Methods** (10):
- `__init__(self, agent_id, trace_id, log_file)`
- `_ensure_log_dir(self)`
- `_compress_logs(self)`
- `_mask_sensitive(self, text)`
- `log(self, level, message)`
- `info(self, message)`
- `error(self, message)`
- `warning(self, message)`
- `debug(self, message)`
- `success(self, message)`

## Dependencies

**Imports** (13):
- `__future__.annotations`
- `datetime.datetime`
- `datetime.timezone`
- `gzip`
- `json`
- `logging`
- `pathlib.Path`
- `re`
- `rust_core`
- `shutil`
- `src.core.base.Version.VERSION`
- `time`
- `typing.Any`

---
*Auto-generated documentation*
## Source: src-old/observability/StructuredLogger.improvements.md

# Improvements for StructuredLogger

**File**: `src\observability\StructuredLogger.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 178 lines (medium)  
**Complexity**: 10 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `StructuredLogger_test.py` with pytest tests

## Best Practices Checklist

- [x] All classes have docstrings
- [x] All public methods have docstrings
- [x] Type hints are present
- [x] pytest tests cover main functionality
- [x] Error handling is robust
- [x] Code follows PEP 8 style guide
- [x] No code duplication
- [x] Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

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


"""
StructuredLogger: JSON-based logging for Phase 144 observability.
Ensures machine-readable logs with mandatory AgentID and TraceID fields.
"""

from typing import Any
from src.core.base.Version import VERSION
import json
import logging
import re
import time
import gzip
import shutil
from datetime import datetime, timezone
from pathlib import Path

# Rust acceleration for hot-path logging
try:
    import rust_core as rc

    _RUST_ACCEL = True
except ImportError:
    rc = None  # type: ignore[assignment]
    _RUST_ACCEL = False

__version__ = VERSION


class StructuredLogger:
    """JSON logger for PyAgent swarm observability.
    Phase 277: Added log hygiene with automated GZIP compression.
    """

    # regex for sensitive data masking (Phase 227)
    SENSITIVE_PATTERNS = [
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
        self.agent_id = agent_id
        self.trace_id = trace_id or f"trace_{int(time.time())}"
        self.log_file = Path(log_file)
        self._ensure_log_dir()

    def _ensure_log_dir(self) -> None:
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        # Phase 277: Compress if > 100MB
        if self.log_file.exists() and self.log_file.stat().st_size > 100 * 1024 * 1024:
            self._compress_logs()

    def _compress_logs(self) -> None:
        """Compresses current log file to .json.gz (Phase 277)."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        compressed_file = self.log_file.with_name(
            f"{self.log_file.stem}_{timestamp}.json.gz"
        )
        logging.info(
            f"StructuredLogger: Compressing log file ({self.log_file.name}) to {compressed_file.name}"
        )

        try:
            with open(self.log_file, "rb") as f_in:
                with gzip.open(compressed_file, "wb") as f_out:
                    shutil.copyfileobj(f_in, f_out)
            self.log_file.unlink()  # Delete original
        except Exception as e:
            logging.error(f"StructuredLogger compression failed: {e}")

    def _mask_sensitive(self, text: str) -> str:
        """Automated masking for API keys and tokens (Phase 227)."""
        # Use Rust acceleration when available (2-3x faster)
        if _RUST_ACCEL and rc is not None:
            try:
                return rc.mask_sensitive_logs(text)
            except Exception:
                pass
        # Python fallback
        masked = text
        for pattern in self.SENSITIVE_PATTERNS:
            masked = pattern.sub("[REDACTED]", masked)
        return masked

    def log(self, level: str, message: str, **kwargs: Any) -> None:
        """Log a structured entry."""
        timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

        # Fast path: Use Rust for building the log entry (includes masking)
        if _RUST_ACCEL and rc is not None:
            try:
                extra_json = json.dumps(kwargs) if kwargs else None
                entry_json = rc.build_log_entry_rust(
                    timestamp,
                    self.agent_id,
                    self.trace_id,
                    level,
                    message,
                    extra_json,
                )
                # Console logging (quick)
                std_logger = logging.getLogger(f"PyAgent.{self.agent_id}")
                log_func = getattr(std_logger, level.lower(), std_logger.info)
                log_func(f"[{self.agent_id}] {message[:200]}")

                # File write
                try:
                    with open(self.log_file, "a", encoding="utf-8") as f:
                        f.write(entry_json + "\n")
                except Exception as e:
                    logging.error(f"StructuredLogger failed to write: {e}")
                return
            except Exception:
                pass  # Fall through to Python path

        # Python fallback path
        clean_message = self._mask_sensitive(message)
        clean_kwargs = {
            k: (self._mask_sensitive(str(v)) if isinstance(v, str) else v)
            for k, v in kwargs.items()
        }

        entry = {
            "timestamp": timestamp,
            "agent_id": self.agent_id,
            "trace_id": self.trace_id,
            "level": level.upper(),
            "message": clean_message,
            **clean_kwargs,
        }

        # Also log to standard logging for console visibility
        std_logger = logging.getLogger(f"PyAgent.{self.agent_id}")
        log_func = getattr(std_logger, level.lower(), std_logger.info)
        log_func(
            f"[{self.agent_id}] {clean_message} {json.dumps(clean_kwargs) if clean_kwargs else ''}"
        )

        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            logging.error(f"StructuredLogger failed to write: {e}")

    def info(self, message: str, **kwargs: Any) -> None:
        self.log("info", message, **kwargs)

    def error(self, message: str, **kwargs: Any) -> None:
        self.log("error", message, **kwargs)

    def warning(self, message: str, **kwargs: Any) -> None:
        self.log("warning", message, **kwargs)

    def debug(self, message: str, **kwargs: Any) -> None:
        self.log("debug", message, **kwargs)

    def success(self, message: str, **kwargs: Any) -> None:
        self.log("success", message, **kwargs)
