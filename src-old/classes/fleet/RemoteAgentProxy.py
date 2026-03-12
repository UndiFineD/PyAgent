#!/usr/bin/env python3
"""LLM_CONTEXT_START

## Source: src-old/classes/fleet/RemoteAgentProxy.description.md

# RemoteAgentProxy

**File**: `src\\classes\fleet\\RemoteAgentProxy.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 12 imports  
**Lines**: 135  
**Complexity**: 7 (moderate)

## Overview

Proxy for agents running on remote nodes.
Allows FleetManager to transparently call tools on other machines.

## Classes (1)

### `RemoteAgentProxy`

**Inherits from**: BaseAgent

Encapsulates a remote agent accessible via HTTP/JSON-RPC.

Resilience (Phase 108): Implements a 15-minute TTL status cache for remote nodes.
Intelligence (Phase 108): Records remote interactions to local shards.

**Methods** (7):
- `__init__(self, file_path, node_url, agent_name)`
- `_is_node_working(self)`
- `_update_node_status(self, is_up)`
- `call_remote_tool(self, tool_name)`
- `call_remote_tool_binary(self, tool_name, compress)`
- `_record_interaction(self, tool_name, payload, response)`
- `improve_content(self, prompt)`

## Dependencies

**Imports** (12):
- `__future__.annotations`
- `logging`
- `os`
- `requests`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.ConnectivityManager.ConnectivityManager`
- `src.core.base.connectivity.BinaryTransport`
- `src.core.base.version.VERSION`
- `src.infrastructure.backend.LocalContextRecorder.LocalContextRecorder`
- `typing.Any`
- `typing.Dict`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/classes/fleet/RemoteAgentProxy.improvements.md

# Improvements for RemoteAgentProxy

**File**: `src\\classes\fleet\\RemoteAgentProxy.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 135 lines (medium)  
**Complexity**: 7 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `RemoteAgentProxy_test.py` with pytest tests

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


"""Proxy for agents running on remote nodes.
Allows FleetManager to transparently call tools on other machines.
"""

import logging
import os
from typing import Any

import requests
from src.core.base.BaseAgent import BaseAgent
from src.core.base.connectivity import BinaryTransport
from src.core.base.ConnectivityManager import ConnectivityManager
from src.core.base.version import VERSION

__version__ = VERSION


class RemoteAgentProxy(BaseAgent):
    """Encapsulates a remote agent accessible via HTTP/JSON-RPC.

    Resilience (Phase 108): Implements a 15-minute TTL status cache for remote nodes.
    Intelligence (Phase 108): Records remote interactions to local shards.
    """

    def __init__(self, file_path: str, node_url: str, agent_name: str) -> None:
        super().__init__(file_path)
        self.node_url = node_url.rstrip("/")
        self.agent_name = agent_name
        self._system_prompt = f"Proxy for remote agent '{agent_name}' at {node_url}"

        # Phase 108: Centralized Resilience management
        work_root = getattr(self, "_workspace_root", os.getcwd())
        self.connectivity = ConnectivityManager(work_root)

    def _is_node_working(self) -> bool:
        """Checks if the remote node is known to be working via cache (Phase 108)."""
        return self.connectivity.is_endpoint_available(self.node_url)

    def _update_node_status(self, is_up: bool) -> None:
        """Updates the node status in the persistent cache (Phase 108)."""
        self.connectivity.update_status(self.node_url, is_up)

    def call_remote_tool(self, tool_name: str, **kwargs) -> str:
        """Calls a tool on the remote node with resilience and intelligence (Phase 108)."""
        if not self._is_node_working():
            return f"Skipping call: Remote node {self.node_url} is currently unreachable (cached)."

        endpoint = f"{self.node_url}/call"
        payload = {"agent": self.agent_name, "tool": tool_name, "args": kwargs}

        try:
            logging.info(f"Calling remote tool {tool_name} on {self.node_url}")
            # Security Patch 115.1: Limit redirects for remote proxy calls
            with requests.Session() as session:
                session.max_redirects = 3
                response = session.post(endpoint, json=payload, timeout=60)
                response.raise_for_status()

            result = response.json().get("result", "No result returned.")
            self._update_node_status(True)
            self._record_interaction(tool_name, payload, result)
            return result
        except Exception as e:
            logging.error(f"Error calling remote agent: {e}")
            self._update_node_status(False)
            return f"Error calling remote agent: {e}"

    def call_remote_tool_binary(
        self, tool_name: str, compress: bool = True, **kwargs
    ) -> Any:
        """Calls a tool on the remote node using high-performance binary transport (Phase 255).
        """
        if not self._is_node_working():
            return None

        endpoint = f"{self.node_url}/call_binary"
        payload_data = {"agent": self.agent_name, "tool": tool_name, "args": kwargs}

        try:
            packed_payload = BinaryTransport.pack(payload_data, compress=compress)
            logging.info(
                f"Calling remote binary tool {tool_name} on {self.node_url} (Compressed: {compress})"
            )

            headers = {"Content-Type": "application/octet-stream"}
            if compress:
                headers["Content-Encoding"] = "zstd"

            response = requests.post(
                endpoint, data=packed_payload, headers=headers, timeout=60
            )
            response.raise_for_status()

            result = BinaryTransport.unpack(response.content, compressed=compress)
            self._update_node_status(True)
            return result.get("result")
        except Exception as e:
            logging.error(f"Error in remote binary call: {e}")
            self._update_node_status(False)
            return None

    def _record_interaction(
        self, tool_name: str, payload: dict[str, Any], response: str
    ) -> None:
        """Records the interaction to a local shard for later intelligence harvesting (Phase 108)."""
        try:
            from src.infrastructure.backend.LocalContextRecorder import (
                LocalContextRecorder,
            )

            recorder = LocalContextRecorder()
            recorder.record_interaction(
                agent_name=f"remote_{self.agent_name}",
                tool_name=tool_name,
                payload=payload,
                response=response,
            )
        except Exception as e:
            logging.debug(f"Failed to record remote interaction: {e}")

    def improve_content(self, prompt: str) -> str:
        """Proxies the improvement request to the remote agent."""
        return self.call_remote_tool("improve_content", prompt=prompt)
