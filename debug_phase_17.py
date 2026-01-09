#!/usr/bin/env python3
import logging
import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent))

from src.classes.fleet.FleetManager import FleetManager
from src.classes.specialized.WebAgent import WebAgent

def test_phase_17():
    logging.basicConfig(level=logging.INFO)
    workspace = os.getcwd()
    fleet = FleetManager(workspace)
    
    print("\n--- Phase 17: WebAgent (Simulation) ---")
    web_agent = WebAgent(str(Path(workspace) / "src/classes/specialized/WebAgent.py"))
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
