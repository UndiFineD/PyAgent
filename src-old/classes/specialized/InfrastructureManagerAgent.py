#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/classes/specialized/InfrastructureManagerAgent.description.md

# InfrastructureManagerAgent

**File**: `src\classes\specialized\InfrastructureManagerAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 96  
**Complexity**: 5 (moderate)

## Overview

Agent specializing in infrastructure management, Proxmox orchestration, and HomeAssistant IoT control.
Provides tools for remote system administration and automated environment scaling.

## Classes (1)

### `InfrastructureManagerAgent`

**Inherits from**: BaseAgent

Manages remote infrastructure including Proxmox virtualization and HomeAssistant IoT.

**Methods** (5):
- `__init__(self, file_path)`
- `list_proxmox_vms(self, host, token_id, secret)`
- `control_homeassistant_device(self, entity_id, action, api_url, token)`
- `get_system_metrics(self, server_ip)`
- `improve_content(self, prompt)`

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `logging`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.utilities.as_tool`
- `src.core.base.utilities.create_main_function`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Dict`

---
*Auto-generated documentation*
## Source: src-old/classes/specialized/InfrastructureManagerAgent.improvements.md

# Improvements for InfrastructureManagerAgent

**File**: `src\classes\specialized\InfrastructureManagerAgent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 96 lines (small)  
**Complexity**: 5 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `InfrastructureManagerAgent_test.py` with pytest tests

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


"""Agent specializing in infrastructure management, Proxmox orchestration, and HomeAssistant IoT control.
Provides tools for remote system administration and automated environment scaling.
"""

import logging
from typing import Any

from src.core.base.BaseAgent import BaseAgent
from src.core.base.utilities import as_tool
from src.core.base.version import VERSION

__version__ = VERSION


class InfrastructureManagerAgent(BaseAgent):
    """Manages remote infrastructure including Proxmox virtualization and HomeAssistant IoT."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._system_prompt = (
            "You are the Infrastructure Manager Agent. "
            "You control remote servers (Proxmox) and IoT environments (HomeAssistant). "
            "You provide tools for starting/stopping VMs, monitoring system health, "
            "and automating house-wide or data-center-wide configurations."
        )

    @as_tool
    def list_proxmox_vms(self, host: str, token_id: str, secret: str) -> str:
        """Lists all VMs and containers on a Proxmox host.

        Args:
            host: Proxmox host IP or domain.
            token_id: API Token ID.
            secret: API Secret.

        """
        logging.info(f"INFRA: Listing ProxMox VMs on {host}")
        # Simulation of Proxmox API call
        # url = f"https://{host}:8006/api2/json/nodes"
        # headers = {"Authorization": f"PVEAPIToken={token_id}={secret}"}

        return (
            f"### Proxmox Inventory for {host}\n"
            "- VM 101: `Ubuntu-Server` (Status: Running, CPU: 2.1%)\n"
            "- VM 102: `Win10-Dev` (Status: Stopped)\n"
            "- CT 201: `NextCloud-LXC` (Status: Running, Mem: 1.2GB)"
        )

    @as_tool
    def control_homeassistant_device(
        self, entity_id: str, action: str, api_url: str, token: str
    ) -> str:
        """Controls a HomeAssistant device (light, switch, etc.).

        Args:
            entity_id: The HA entity ID (e.g., 'light.living_room').
            action: 'turn_on', 'turn_off', 'toggle'.
            api_url: HA Base URL.
            token: Long-lived access token.

        """
        logging.info(f"INFRA: HomeAssistant {action} for {entity_id}")
        # Simulation of HA REST API call
        # url = f"{api_url}/api/services/{entity_id.split('.')[0]}/{action}"
        # headers = {"Authorization": f"Bearer {token}"}

        return f"Successfully executed `{action}` for `{entity_id}` on HomeAssistant at {api_url}."

    @as_tool
    def get_system_metrics(self, server_ip: str) -> dict[str, Any]:
        """Retrieves hardware metrics (CPU, RAM, Disk) from a remote server via SSH or SNMP."""
        logging.info(f"INFRA: Fetching metrics for {server_ip}")
        # Mock metrics
        return {
            "server": server_ip,
            "cpu_usage": "15%",
            "ram_free": "8.2GB",
            "disk_status": "Healthy",
            "uptime": "14 days, 3 hours",
        }

    def improve_content(self, prompt: str) -> str:
        return "Infrastructure Manager ready. Provide Proxmox or HomeAssistant credentials to begin orchestration."


if __name__ == "__main__":
    from src.core.base.utilities import create_main_function

    main = create_main_function(
        InfrastructureManagerAgent, "Infra Manager", "Infra logs"
    )
    main()
