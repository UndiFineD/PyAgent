#!/usr/bin/env python3

import os
import logging
import sys
from pathlib import Path
from src.classes.fleet.FleetManager import FleetManager
from src.classes.orchestration.SelfImprovementOrchestrator import SelfImprovementOrchestrator

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def run_autonomous_maintenance():
    """
    Master entry point for autonomous fleet maintenance.
    - Improves speed, security, robustness, self-healing.
    - Prepares code for Rust migration via strong typing.
    - Optimizes databases for trillion-parameter scale.
    - Enforces local-first AI and recording.
    """
    workspace_root = Path(os.getcwd())
    print("=== SWARM AUTONOMOUS MAINTENANCE INITIATED ===")
    
    # 1. Initialize Fleet Manager (Core Hub)
    fleet = FleetManager(str(workspace_root))
    
    # 2. Trigger Self-Improvement Cycle
    print("[1/3] Running codebase improvement cycle (Speed, Security, Types)...")
    orchestrator = SelfImprovementOrchestrator(fleet)
    results = orchestrator.run_improvement_cycle(target_dir="src")
    
    print(f" - Files Scanned: {results['files_scanned']}")
    print(f" - Issues Identified: {results['issues_found']}")
    print(f" - Autonomous Fixes Applied: {results['fixes_applied']}")
    
    # 3. Relational Scale Optimization
    print("[2/3] Optimizing Relational Metadata (Trillion-Parameter Scalability)...")
    fleet.sql_metadata.optimize_db()
    
    # 4. Interaction Record Audit
    print("[3/3] Auditing AI Interaction Shards...")
    shard_count = len(list((workspace_root / "logs" / "external_ai_learning").glob("shard_*.jsonl.gz")))
    print(f" - Active Shards: {shard_count}")
    print(" - Recording Strategy: Compressed Monthly/Zlib (Active)")
    
    # 5. Rust Readiness Report
    untyped_files = [d['file'] for d in results['details'] if any(i['type'] == "Rust Readiness Task" and not i['fixed'] for i in d['issues'])]
    if untyped_files:
        print(f"\n--- PENDING RUST CONVERSION TARGETS ({len(untyped_files)}) ---")
        for f in untyped_files[:5]:
            print(f" - {f}")
        if len(untyped_files) > 5:
            print(f" ... and {len(untyped_files)-5} more.")
    else:
        print("\n[SUCCESS] Codebase type coverage reached optimal threshold for Rust migration.")

    print("\n=== MAINTENANCE CYCLE COMPLETE ===")

if __name__ == "__main__":
    run_autonomous_maintenance()
