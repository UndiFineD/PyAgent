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
Test script for LANDiscovery network functionality.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.infrastructure.swarm.network.lan_discovery import LANDiscovery

def test_network_detection():
    """Test network detection and configuration."""
    print("Testing LANDiscovery network detection...")

    # Create a discovery instance with broadcasting enabled
    discovery = LANDiscovery(
        agent_id="test-agent",
        service_port=8080,
        enable_broadcast=True,  # Enable broadcasting to test subnet detection
        auto_find_port=True
    )

    # Test network info
    info = discovery.get_network_info()
    print(f"Network Info: {info}")

    # Test port availability
    port_available = discovery._test_port_available(9999)
    print(f"Port 9999 available: {port_available}")

    # Test finding available port
    available_port = discovery.find_available_port(9999, 10)
    print(f"Available port starting from 9999: {available_port}")

    # Test connectivity details
    connectivity = discovery.test_network_connectivity()
    print(f"Connectivity details: {connectivity}")

    print("Network detection test completed.")

if __name__ == "__main__":
    test_network_detection()