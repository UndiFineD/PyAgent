#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/classes/agent/NotificationManager.description.md

# NotificationManager

**File**: `src\classes\agent\NotificationManager.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 12 imports  
**Lines**: 105  
**Complexity**: 8 (moderate)

## Overview

Python module containing implementation for NotificationManager.

## Classes (1)

### `NotificationManager`

Manages event notifications via webhooks and internal callbacks.

**Methods** (8):
- `__init__(self, workspace_root, recorder)`
- `_is_webhook_working(self, url)`
- `_update_status(self, url, working)`
- `register_webhook(self, url)`
- `register_callback(self, callback)`
- `notify(self, event_name, event_data)`
- `_execute_callbacks(self, event_name, event_data)`
- `_send_webhooks(self, event_name, event_data)`

## Dependencies

**Imports** (12):
- `__future__.annotations`
- `collections.abc.Callable`
- `logging`
- `requests`
- `src.core.base.ConnectivityManager.ConnectivityManager`
- `src.core.base.utils.NotificationCore.NotificationCore`
- `src.core.base.version.VERSION`
- `src.infrastructure.backend.LocalContextRecorder.LocalContextRecorder`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/classes/agent/NotificationManager.improvements.md

# Improvements for NotificationManager

**File**: `src\classes\agent\NotificationManager.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 105 lines (medium)  
**Complexity**: 8 score (moderate)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `NotificationManager_test.py` with pytest tests

## Best Practices Checklist

- All classes have docstrings
- All public methods have docstrings
- Type hints are present
- pytest tests cover main functionality
- Error handling is robust
- Code follows PEP 8 style guide
- No code duplication
- Proper separation of concerns

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

# Infrastructure

from src.core.base.version import VERSION
import logging
from typing import List, Dict, Any, Optional
from collections.abc import Callable
from src.infrastructure.backend.LocalContextRecorder import LocalContextRecorder
from src.core.base.ConnectivityManager import ConnectivityManager
from src.core.base.utils.NotificationCore import NotificationCore

__version__ = VERSION

# Optional dependency
try:
    import requests

    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    requests = None


class NotificationManager:
    """Manages event notifications via webhooks and internal callbacks."""

    def __init__(
        self,
        workspace_root: str | None = None,
        recorder: LocalContextRecorder | None = None,
    ) -> None:
        self.webhooks: list[str] = []
        self.callbacks: list[Callable[[str, dict[str, Any]], None]] = []
        # Phase 108: Resilience management
        self.workspace_root = workspace_root
        self.recorder = recorder
        self.connectivity = ConnectivityManager(workspace_root)
        self.core = NotificationCore()

    def _is_webhook_working(self, url: str) -> bool:
        domain = self.core.get_domain_from_url(url)
        return self.connectivity.is_endpoint_available(domain)

    def _update_status(self, url: str, working: bool) -> None:
        domain = self.core.get_domain_from_url(url)
        self.connectivity.update_status(domain, working)

    def register_webhook(self, url: str) -> None:
        self.webhooks.append(url)
        logging.info(f"Registered webhook: {url}")

    def register_callback(
        self, callback: Callable[[str, dict[str, Any]], None]
    ) -> None:
        self.callbacks.append(callback)
        name = getattr(callback, "__name__", repr(callback))
        logging.info(f"Registered callback: {name}")

    def notify(self, event_name: str, event_data: dict[str, Any]) -> None:
        """Executes callbacks and sends webhooks for an event."""
        if not self.core.validate_event_data(event_data):
            logging.debug(f"Invalid event data for {event_name}")
            return

        if self.recorder:
            self.recorder.record_lesson(
                "event_notify",
                {"event": event_name, "data_keys": list(event_data.keys())},
            )
        self._execute_callbacks(event_name, event_data)
        self._send_webhooks(event_name, event_data)

    def _execute_callbacks(self, event_name: str, event_data: dict[str, Any]) -> None:
        for callback in self.callbacks:
            try:
                callback(event_name, event_data)
            except Exception as e:
                logging.warning(f"Callback failed: {e}")

    def _send_webhooks(self, event_name: str, event_data: dict[str, Any]) -> None:
        if not HAS_REQUESTS or requests is None or not self.webhooks:
            return

        payload = self.core.construct_payload(event_name, event_data)

        for url in self.webhooks:
            if not self._is_webhook_working(url):
                continue

            try:
                # Fire and forget (ideally should be async or in a thread)
                # Security Patch 115.1: Limit redirects for webhook calls
                with requests.Session() as session:
                    session.max_redirects = 2
                    response = session.post(url, json=payload, timeout=5)
                    response.raise_for_status()
                    self._update_status(url, True)
            except Exception as e:
                logging.warning(f"Webhook failed for {url}: {e}")
                self._update_status(url, False)
                if self.recorder:
                    self.recorder.record_lesson(
                        "webhook_failure", {"url": url, "error": str(e)}
                    )
