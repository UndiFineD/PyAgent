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
Lan discovery.py module.
"""
# Phase 320: LAN Discovery & Peer Synchronization

import hashlib
import hmac
import json
import socket
import threading
import time
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional, Callable

from src.infrastructure.swarm.network.network_utils import get_local_network_ip
# from src.observability.structured_logger import StructuredLogger
import logging

# logger = StructuredLogger(__name__)
logger = logging.getLogger(__name__)


@dataclass
class PeerInfo:
    """Discovery metadata for a peer agent on the LAN."""

    agent_id: str
    ip: str
    port: int
    last_seen: float
    metadata: Dict[str, Any]
    trust_score: float = 1.0
    latency: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Serializes peer info to a dictionary."""
        return asdict(self)


class LANDiscovery:
    """
    Decentralized LAN Discovery for PyAgents.
    Follows an Announce -> Respond -> Register -> Sync cycle.

    Network-aware implementation that detects subnet and uses proper broadcasting.
    """

    DEFAULT_DISCOVERY_PORT = 31415
    MAX_CLOCK_SKEW = 300.0  # Seconds

    def __init__(
        self,
        agent_id: str,
        service_port: int,
        secret_key: Optional[str] = None,
        metadata: Optional[Dict] = None,
        sleep_fn: Callable[[float], None] | None = None,
        discovery_port: Optional[int] = None,
        enable_broadcast: bool = True,
        auto_find_port: bool = True,
    ):
        self.agent_id = agent_id
        self.service_port = service_port
        self.secret_key = secret_key
        self.metadata = metadata or {}
        self.enable_broadcast = enable_broadcast
        self.auto_find_port = auto_find_port

        # Internal identifiers
        self._local_ip: Optional[str] = None
        self._subnet_broadcast: Optional[str] = None

        # Set discovery port (with auto-detection if needed)
        self.discovery_port = discovery_port or self.DEFAULT_DISCOVERY_PORT
        if auto_find_port and not self._test_port_available(self.discovery_port):
            available_port = self.find_available_port(self.discovery_port + 1)
            if available_port:
                logger.info(f"LANDiscovery: Port {self.discovery_port} unavailable, using {available_port}")
                self.discovery_port = available_port
            else:
                logger.warning(f"LANDiscovery: No available ports found, using {self.discovery_port} anyway")

        self.registry: Dict[str, PeerInfo] = {}
        self._running = False
        self._lock = threading.Lock()
        self._nonces: Dict[str, float] = {}  # agent_id: last_timestamp
        self._ping_times: Dict[str, float] = {}  # agent_id: sent_time

        # Network detection
        self._listen_thread: Optional[threading.Thread] = None
        self._announce_thread: Optional[threading.Thread] = None

        # Sleep/wakeup support for the announce loop
        self._sleep_event = threading.Event()
        self._sleep_fn: Callable[[float], None]
        if sleep_fn is None:
            def _wait(secs: float) -> None:
                self._sleep_event.wait(secs)

            self._sleep_fn = _wait
        else:
            self._sleep_fn = sleep_fn

    def _test_port_available(self, port: int) -> bool:
        """
        Test if a port is available for binding.

        Args:
            port: Port number to test.

        Returns:
            True if port is available, False otherwise.
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(("", port))
            sock.close()
            return True
        except OSError:
            return False

    def find_available_port(self, start_port: int, max_attempts: int = 100) -> Optional[int]:
        """
        Find an available port starting from start_port.

        Args:
            start_port: Port number to start searching from.
            max_attempts: Maximum number of ports to try.

        Returns:
            Available port number or None if none found.
        """
        for port in range(start_port, start_port + max_attempts):
            if self._test_port_available(port):
                return port
        return None

    def _detect_network_config(self):
        """Detects local IP and broadcast address."""
        self._local_ip = get_local_network_ip()
        if self._local_ip and self._local_ip != "127.0.0.1":
            # Simple assumption for /24 subnet broadcast
            parts = self._local_ip.split(".")
            parts[-1] = "255"
            self._subnet_broadcast = ".".join(parts)
        else:
            self._subnet_broadcast = "255.255.255.255"

    def _detect_subnet_broadcast(self) -> Optional[str]:
        """
        Detect the proper subnet broadcast address for the local network.

        Returns:
            Subnet broadcast address, or None if detection fails.
        """
        try:
            # Get local IP
            local_ip = self.local_ip
            if local_ip == "0.0.0.0" or local_ip.startswith("127."):
                logger.warning("LANDiscovery: Cannot detect subnet for localhost/unknown IP")
                return None

            # Parse IP and create subnet broadcast
            ip_parts = local_ip.split('.')
            if len(ip_parts) != 4:
                logger.warning(f"LANDiscovery: Invalid IPv4 address format: {local_ip}")
                return None

            # Assume /24 subnet (most common for home/office networks)
            # Broadcast is x.x.x.255 for /24 subnet
            broadcast = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.255"
            logger.info(f"LANDiscovery: Detected subnet broadcast: {broadcast}")
            return broadcast

        except Exception as e:
            logger.warning(f"LANDiscovery: Failed to detect subnet broadcast: {e}")
            return None

    @property
    def local_ip(self) -> str:
        """Lazily identifies and returns the local network IPv4 address for LAN discovery."""
        if not self._local_ip:
            self._local_ip = self._detect_local_network_ip()
        return self._local_ip or "127.0.0.1"

    def _detect_local_network_ip(self) -> str:
        """
        Detect the IP address of the local network interface for LAN discovery.
        Delegates to the shared network_utils.get_local_network_ip implementation.
        """
        return get_local_network_ip()

    @property
    def broadcast_addr(self) -> str:
        """Get the appropriate broadcast address for this network."""
        if not self.enable_broadcast:
            return "255.255.255.255"  # Fallback when broadcast is disabled

        if not self._subnet_broadcast:
            self._subnet_broadcast = self._detect_subnet_broadcast()

        # Fallback to global broadcast if subnet detection fails
        return self._subnet_broadcast or "255.255.255.255"

    def _sign(self, data: str) -> str:
        if not self.secret_key:
            return "unsigned"
        return hmac.new(self.secret_key.encode(), data.encode(), hashlib.sha256).hexdigest()

    def _verify(self, data: str, signature: str) -> bool:
        if not self.secret_key:
            return True
        expected = self._sign(data)
        return hmac.compare_digest(expected, signature)

    def _create_message(self, msg_type: str, extra: Optional[Dict] = None) -> bytes:
        payload: Dict[str, Any] = {
            "type": msg_type,
            "agent_id": self.agent_id,
            "ip": self.local_ip,
            "port": self.service_port,
            "timestamp": time.time(),
            "metadata": self.metadata,
        }
        if extra:
            payload.update(extra)

        data_str = json.dumps(payload, sort_keys=True)
        envelope = {"data": payload, "sig": self._sign(data_str)}
        return json.dumps(envelope).encode()

    def start(self):
        """Starts the discovery threads."""
        if self._running:
            logger.warning("LANDiscovery: Already running")
            return

        try:
            # Detect network configuration
            self._detect_network_config()

            # Test if we can bind to the discovery port. Don't abort startup
            # if the port is unavailable; we can still announce (send-only).
            if not self._test_port_available(self.discovery_port):
                if self.auto_find_port:
                    available_port = self.find_available_port(self.discovery_port + 1)
                    if available_port:
                        logger.info(f"LANDiscovery: Port {self.discovery_port} unavailable, using {available_port}")
                        self.discovery_port = available_port
                    else:
                        logger.warning("LANDiscovery: No available ports found; continuing in send-only mode")
                else:
                    logger.warning("LANDiscovery: Port %d unavailable; continuing in send-only mode",
                                   self.discovery_port)

            self._running = True
            self._listen_thread = threading.Thread(
                target=self._listen_loop,
                daemon=True,
                name=f"LANDiscovery-Listen-{self.agent_id[:8]}"
            )
            self._listen_thread.start()

            if self.enable_broadcast:
                self._announce_thread = threading.Thread(
                    target=self._announce_loop,
                    daemon=True,
                    name=f"LANDiscovery-Announce-{self.agent_id[:8]}"
                )
                self._announce_thread.start()

            logger.info("LANDiscovery: Started on port %d (broadcast: %s)",
                        self.discovery_port, self.enable_broadcast)

        except Exception as e:
            logger.error(f"LANDiscovery: Failed to start: {e}")
            self._running = False
            raise

    def get_network_info(self) -> Dict[str, Any]:
        """
        Get information about the current network configuration.

        Returns:
            Dictionary with network information.
        """
        connectivity = self.test_network_connectivity()

        return {
            "local_ip": self.local_ip,
            "broadcast_addr": self.broadcast_addr,
            "discovery_port": self.discovery_port,
            "service_port": self.service_port,
            "enable_broadcast": self.enable_broadcast,
            "subnet_detected": self._subnet_broadcast is not None,
            "peers_discovered": len(self.registry),
            "connectivity": connectivity
        }

    def test_network_connectivity(self) -> Dict[str, Any]:
        """
        Test network connectivity for discovery operations.

        Returns:
            Dictionary with connectivity test results.
        """
        results = {
            "port_available": self._test_port_available(self.discovery_port),
            "can_bind_socket": False,
            "broadcast_reachable": False,
            "subnet_detected": self._subnet_broadcast is not None,
            "local_ip_valid": False
        }

        # Test socket binding
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(("", self.discovery_port))
            results["can_bind_socket"] = True
            sock.close()
        except OSError:
            pass

        # Test local IP validity
        local_ip = self.local_ip
        results["local_ip_valid"] = (
            local_ip != "0.0.0.0" and
            not local_ip.startswith("127.") and
            len(local_ip.split('.')) == 4
        )

        # Test broadcast reachability (basic connectivity test)
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.settimeout(1.0)
            test_msg = b"test"
            sock.sendto(test_msg, (self.broadcast_addr, self.discovery_port))
            results["broadcast_reachable"] = True
            sock.close()
        except (OSError, socket.timeout):
            pass

        return results

    def stop(self):
        """Stops the discovery threads."""
        self._running = False

    def _announce_loop(self):
        if not self.enable_broadcast:
            logger.info("LANDiscovery: Broadcasting disabled, announce loop skipping")
            return

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        broadcast_addr = self.broadcast_addr

        # Initial announcement
        try:
            msg = self._create_message("ANNOUNCE")
            sock.sendto(msg, (broadcast_addr, self.discovery_port))
            logger.debug(f"LANDiscovery: Sent initial announcement to {broadcast_addr}:{self.discovery_port}")
        except Exception as exc:  # pylint: disable=broad-exception-caught
            logger.error(f"LANDiscovery: Initial announcement failed: {exc}")

        while self._running:
            try:
                # Periodic Heartbeat
                msg = self._create_message("HEARTBEAT")
                sock.sendto(msg, (broadcast_addr, self.discovery_port))

                # Registry Sync (Gossip)
                if self.registry:
                    self._sync_registry(sock)

            except Exception as exc:  # pylint: disable=broad-exception-caught
                logger.debug(f"LANDiscovery: Background loop error: {exc}")

            # Use the instance sleep function so the loop is interruptible and testable
            self._sleep_fn(30)  # Announce every 30 seconds

    def _sync_registry(self, sock: socket.socket):
        with self._lock:
            # Send top 10 most recent peers
            peers_list = sorted(
                [p.to_dict() for p in self.registry.values()], key=lambda x: x["last_seen"], reverse=True
            )[:10]

        msg = self._create_message("SYNC", {"peers": peers_list})
        broadcast_addr = self.broadcast_addr
        sock.sendto(msg, (broadcast_addr, self.discovery_port))

    def _listen_loop(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            # Bind to all interfaces on discovery port
            sock.bind(("", self.discovery_port))
            logger.info(f"LANDiscovery: Listening on port {self.discovery_port}")
        except Exception as exc:  # pylint: disable=broad-exception-caught
            logger.error(f"LANDiscovery: Failed to bind to port {self.discovery_port}: {exc}")
            return

        while self._running:
            try:
                data, addr = sock.recvfrom(65535)
                self._handle_packet(data, addr)
            except Exception as exc:  # pylint: disable=broad-exception-caught
                if self._running:
                    logger.debug(f"LANDiscovery: Listen loop error: {exc}")

    def _handle_packet(self, data: bytes, addr: tuple):
        try:
            envelope = json.loads(data.decode())
            payload = envelope.get("data")
            sig = envelope.get("sig")

            if not payload or not sig:
                return

            # 1. Validation & Security
            data_str = json.dumps(payload, sort_keys=True)
            if not self._verify(data_str, sig):
                logger.warning(f"LANDiscovery: Invalid signature from {addr}")
                return

            remote_agent_id = payload.get("agent_id")
            if remote_agent_id == self.agent_id:
                return  # Self ignore

            msg_timestamp = payload.get("timestamp", 0)
            now = time.time()

            # Anti-Replay & Clock Skew Protection
            if abs(now - msg_timestamp) > self.MAX_CLOCK_SKEW:
                logger.debug(
                    f"LANDiscovery: Dropping message from {remote_agent_id} (Clock skew: {now - msg_timestamp:.2f}s)"
                )
                return

            if self._nonces.get(remote_agent_id, 0) >= msg_timestamp:
                return  # Replay or old message
            self._nonces[remote_agent_id] = msg_timestamp

            msg_type = payload.get("type")

            # 2. Registration
            self.update_peer(payload)

            # 3. Message Handling
            if msg_type == "ANNOUNCE":
                # Direct respond to announcer
                resp = self._create_message("ACK")
                self._ping_times[remote_agent_id] = now
                socket.socket(socket.AF_INET, socket.SOCK_DGRAM).sendto(resp, (addr[0], self.discovery_port))
                logger.info(f"LANDiscovery: New peer announced: {remote_agent_id} at {addr[0]}")

            elif msg_type == "ACK":
                # Calculate latency if we sent the request
                if remote_agent_id in self._ping_times:
                    latency = (now - self._ping_times.pop(remote_agent_id)) * 1000  # ms
                    with self._lock:
                        if remote_agent_id in self.registry:
                            self.registry[remote_agent_id].latency = latency

            elif msg_type == "SYNC":
                for peer_data in payload.get("peers", []):
                    self.update_peer(peer_data)

        except Exception as exc:  # pylint: disable=broad-exception-caught
            logger.debug(f"LANDiscovery: Malformed packet from {addr}: {exc}")

    def update_peer(self, data: Dict[str, Any]):
        """Registers or updates a peer in the local registry."""
        agent_id = data.get("agent_id")
        if not agent_id or agent_id == self.agent_id:
            return

        with self._lock:
            existing = self.registry.get(agent_id)
            latency = existing.latency if existing else data.get("latency", 0.0)

            # Update or Register
            self.registry[agent_id] = PeerInfo(
                agent_id=str(agent_id),
                ip=str(data.get("ip", "")),
                port=int(data.get("port", 0)),
                last_seen=time.time(),
                metadata=data.get("metadata", {}),
                trust_score=float(data.get("trust_score", 1.0)),
                latency=float(latency),
            )

    def get_active_peers(self, max_age: int = 300) -> List[PeerInfo]:
        """Returns list of peers seen within max_age seconds."""
        now = time.time()
        with self._lock:
            return [p for p in self.registry.values() if now - p.last_seen < max_age]

    def clear_stale_peers(self, max_age: int = 3600):
        """Removes peers not seen for an hour."""
        now = time.time()
        with self._lock:
            stale = [k for k, v in self.registry.items() if now - v.last_seen > max_age]
            for k in stale:
                del self.registry[k]
