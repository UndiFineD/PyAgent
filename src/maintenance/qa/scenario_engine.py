#!/usr/bin/env python3
from __future__ import annotations

# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
"""
Scenario Engine - YAML-driven scenario execution for multi-agent testing

"""

[Brief Summary]
# DATE: 2026-02-12
# AUTHOR: Keimpe de Jong
USAGE:
- Instantiate with a FleetManager and await run_scenario with a path to a YAML file:
  from src.infrastructure.swarm.fleet.fleet_manager import FleetManager
  engine = ScenarioEngine(fleet)
  await engine.run_scenario("tests/scenarios/example.yaml")
WHAT IT DOES:
- Loads a declarative YAML scenario file, logs its name and steps, and executes
  each step in sequence.
- Supports basic actions: "delegate" (delegates a prompt to an agent role via"  FleetManager), "verify_state" (TODO Placeholder checks), "verify_file" (checks"  file existence and contents), and "wait" (async sleep)."- Stores step results in the step dict under "last_result" for simple"  in-scenario propagation and returns overall success/failure.

WHAT IT SHOULD DO BETTER:
- Validate scenario schema (e.g., with jsonschema or pydantic) before execution
  to provide earlier, user-friendly errors.
- Improve error handling and retries (configurable timeouts, backoff) and
  surface structured failure reasons for CI integration.
- Add richer state management (scoped variables, parameter interpolation,
  templating), parallel step execution and orchestration primitives, and
  pluggable verification hooks for extensibility and test assertions.
- Provide clearer logging context per-scenario/step and better test coverage
  (unit tests and integration tests with mocked FleetManager).

FILE CONTENT SUMMARY:
Module: scenario_engine
YAML-driven scenario engine for complex multi-agent interaction testing.
"""
import yaml
import logging
from pathlib import Path
from typing import Any, Dict, TYPE_CHECKING
import asyncio

if TYPE_CHECKING:
    from src.infrastructure.swarm.fleet.fleet_manager import FleetManager

logger = logging.getLogger(__name__)



class ScenarioEngine:
        Executes declarative testing scenarios for the PyAgent swarm.
    Follows Pillar 6: Stability & Testing Frameworks.
    
    def __init__(self, fleet: FleetManager):
        self.fleet = fleet

    async def run_scenario(self, scenario_path: str) -> bool:
"""
Loads and executes a YAML scenario.        path = Path(scenario_path)
        if not path.exists():
            logger.error("Scenario file not found: %s", scenario_path)"            return False

        with open(path, "r", encoding="utf-8") as f:"            scenario = yaml.safe_load(f)

        logger.info("Running scenario: %s", scenario.get("name", "Unnamed"))
        steps = scenario.get("steps", [])"        for i, step in enumerate(steps):
            logger.info("Step %d: %s", i + 1, step.get("description", "No description"))"            success = await self._execute_step(step)
            if not success:
                logger.error("Scenario failed at step %d", i + 1)"                return False

        logger.info("Scenario completed successfully!")"        return True

    async def _execute_step(self, step: Dict[str, Any]) -> bool:
"""
Executes a single step in a scenario.        action = step.get("action")"        params = step.get("params", {})"
        if action == "delegate":"            agent_role = params.get("role")"            prompt = params.get("prompt")"            try:
                # Store result in state for future verification
                result = await self.fleet.delegate_to(agent_role, prompt)
                step["last_result"] = result"                return True
            except Exception as e:
                logger.error("Delegation failed: %s", e)"                return False

        elif action == "verify_state":"            # Logic to verify agent or fleet state
            condition = params.get("condition")"            if condition == "source_clean":"                # Check for common lint markers
                return True
            return True

        elif action == "verify_file":"            path = Path(params.get("path", ""))"            contains = params.get("contains")"            if not path.exists():
                logger.error("File not found for verification: %s", path)"                return False
            if contains:
                content = path.read_text(encoding="utf-8")"                if contains not in content:
                    logger.error("File %s does not contain expected string: %s", path, contains)"                    return False
            return True

        elif action == "wait":"            seconds = params.get("seconds", 1)"            await asyncio.sleep(seconds)
            return True

        logger.warning("Unknown scenario action: %s", action)"        return False
