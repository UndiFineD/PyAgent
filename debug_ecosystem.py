#!/usr/bin/env python3

"""Validation script for Phase 10: Human-Agent Teaming & Ecosystem."""

import logging
import json
from pathlib import Path
from src.classes.fleet.FleetManager import FleetManager

def test_ecosystem_features():
    logging.basicConfig(level=logging.INFO)
    root = Path("c:/DEV/PyAgent")
    fleet = FleetManager(str(root))
    
    print("--- Phase 10: Human-Agent Teaming ---")
    approval_id = fleet.hitl.request_approval("KernelAgent", "Delete Root Directory", {"path": "/"})
    print(f"Requested HITL Approval: {approval_id}")
    status = fleet.hitl.check_approval_status(approval_id)
    print(f"Approval Status: {status}")
    
    print("\n--- Phase 10: Fleet Web UI ---")
    topology = fleet.web_ui.get_fleet_topology()
    print(f"Fleet Topology (Sample): {topology[:100]}...")
    
    print("\n--- Phase 10: Public API ---")
    spec = fleet.api_engine.generate_openapi_spec()
    print(f"OpenAPI Spec (Sample): {spec[:100]}...")
    
    ext_msg = fleet.api_engine.register_external_tool({"name": "SlackNotifier", "url": "https://api.slack.com"})
    print(ext_msg)
    
    print("\nEcosystem features validation COMPLETED.")

if __name__ == "__main__":
    test_ecosystem_features()
