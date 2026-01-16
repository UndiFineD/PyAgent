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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

from __future__ import annotations
from src.core.base.Version import VERSION
import os
import logging
from pathlib import Path
from src.infrastructure.fleet.FleetManager import FleetManager
from src.infrastructure.orchestration.intel.SelfImprovementOrchestrator import (
    SelfImprovementOrchestrator,
)

__version__ = VERSION

# Initialize logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def run_autonomous_maintenance() -> None:
    """
    Master entry point for autonomous fleet maintenance.
    - Improves speed, security, robustness, self-healing.
    - Prepares code for Rust migration via strong typing.
    - Optimizes databases for trillion-parameter scale.
    - Enforces local-first AI and recording.
    """
    workspace_root = Path(os.getcwd())
    logging.info("=== SWARM AUTONOMOUS MAINTENANCE INITIATED ===")

    # 1. Initialize Fleet Manager (Core Hub)
    fleet = FleetManager(str(workspace_root))

    # 2. Trigger Self-Improvement Cycle
    logging.info("[1/3] Running codebase improvement cycle (Speed, Security, Types)...")
    orchestrator = SelfImprovementOrchestrator(fleet)
    results = orchestrator.run_improvement_cycle(target_dir="src")

    logging.info(f" - Files Scanned: {results['files_scanned']}")
    logging.info(f" - Issues Identified: {results['issues_found']}")
    logging.info(f" - Autonomous Fixes Applied: {results['fixes_applied']}")

    # 3. Relational Scale Optimization

    logging.info(
        "[2/3] Optimizing Relational Metadata (Trillion-Parameter Scalability)..."
    )
    fleet.sql_metadata.optimize_db()

    # 4. Interaction Record Audit
    logging.info("[3/3] Auditing AI Interaction Shards...")
    shard_count = len(
        list(
            (workspace_root / "data/logs" / "external_ai_learning").glob(
                "shard_*.jsonl.gz"
            )
        )
    )
    logging.info(f" - Active Shards: {shard_count}")

    logging.info(" - Recording Strategy: Compressed Monthly/Zlib (Active)")

    # 5. Rust Readiness Report
    untyped_files = [
        d["file"]
        for d in results["details"]
        if any(
            i["type"] == "Rust Readiness Task" and not i["fixed"] for i in d["issues"]
        )
    ]
    if untyped_files:
        logging.info(f"--- PENDING RUST CONVERSION TARGETS ({len(untyped_files)}) ---")
        for f in untyped_files[:5]:
            logging.info(f" - {f}")
        if len(untyped_files) > 5:
            logging.info(f" ... and {len(untyped_files) - 5} more.")

    else:
        logging.info(
            "[SUCCESS] Codebase type coverage reached optimal threshold for Rust migration."
        )

    logging.info("=== MAINTENANCE CYCLE COMPLETE ===")


if __name__ == "__main__":
    run_autonomous_maintenance()
