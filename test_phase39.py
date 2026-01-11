#!/usr/bin/env python3

import logging
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from src.classes.fleet.FleetManager import FleetManager

def test_phase39() -> None:
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    workspace_root = os.getcwd()
    fleet = FleetManager(workspace_root)
    
    print("\n--- Testing Phase 39: Fractal Knowledge, Speciation & Load Balancing ---")
    
    # 1. Test Fractal Knowledge Synthesis
    topic = "Market Sentiment on AI GPUs"
    agents = ["SQL", "Financial", "Reasoner"]
    synthesis = fleet.fractal_knowledge.synthesize(topic, agents)
    print(f"FractalKnowledge: Unified Wisdom: {synthesis['unified_wisdom'][:80]}...")
    
    # 2. Test Speciation
    domain = "Kubernetes-SRE"
    spec_fleet = fleet.speciation_orchestrator.speciate(domain)
    print(f"SpeciationOrchestrator: Created '{spec_fleet['breed_name']}' with agents: {spec_fleet['agents']}")
    
    # 3. Test Load Balancer
    lb_resp = fleet.load_balancer.balance_request("Mobile", "Fetch Fleet Status")
    print(f"LoadBalancer: Request Accepted: {lb_resp['status']}, Worker: {lb_resp['assigned_worker']}")
    
    # Assertions
    assert synthesis['topic'] == topic, "Fractal synthesis failed!"
    assert len(spec_fleet['agents']) > 0, "Speciation failed!"
    assert lb_resp['status'] == "ACCEPTED", "Load balancing failed!"
    
    print("\n[SUCCESS] Phase 39 verification complete.")

if __name__ == "__main__":
    test_phase39()
