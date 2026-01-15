#!/usr/bin/env python3

import logging
import os
import asyncio

# Add project root to path

from src.infrastructure.fleet.FleetManager import FleetManager




async def run_phase39():
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    workspace_root = os.getcwd()
    fleet = FleetManager(workspace_root)

    print("\n--- Testing Phase 39: Fractal Knowledge, Speciation & Load Balancing ---")

    # 1. Test Fractal Knowledge Synthesis
    topic = "Market Sentiment on AI GPUs"
    agents = ["SQL", "Financial", "Reasoner"]
    # Check if async
    res = fleet.fractal_knowledge.synthesize(topic, agents)
    if asyncio.iscoroutine(res):
        synthesis = await res
    else:
        synthesis = res
    print(f"FractalKnowledge: Unified Wisdom: {synthesis['unified_wisdom'][:80]}...")

    # 2. Test Speciation
    domain = "Kubernetes-SRE"
    res = fleet.speciation_orchestrator.speciate(domain)
    if asyncio.iscoroutine(res):
        spec_fleet = await res










    else:
        spec_fleet = res
    print(f"SpeciationOrchestrator: Created '{spec_fleet['breed_name']}' with agents: {spec_fleet['agents']}")














    # 3. Test Load Balancer
    res = fleet.load_balancer.balance_request("Mobile", "Fetch Fleet Status")
    if asyncio.iscoroutine(res):


        lb_resp = await res
    else:



        lb_resp = res
    print(f"LoadBalancer: Request Accepted: {lb_resp['status']}, Worker: {lb_resp['assigned_model']}")

    # Assertions
    assert synthesis['topic'] == topic, "Fractal synthesis failed!"



    assert len(spec_fleet['agents']) > 0, "Speciation failed!"
    assert lb_resp['status'] == "ACCEPTED", "Load balancing failed!"


    print("\n[SUCCESS] Phase 39 verification complete.")





def test_phase39() -> None:
    asyncio.run(run_phase39())





if __name__ == "__main__":
    test_phase39()
