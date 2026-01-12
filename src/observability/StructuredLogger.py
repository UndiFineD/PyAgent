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

from __future__ import annotations

from src.core.base.version import VERSION
__version__ = VERSION

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.


"""
StructuredLogger: JSON-based logging for Phase 144 observability.
Ensures machine-readable logs with mandatory AgentID and TraceID fields.
"""



import json
import logging
import os
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

class StructuredLogger:
    """JSON logger for PyAgent swarm observability."""
    
    # regex for sensitive data masking (Phase 227)
    SENSITIVE_PATTERNS = [
        re.compile(r"sk-[a-zA-Z0-9]{32,}"),  # OpenAI Keys
        re.compile(r"Bearer\s+[a-zA-Z0-9\-\._~+/]+=*"), # Bearer Tokens
        re.compile(r"gh[ps]_[a-zA-Z0-9]{36}") # GitHub Tokens
    ]

    def __init__(self, agent_id: str, trace_id: Optional[str] = None, log_file: str = "data/logs/structured.json") -> None:
        self.agent_id = agent_id
        self.trace_id = trace_id or f"trace_{int(time.time())}"
        self.log_file = Path(log_file)
        self._ensure_log_dir()

    def _ensure_log_dir(self):
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

    def _mask_sensitive(self, text: str) -> str:
        """Automated masking for API keys and tokens (Phase 227)."""
        masked = text
        for pattern in self.SENSITIVE_PATTERNS:
            masked = pattern.sub("[REDACTED]", masked)
        return masked

    def log(self, level: str, message: str, **kwargs):
        """Log a structured entry."""
        # Clean sensitive data from message and kwargs
        clean_message = self._mask_sensitive(message)
        clean_kwargs = {k: (self._mask_sensitive(str(v)) if isinstance(v, str) else v) for k, v in kwargs.items()}

        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "agent_id": self.agent_id,
            "trace_id": self.trace_id,
            "level": level.upper(),
            "message": clean_message,
            **clean_kwargs
        }
        
        # Also log to standard logging for console visibility
        std_logger = logging.getLogger(f"PyAgent.{self.agent_id}")
        log_func = getattr(std_logger, level.lower(), std_logger.info)
        log_func(f"[{self.agent_id}] {clean_message} {json.dumps(clean_kwargs) if clean_kwargs else ''}")

        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            logging.error(f"StructuredLogger failed to write: {e}")

    def info(self, message: str, **kwargs):
        self.log("info", message, **kwargs)

    def error(self, message: str, **kwargs):
        self.log("error", message, **kwargs)

    def warning(self, message: str, **kwargs):
        self.log("warning", message, **kwargs)

    def debug(self, message: str, **kwargs):
        self.log("debug", message, **kwargs)

    def success(self, message: str, **kwargs):
        self.log("success", message, **kwargs)
