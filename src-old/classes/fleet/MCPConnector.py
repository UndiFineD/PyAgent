#!/usr/bin/env python3
"""LLM_CONTEXT_START

## Source: src-old/classes/fleet/MCPConnector.description.md

# MCPConnector

**File**: `src\\classes\fleet\\MCPConnector.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 117  
**Complexity**: 6 (moderate)

## Overview

Low-level connector for Model Context Protocol (MCP) servers using stdio transport.

## Classes (1)

### `MCPConnector`

Manages the lifecycle and JSON-RPC communication with an MCP server.

**Methods** (6):
- `__init__(self, name, command, env, recorder)`
- `_record(self, action, result)`
- `start(self)`
- `_read_stderr(self)`
- `call(self, method, params, timeout)`
- `stop(self)`

## Dependencies

**Imports** (10):
- `__future__.annotations`
- `json`
- `logging`
- `src.core.base.version.VERSION`
- `subprocess`
- `threading`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/classes/fleet/MCPConnector.improvements.md

# Improvements for MCPConnector

**File**: `src\\classes\fleet\\MCPConnector.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 117 lines (medium)  
**Complexity**: 6 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `MCPConnector_test.py` with pytest tests

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


"""Low-level connector for Model Context Protocol (MCP) servers using stdio transport."""

import json
import logging
import subprocess
import threading
from typing import Any

from src.core.base.version import VERSION

__version__ = VERSION


class MCPConnector:
    """Manages the lifecycle and JSON-RPC communication with an MCP server."""

    def __init__(
        self,
        name: str,
        command: list[str],
        env: dict[str, str] | None = None,
        recorder: Any = None,
    ) -> None:
        self.name = name
        self.command = command
        self.env = env
        self.recorder = recorder
        self.process: subprocess.Popen | None = None
        self.request_id = 0
        self.pending_requests: dict[int, Any] = {}
        self._lock = threading.Lock()
        self.is_running = False

    def _record(self, action: str, result: str) -> None:
        """Record MCP operations."""
        if self.recorder:
            self.recorder.record_interaction("MCP", self.name, action, result)

    def start(self) -> None:
        """Launches the MCP server process."""
        try:
            logging.info(
                f"Starting MCP server '{self.name}' with command: {' '.join(self.command)}"
            )
            self.process = subprocess.Popen(
                self.command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=self.env,
                text=True,
                bufsize=1,
            )
            self.is_running = True
            # Start a thread to read stderr for logging
            threading.Thread(target=self._read_stderr, daemon=True).start()
        except Exception as e:
            logging.error(f"Failed to start MCP server {self.name}: {e}")
            self.is_running = False

    def _read_stderr(self) -> None:
        """Logs stderr from the MCP server."""
        if not self.process or not self.process.stderr:
            return
        for line in self.process.stderr:
            logging.warning(f"[MCP:{self.name}:ERR] {line.strip()}")

    def call(
        self, method: str, params: dict[str, Any], timeout: int = 30
    ) -> dict[str, Any]:
        """Sends a JSON-RPC request and waits for the response."""
        if not self.is_running or not self.process or not self.process.stdin:
            return {"error": "MCP server not running"}

        with self._lock:
            self.request_id += 1
            id = self.request_id

        request = {"jsonrpc": "2.0", "id": id, "method": method, "params": params}

        try:
            self.process.stdin.write(json.dumps(request) + "\n")
            self.process.stdin.flush()

            # Read response
            # Note: This is an extremely simplified synchronous read from a shared stdout.
            # In a real system, we'd have a permanent reader thread and a way to match IDs.
            # For this Phase, we'll implement a basic matching reader.

            line = self.process.stdout.readline()
            if not line:
                return {"error": "No response from MCP server"}

            response = json.loads(line)
            if response.get("id") == id:
                return response
            else:
                return {
                    "error": f"ID mismatch: expected {id}, got {response.get('id')}",
                    "raw": response,
                }

        except Exception as e:
            logging.error(f"Error calling MCP server {self.name}: {e}")
            return {"error": str(e)}

    def stop(self) -> None:
        """Gracefully shuts down the MCP server."""
        if self.process:
            self.process.terminate()
            self.is_running = False
