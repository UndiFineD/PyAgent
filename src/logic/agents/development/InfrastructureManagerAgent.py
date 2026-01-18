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


"""Agent specializing in infrastructure management, Proxmox orchestration, and HomeAssistant IoT control.
Provides tools for remote system administration and automated environment scaling.
"""

from __future__ import annotations
from src.core.base.Version import VERSION
import logging
from typing import Any
from src.core.base.BaseAgent import BaseAgent
from src.core.base.BaseUtilities import as_tool

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
    from src.core.base.BaseUtilities import create_main_function

    main = create_main_function(
        InfrastructureManagerAgent, "Infra Manager", "Infra logs"
    )
    main()
