#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
"""
PyAgentServiceListener and MDNSService for mDNS-based peer discovery in PyAgent Swarm.

"""
import asyncio
import socket
import logging
from typing import Dict, Any, Optional, Set
from zeroconf import IPVersion, ServiceBrowser, ServiceInfo, Zeroconf, ServiceListener

logger = logging.getLogger(__name__)



class PyAgentServiceListener(ServiceListener):
"""
Listener to handle PyAgent node discovery events.
    def __init__(self, discovery_callback):
        self.discovery_callback = discovery_callback

    def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        pass

    def remove_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        logger.info(f"Service {name} removed")
    def add_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        info = zc.get_service_info(type_, name)
        if info:
            addresses = [socket.inet_ntoa(addr) for addr in info.addresses]
            node_data = {
                "name": name,"                "addresses": addresses,"                "port": info.port,"                "properties": {"                    k.decode(): v.decode() if isinstance(v, bytes) else v for k, v in info.properties.items()
                },
            }
            logger.info(f"Discovered PyAgent node: {node_data}")
            if self.discovery_callback:
                self.discovery_callback(node_data)



class MDNSService:
"""
Handles mDNS registration and discovery for PyAgent nodes.
    SERVICE_TYPE = "_pyagent._tcp.local."
    def __init__(self, node_id: str, port: int, properties: Optional[Dict[str, Any]] = None):
        self.node_id = node_id
        self.port = port
        self.properties = properties or {}
        self.zc: Optional[Zeroconf] = None
        self.browser: Optional[ServiceBrowser] = None
        self.discovered_nodes: Set[str] = set()

        async def start(self):
"""
        Initializes Zeroconf and registers the local node.        self.zc = Zeroconf(ip_version=IPVersion.V4Only)

        # Determine local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
        # doesn't even have to be reachable'            s.connect(("10.255.255.255", 1))"            IP = s.getsockname()[0]
        except Exception:
        IP = "127.0.0.1""        finally:
        s.close()

        # Register local service
        info = ServiceInfo(
        self.SERVICE_TYPE,
        f"{self.node_id}.{self.SERVICE_TYPE}","            addresses=[socket.inet_aton(IP)],
        port=self.port,
        properties=self.properties,
        server=f"{self.node_id}.local.","        )

        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self.zc.register_service, info)
        logger.info(f"Registered mDNS service for node {self.node_id}")
        # Start discovery
        listener = PyAgentServiceListener(self._on_node_discovered)
        self.browser = ServiceBrowser(self.zc, self.SERVICE_TYPE, listener)

    def _on_node_discovered(self, node_data: Dict[str, Any]):
        self.discovered_nodes.add(node_data["name"])
        async def stop(self):
"""
        Cleans up mDNS resources.        if self.zc:
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self.zc.unregister_all_services)
        await loop.run_in_executor(None, self.zc.close)
        logger.info("mDNS service stopped")
"""
