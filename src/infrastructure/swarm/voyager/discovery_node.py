
"""
Discovery node.py module.
"""
# Copyright 2026 PyAgent Authors
# Phase 319: Multi-Cloud Teleportation (Discovery Node)

import asyncio
import contextlib
import socket
import uuid
from typing import Any, Dict, List, Optional

from zeroconf import IPVersion, ServiceBrowser, ServiceInfo, ServiceListener
from zeroconf.asyncio import AsyncZeroconf

from src.core.base.lifecycle.version import VERSION
from src.observability.structured_logger import StructuredLogger

logger = StructuredLogger(__name__)


class VoyagerPeerListener(ServiceListener):
    """Listens for other PyAgent Voyager peers on the local network."""

    def __init__(self, callback: Any, loop: asyncio.AbstractEventLoop):
        self.callback = callback
        self.loop = loop

    def add_service(self, zc: Any, type_: str, name: str) -> None:
        """Called by Zeroconf when a new service is discovered."""
        asyncio.run_coroutine_threadsafe(self._async_add_service(zc, type_, name), self.loop)

    async def _async_add_service(self, zc: Any, type_: str, name: str) -> None:
        """Asynchronously retrieves service info and notifies the callback."""
        info = await zc.async_get_service_info(type_, name)
        if info:
            logger.info(f"Voyager: Discovered peer {name} at {info.parsed_addresses()}")
            self.callback(info)

    def update_service(self, zc: Any, type_: str, name: str) -> None:
        """Called by Zeroconf when a service is updated (not used)."""

    def remove_service(self, zc: Any, type_: str, name: str) -> None:
        """Called by Zeroconf when a service is removed from the network."""
        logger.info(f"Voyager: Peer {name} removed from network.")


class DiscoveryNode:
    """
    DiscoveryNode handles decentralized peer advertisement and lookup.
    Uses mDNS (zeroconf) for Phase 1.0 of Project Voyager.
    """

    SERVICE_TYPE = "_pyagentv._tcp.local."

    def __init__(self, node_name: Optional[str] = None, port: int = 8000, transport_port: int = 5555):
        self.node_id = str(uuid.uuid4())[:8]
        self.node_name = node_name or f"PyAgent-{self.node_id}"
        self.port = port
        self.transport_port = transport_port
        self.aiozc: Optional[AsyncZeroconf] = None
        self.peers: Dict[str, ServiceInfo] = {}
        self.info: Optional[ServiceInfo] = None
        self.browser: Optional[ServiceBrowser] = None

        # Local IP detection
        self.local_ip = self._get_local_ip()

    def _get_local_ip(self) -> str:
        """Returns the local IPv4 address of the node."""
        ip_address = "127.0.0.1"
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        with contextlib.suppress(Exception):
            # doesn't even have to be reachable
            s.connect(("10.255.255.255", 1))
            ip_address = s.getsockname()[0]
        s.close()
        return ip_address

    async def start_advertising(self):
        """Broadcasts this node to the local network."""
        import os
        import platform

        if self.aiozc is None:
            self.aiozc = AsyncZeroconf(ip_version=IPVersion.V4Only)

        # Basic resource detection for Voyager Synergy (Phase 4.0)
        cpu_cores = str(os.cpu_count() or 1)
        ram_gb = "8.0" # Default
        try:
             import psutil
             ram_gb = f"{psutil.virtual_memory().total / (1024**3):.1f}"
        except ImportError:
             pass

        desc = {
            "version": VERSION,
            "node_id": self.node_id,
            "transport_port": str(self.transport_port),
            "status": "Online",
            "cpu_cores": cpu_cores,
            "ram_gb": ram_gb,
            "os": platform.system(),
        }

        self.info = ServiceInfo(
            self.SERVICE_TYPE,
            f"{self.node_name}.{self.SERVICE_TYPE}",
            addresses=[socket.inet_aton(self.local_ip)],
            port=self.port,
            properties=desc,
            server=f"{self.node_name}.local.",
        )

        logger.info(f"Voyager: Advertising node {self.node_name} at {self.local_ip}:{self.port}")
        await self.aiozc.zeroconf.async_register_service(self.info)

    async def start_discovery(self):
        """Starts browsing for other Voyager peers."""
        if self.aiozc is None:
            self.aiozc = AsyncZeroconf(ip_version=IPVersion.V4Only)

        logger.info("Voyager: Starting peer discovery browser...")
        loop = asyncio.get_running_loop()
        self.browser = ServiceBrowser(
            self.aiozc.zeroconf, self.SERVICE_TYPE, VoyagerPeerListener(self._peer_discovered, loop)
        )

    def _peer_discovered(self, info: ServiceInfo):
        """Internal callback for when a peer is discovered via Zeroconf."""
        if info.name not in self.peers:
            self.peers[info.name] = info
            logger.info(f"Voyager: Peer Registry updated. Total peers: {len(self.peers)}")

    async def stop(self):
        """Stops advertising and discovery."""
        if self.aiozc:
            if self.info:
                await self.aiozc.zeroconf.async_unregister_service(self.info)
            await self.aiozc.async_close()
            self.aiozc = None
        logger.info(f"Voyager: Discovery Node {self.node_name} stopped.")

    def get_active_peers(self) -> List[Dict[str, Any]]:
        """Returns a list of active peers found on the network."""
        results = []
        for name, info in self.peers.items():
            results.append(
                {
                    "name": name,
                    "addresses": info.parsed_addresses(),
                    "port": info.port,
                    "properties": {
                        k.decode() if isinstance(k, bytes) else k: v.decode() if isinstance(v, bytes) else v
                        for k, v in info.properties.items()
                    },
                }
            )
        return results

    def resolve_synapse_address(self, peer_name: str) -> Optional[tuple[str, int]]:
        """
        Phase 319: Resolves a peer name or node_id to an (IP, transport_port) tuple.
        This enables decentralized routing without hardcoded IPs.
        """
        for name, info in self.peers.items():
            props = {
                k.decode() if isinstance(k, bytes) else k: v.decode() if isinstance(v, bytes) else v
                for k, v in info.properties.items()
            }

            # Match by node_name, node_id, or mDNS service name
            if peer_name == props.get("node_id") or peer_name == name.split(".")[0] or peer_name in name:
                addrs = info.parsed_addresses()
                t_port = props.get("transport_port")
                if addrs and t_port:
                    return (addrs[0], int(t_port))

        return None


if __name__ == "__main__":
    import sys

    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    async def run_test():
        """Manual test runner for discovery node."""
        node = DiscoveryNode()
        try:
            await node.start_advertising()
            await node.start_discovery()
            print("Discovery Node Active. Press Ctrl+C to stop.")
            while True:
                await asyncio.sleep(5)
                peers = node.get_active_peers()
                if peers:
                    print(f"Found {len(peers)} peers: {[p['name'] for p in peers]}")
        except asyncio.CancelledError:
            pass
        finally:
            await node.stop()

    try:
        asyncio.run(run_test())
    except KeyboardInterrupt:
        print("\nStopping discovery node...")
