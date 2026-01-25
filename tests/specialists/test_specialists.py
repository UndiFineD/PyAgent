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
Test Specialists module.
"""

import sys
from pathlib import Path

# Add src to path

from src.infrastructure.swarm.orchestration.swarm.director_agent import DirectorAgent
from src.logic.agents.development.rust_agent import RustAgent
from src.logic.agents.development.go_agent import GoAgent
from src.logic.agents.cognitive.knowledge_agent import KnowledgeAgent


def test_specialists_exist() -> None:
    print("Checking specialist availability...")
    agents = [
        DirectorAgent("test_plan.md"),
        RustAgent("test.rs"),
        GoAgent("test.go"),
        KnowledgeAgent("."),
    ]
    for agent in agents:
        print(f"Verified: {agent.__class__.__name__}")


def test_knowledge_agent_scan() -> None:
    print("\nTesting KnowledgeAgent scanning...")
    ka = KnowledgeAgent(Path("."))
    context = ka.scan_workspace("DirectorAgent")
    print(f"KnowledgeAgent found {len(context)} chars of context.")
    assert "DirectorAgent" in context
    print("KnowledgeAgent scan: SUCCESS")


if __name__ == "__main__":
    try:
        test_specialists_exist()
        test_knowledge_agent_scan()
        print("\nAll specialist sanity checks: PASSED")
    except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
        print(f"\nVerification FAILED: {e}")
        sys.exit(1)
