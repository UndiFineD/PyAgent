#!/usr/bin/env python3

"""Validation script for Phase 8: Production Readiness & Phase 9: Security/Infra."""

import logging
from pathlib import Path
from src.infrastructure.fleet.FleetManager import FleetManager

def test_production_features() -> None:
    """Validate Kubernetes deployment and telemetry export features."""
    logging.basicConfig(level=logging.INFO)
    root = Path("c:/DEV/PyAgent")
    fleet = FleetManager(str(root))
    
    print("--- Phase 8: Kubernetes & Observability ---")
    manifest = fleet.kubernetes.deploy_agent_pod("ResearchAgent")
    print(f"Generated K8s Manifest snippet: {manifest[:100]}...")
    
    fleet.telemetry.log_event("TestAgent", "START", {"msg": "Observability Check"})
    elk_status = fleet.telemetry.export_to_elk()
    print(f"ELK Export: {elk_status}")
    
    metrics = fleet.telemetry.get_metrics()
    print(f"Prometheus Metrics Preview:\n{metrics[:100]}...")

    print("\n--- Phase 9: Security & GPU Scaling ---")
    rot_msg = fleet.security_audit.rotate_certificates("fleet-01")
    print(rot_msg)
    
    gpu_actions = fleet.gpu_scaling.monitor_memory_pressure()
    print(f"GPU Scaling Actions: {gpu_actions}")
    
    print("\nProduction readiness validation COMPLETED.")

if __name__ == "__main__":
    test_production_features()
