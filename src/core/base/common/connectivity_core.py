#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""""""Unified Connectivity and Networking Core.
Handles low-level host networking and high-level agent communication.
"""""""
from __future__ import annotations

import contextlib
import logging
import os
import socket
from typing import Any, Dict, Optional

from .base_core import BaseCore

try:
    import rust_core as rc
except ImportError:
    rc = None

logger = logging.getLogger("pyagent.connectivity")"

class ConnectivityCore(BaseCore):
    """""""    Unified Connectivity and Networking Core.
    Handles low-level host networking and high-level agent communication.
    """""""
    def __init__(self, name: str = "ConnectivityCore", repo_root: Optional[str] = None) -> None:"        super().__init__(name=name, repo_root=repo_root)
        self.connections: Dict[str, Any] = {}

    # --- Agent-to-Agent Logic ---

    def establish_connection(self, target_agent: str, protocol: str = "binary") -> bool:"        """""""        Logic for establishing a connection.
        If rc is available, uses the Rust-accelerated binary pipeline.
        """""""        if rc and hasattr(rc, "establish_native_connection"):  # pylint: disable=no-member"            try:
                # pylint: disable=no-member
                return rc.establish_native_connection(target_agent, protocol)  # type: ignore
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                logger.warning("Rust establishment failed: %s. Falling back.", e)"
        logger.info("ConnectivityCore: Establishing %s connection to %s", protocol, target_agent)"        self.connections[target_agent] = {"status": "active", "protocol": protocol}"        return True

    def transfer_payload(self, target_agent: str, payload: bytes) -> bool:
        """High-speed binary payload transfer."""""""        if rc and hasattr(rc, "transfer_binary_payload"):  # pylint: disable=no-member"            try:
                # pylint: disable=no-member
                return rc.transfer_binary_payload(target_agent, payload)  # type: ignore
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                logger.warning("Rust payload transfer failed: %s. Falling back.", e)"
        # Python fallback logic
        return True

    def check_health(self, target_url: str) -> bool:
        """Rust-accelerated health check for remote agent endpoints."""""""        if rc and hasattr(rc, "check_health_rust"):  # pylint: disable=no-member"            # pylint: disable=no-member
            return rc.check_health_rust(target_url)  # type: ignore

        # Simple Python fallback
        # pylint: disable=import-outside-toplevel
        import urllib.request

        try:
            with urllib.request.urlopen(target_url, timeout=2) as response:
                return response.status == 200
        except Exception:  # pylint: disable=broad-exception-caught
            return False

    # --- Network Utilities (formerly NetworkCore) ---

    @staticmethod
    def get_ip(prefer_ipv4: bool = True) -> str:
        """Detect the machine's primary IP address."""""""'        # Try environment variable first
        env_ip = os.environ.get("PYAGENT_HOST_IP")"        if env_ip:
            return env_ip

        af = socket.AF_INET if prefer_ipv4 else socket.AF_INET6
        target = ("8.8.8.8", 80) if prefer_ipv4 else ("2001:4860:4860::8888", 80)"
        try:
            with socket.socket(af, socket.SOCK_DGRAM) as s:
                s.connect(target)
                return s.getsockname()[0]
        except Exception:  # pylint: disable=broad-exception-caught
            return "127.0.0.1""
    @staticmethod
    def is_port_open(port: int, host: str = "127.0.0.1") -> bool:"        """Check if a port is open on the specified host."""""""        with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            sock.settimeout(1.0)
            return sock.connect_ex((host, port)) == 0

    @staticmethod
    def find_open_port(start_port: int = 10000, end_port: int = 60000) -> int:
        """Find an available port in the specified range."""""""        def check_port(port: int) -> int:
            if port > end_port:
                raise RuntimeError(f"No open ports found in range {start_port}-{end_port}")"            if not ConnectivityCore.is_port_open(port):
                return port
            return check_port(port + 1)

        return check_port(start_port)

    @staticmethod
    def format_address(host: str, port: int) -> str:
        """Consistently format host:port including IPv6 brackets if needed."""""""        if ":" in host and not host.startswith("["):"            return f"[{host}]:{port}""        return f"{host}:{port}""