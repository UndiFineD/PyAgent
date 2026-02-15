#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test script for LANDiscovery network functionality.
"""

from src.infrastructure.swarm.network.lan_discovery import LANDiscovery

def test_network_detection():
    discovery = LANDiscovery(
        agent_id="test-agent",
        service_port=8080,
        enable_broadcast=True,
        auto_find_port=True
    )
    info = discovery.get_network_info()
    assert isinstance(info, dict)
    port_available = discovery._test_port_available(9999)
    assert isinstance(port_available, bool)
    available_port = discovery.find_available_port(9999, 10)
    assert isinstance(available_port, int)
    connectivity = discovery.test_network_connectivity()
    assert isinstance(connectivity, dict)
