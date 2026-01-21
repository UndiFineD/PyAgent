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


"""Validation script for Phase 12: Cognitive Architectures."""

from __future__ import annotations
from src.core.base.lifecycle.version import VERSION
import logging
from pathlib import Path
from src.infrastructure.swarm.fleet.fleet_manager import FleetManager

__version__ = VERSION


def test_cognitive_features() -> None:
    """Validate metacognitive and Theory of Mind features."""
    logging.basicConfig(level=logging.INFO)
    root = Path(str(Path(__file__).resolve().parents[5]) + "")
    fleet = FleetManager(str(root))

    print("--- Phase 12: Metacognitive Monitoring ---")
    reasoning = "I think perhaps this might work, but i am not sure if it is likely the best way."
    eval_res = fleet.metacognition.evaluate_reasoning(
        "TestAgent", "Risk Analysis", reasoning
    )
    print(f"Metacognitive Eval: {eval_res}")

    print("\n--- Phase 12: Theory of Mind ---")
    fleet.tom.update_model(
        "CoderAgent", {"domain": "Python", "strength": "refactoring"}
    )
    fleet.tom.update_model(
        "DataAgent", {"domain": "SQL", "strength": "query_optimization"}
    )

    collaborators = fleet.tom.suggest_collaborator("I need help with a Python function")
    print(f"Suggested Collaborators for Python: {collaborators}")

    knowledge = fleet.tom.estimate_knowledge("DataAgent", "Database Schema")
    print(f"DataAgent knowledge estimate for Database: {knowledge}")

    print("\n--- Phase 12: Sleep & Consolidate ---")
    fleet.consolidator.record_interaction("CoderAgent", "Refactor core.py", "success")

    fleet.consolidator.record_interaction("DataAgent", "Clean logs", "success")

    report = fleet.consolidator.sleep_and_consolidate()
    print(report)

    memory_query = fleet.consolidator.query_long_term_memory("Refactor")
    print(f"Long-term memory search result: {memory_query}")

    print("\nCognitive features validation COMPLETED.")


if __name__ == "__main__":
    test_cognitive_features()
