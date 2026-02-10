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
from pathlib import Path
from typing import Any, TYPE_CHECKING

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
            # Only run if system load is low
            stats = self.fleet.resource_monitor.get_latest_stats()
            if stats.get("cpu_percent", 100) < 30: # Idle threshold
                await self._identify_and_improve_bottleneck()
            
            await asyncio.sleep(3600) # Once per hour

    async def _identify_and_improve_bottleneck(self):
        """Heuristic-based logic bottleneck identification."""
        logger.info("Evolution: Identifying code bottlenecks...")
        
        # Pillar 8: Identify Python functions for Rust migration
        python_files = list(self.fleet.workspace_root.rglob("*.py"))
        candidate = None
        
        for pfile in python_files:
            if "__" in pfile.name: continue
            # Look for large, complex files (proxy for migration need)
            if pfile.stat().st_size > 20000: # >20KB
                candidate = str(pfile.relative_to(self.fleet.workspace_root))
                break

        if candidate:
            logger.info(f"Evolution: Suggesting Rust migration for {candidate}")
            try:
                await self.fleet.delegate_to(
                    "coder", 
                    prompt=f"Analyze {candidate} and suggest which logic parts should be migrated to Rust for performance."
                )
            except Exception as e:
                logger.error(f"Evolution: Analysis failed: {e}")
        
        # standard refactor cleanup
        target_file = "src/core/base/lifecycle/base_agent_core.py"
        try:
            await self.fleet.delegate_to(
                "coder", 
                prompt=f"Identify and refactor any performance bottlenecks in {target_file}.",
                target_file=target_file
            )
            logger.info("Evolution: Successfully refactored %s", target_file)
        except Exception as e:
            logger.error("Evolution: Refactor failed: %s", e)
