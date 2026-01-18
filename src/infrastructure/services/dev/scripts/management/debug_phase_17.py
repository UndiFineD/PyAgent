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

# Add src to path

from __future__ import annotations
from src.core.base.version import VERSION
import logging
import sys
import os
from pathlib import Path
from src.infrastructure.fleet.FleetManager import FleetManager
from src.logic.agents.intelligence.WebAgent import WebAgent

sys.path.append(str(Path(__file__).parent))

__version__ = VERSION

def test_phase_17() -> None:
    """Validate WebAgent simulation and SaaS deployment gateway."""
    logging.basicConfig(level=logging.INFO)
    workspace = os.getcwd()
    fleet = FleetManager(workspace)
    
    print("\n--- Phase 17: WebAgent (Simulation) ---")
    web_agent = WebAgent(str(Path(workspace) / "src/logic/agents/intelligence/WebAgent.py"))
    search_results = web_agent.search_web("PyAgent GitHub")
    print(f"Search Results: {search_results}")
    
    # Simulate fetching a page (mocked)
    content = web_agent.fetch_page_content("https://github.com/UndiFineD/PyAgent")
    print(f"Fetched Content Length: {len(content)}")

    print("\n--- Phase 17: Deployment Manager ---")
    dockerfile = fleet.deployment.generate_docker_manifest("coder-node")
    compose = fleet.deployment.generate_compose_orchestration(num_replicas=2)
    print(f"Dockerfile created: {dockerfile}")
    print(f"Compose created: {compose}")

    print("\n--- Phase 17: SaaS Gateway ---")
    key = fleet.gateway.create_api_key("tenant_001", daily_quota=5)
    valid = fleet.gateway.validate_request(key)
    status = fleet.gateway.get_quota_status(key)
    print(f"API Key Validated: {valid}")
    print(f"Quota Status: {status}")

    if len(search_results) > 0 and "Dockerfile" in dockerfile and valid:
        print("\nWeb-Native & SaaS Deployment validation COMPLETED.")
    else:
        print("\nWeb-Native & SaaS Deployment validation FAILED.")

if __name__ == "__main__":
    test_phase_17()