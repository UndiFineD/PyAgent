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
Module: code_improver
Autonomous Codebase Evolution Loop for self-optimizing system logic.
"""

from __future__ import annotations
import asyncio
import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.infrastructure.swarm.fleet.fleet_manager import FleetManager

logger = logging.getLogger(__name__)


class EvolutionLoop:
    """
    Background process that proactively improves the PyAgent core.
    Follows Pillar 8: Self-Improving Intelligence.
    """

    def __init__(self, fleet: FleetManager):
        self.fleet = fleet
        self.running = False

    async def start(self):
        """Starts the autonomous evolution cycle."""
        self.running = True
        logger.info("Autonomous Evolution Loop engaged.")

        while self.running:
            # 1. Performance Evolution (Python -> Rust / Refactor)
            stats = self.fleet.resource_monitor.get_latest_stats()
            if stats.get("cpu_percent", 100) < 30:  # Idle threshold
                await self._identify_and_improve_bottleneck()

            # 2. Resilience Evolution (RAID-10 Sharding Update)
            if hasattr(self.fleet, "run_resilience_audit"):
                await self.fleet.run_resilience_audit()

            # 3. Cognitive Evolution (Synaptic Pruning - Pillar 6)
            if hasattr(self.fleet, "pruning_orchestrator"):
                logger.info("Evolution: Triggering synaptic pruning cycle...")
                self.fleet.pruning_orchestrator.run_pruning_cycle(threshold=0.15)

            await asyncio.sleep(3600)  # Once per hour

    async def _identify_and_improve_bottleneck(self):
        """Heuristic-based logic bottleneck identification and Rust acceleration."""
        logger.info("Evolution: Identifying code bottlenecks (Pillar 8)...")

        # 1. Complexity-based Rust Candidate Identification
        python_files = list(self.fleet.workspace_root.rglob("*.py"))
        rust_candidates = []

        for pfile in python_files:
            if "__" in pfile.name or "test" in pfile.name.lower():
                continue

            # Heuristic: Large files with high loop density or many mathematical ops
            try:
                content = pfile.read_text(encoding="utf-8")
                if len(content) > 15000:  # >15KB
                    loop_count = content.count("for ") + content.count("while ")
                    math_count = (content.count("math.") + content.count("np.") +
                                  content.count(" + ") + content.count(" * "))

                    if loop_count > 20 or math_count > 50:
                        rust_candidates.append(str(pfile.relative_to(self.fleet.workspace_root)))
            except Exception:
                continue

        if rust_candidates:
            target = rust_candidates[0]
            logger.info(f"Evolution: Target identified for Rust acceleration: {target}")
            try:
                # Dispatch a special 'rust_porter' shard if available, or use Coder
                await self.fleet.delegate_to(
                    "coder",
                    prompt=f"AUTONOMOUS_EVOLUTION: The function in {target} is a bottleneck. "
                    f"Implement a high-performance Rust version in 'rust_lib/src/optimized/' "
                    f"and provide a Python FFI bridge using PyO3."
                )
            except Exception as e:
                logger.error(f"Evolution: Rust porting request failed: {e}")

        # 2. General logic refactor for the core
        target_core = "src/core/base/lifecycle/base_agent.py"
        try:
            await self.fleet.delegate_to(
                "coder",
                prompt=(f"EVOLUTION_LOOP: Review {target_core} for redundancy and "
                        f"apply architectural patterns like Mixins for better isolation."),
                target_file=target_core
            )
        except Exception as e:
            logger.error("Evolution: Refactor failed: %s", e)
