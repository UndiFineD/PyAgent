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
Discovery orchestrator.py module.
"""


from __future__ import annotations

import contextlib
import logging
import socket
import threading
import time
from typing import TYPE_CHECKING, Any

from zeroconf import (IPVersion, ServiceBrowser, ServiceInfo, ServiceListener,
                      Zeroconf)

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION

if TYPE_CHECKING:
    from src.infrastructure.swarm.fleet.fleet_manager import FleetManager


class DiscoveryOrchestrator:
    """Handles peer-to-peer discovery of fleet nodes using mDNS/Zeroconf."""

    SERVICE_TYPE = "_pyagent._tcp.local."

    def __init__(self, fleet: FleetManager) -> None:
        self.fleet = fleet
        self._failure_count = 0
        self._circuit_open = False
        self._last_retry = 0
        self._last_advertisement = 0  # Rate limiting

        try:
            self.zeroconf = Zeroconf(ip_version=IPVersion.V4Only)
            self.listener = FleetServiceListener(self.fleet)
            self.browser = ServiceBrowser(self.zeroconf, self.SERVICE_TYPE, self.listener)
            self._is_advertising = False

            # Start advertising in a background thread to not block fleet init
            threading.Thread(target=self.start_advertising, daemon=True).start()
        except Exception as e:
            logging.error(f"Discovery: Initialization failed: {e}")

    def _on_failure(self, error: Exception) -> None:
        """Handles internal discovery failures with a circuit breaker mechanism."""
        self._failure_count += 1
        if self._failure_count > 5:
            logging.error(f"Discovery: Circuit breaker OPEN due to multiple failures: {error}")
            self._circuit_open = True
            self._last_retry = time.time()

    def _check_circuit(self) -> bool:
        """Checks if the circuit is closed or if a retry is allowed."""
        if self._circuit_open:
            if time.time() - self._last_retry > 60:
                # 1 minute cooldown
                logging.info("Discovery: Circuit breaker HALF-OPEN, attempting retry...")
                self._circuit_open = False
                self._failure_count = 0
                return True
            return False
        return True

    def get_local_ip(self) -> str:
        """Utility to get the primary local IP address."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "127.0.0.1"

    def start_advertising(self, port: int = 8000) -> None:
        """Advertises the local fleet node to the network."""
        # 1. Check Circuit & Rate Limiting (Phase 123/124 Hardening)
        if self._is_advertising:
            return

        if not self._check_circuit():
            return

        now = time.time()
        if now - self._last_advertisement < 30:
            # Max once every 30 seconds
            logging.debug("Discovery: Advertisement rate-limited (Skipping).")
            return

        self._last_advertisement = now
        local_ip = self.get_local_ip()
        node_id = f"pyagent-{socket.gethostname()}"

        # Get list of local agent names to share (limit to top 15)
        agent_names: list[str] = []
        if hasattr(self.fleet, "agents") and hasattr(self.fleet.agents, "registry_configs"):
            agent_names = list(self.fleet.agents.registry_configs.keys())

        info = ServiceInfo(
            self.SERVICE_TYPE,
            f"{node_id}.{self.SERVICE_TYPE}",
            addresses=[socket.inet_aton(local_ip)],
            port=port,
            properties={
                "agents": ",".join(agent_names[:15]),
                "version": "1.0.0",
                "hostname": socket.gethostname(),
            },
            server=f"{node_id}.local.",
        )

        try:
            logging.info(f"Discovery: Advertising local fleet node '{node_id}' at {local_ip}:{port}")
            self.zeroconf.register_service(info, allow_name_change=True)
            self._is_advertising = True
            self._failure_count = 0  # Reset on success

        except Exception as e:
            logging.error(f"Discovery: Failed to register service: {e}")
            self._on_failure(e)

    def shutdown(self) -> None:
        """Gracefully shuts down discovery."""
        if hasattr(self, "zeroconf"):
            self.zeroconf.unregister_all_services()
            self.zeroconf.close()


class FleetServiceListener(ServiceListener):
    """Listens for other PyAgent fleet nodes and registers them."""

    def __init__(self, fleet: FleetManager) -> None:
        self.fleet = fleet
        self._discovered_nodes: set[Any] = set()
        self._last_add_time = 0
        self._min_interval = 0.5  # Rate limit: 2 adds per second

    def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        pass

    def remove_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        logging.info(f"Discovery: Service {name} removed")
        if name in self._discovered_nodes:
            self._discovered_nodes.remove(name)

    def add_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        # Rate Limiting (Phase 123 Hardening)
        now = time.time()
        if now - self._last_add_time < self._min_interval:
            return
        self._last_add_time = now

        try:
            info = zc.get_service_info(type_, name)
        except Exception:
            # Zeroconf instance loop might be stopping, already stopped, or other transient issue (Phase 123)
            return

        if not info:
            return

        if name in self._discovered_nodes:
            return

        self._discovered_nodes.add(name)

        addresses = [socket.inet_ntoa(addr) for addr in info.addresses]
        if not addresses:
            return

        # Filter out self
        with contextlib.suppress(Exception):
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            if addresses[0] == local_ip:
                logging.debug(f"Discovery: Skipping local node discovery for {name}")
                return

        url = f"http://{addresses[0]}:{info.port}"
        agents_bytes = info.properties.get(b"agents", b"")
        agents = agents_bytes.decode("utf-8").split(",") if agents_bytes else []
        version_bytes = info.properties.get(b"version", b"1.0.0")
        version = version_bytes.decode("utf-8")

        logging.info(f"Discovery: Found remote fleet node '{name}' at {url} with agents: {agents}")

        # Register the remote node in the fleet
        try:
            self.fleet.register_remote_node(url, agents, version)
        except Exception as e:
            logging.error(f"Discovery: Failed to register remote node {url}: {e}")
