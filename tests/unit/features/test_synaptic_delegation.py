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
Test Synaptic Delegation module.
"""

#!/usr/bin/env python3
import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.infrastructure.swarm.orchestration.swarm.director_agent import DirectorAgent

import asyncio

def test_delegation():
    print("--- Testing Synaptic Delegation ---")
    # Initialize DirectorAgent
    director = DirectorAgent("test_project.md")

    # Mocking fleet just in case
    class MockFleet:
        def __init__(self):
            self.agents = {}
    director.fleet = MockFleet()

    print(f"Available agents: {director._get_available_agents()}")

    # Test delegate_to (Dynamic import check)
    print("\nTesting dynamic delegation to CoderAgent...")

    async def run_test():
        try:
            result = await director.delegate_to("CoderAgent", "Hello Coder", "test_file.py")
            print(f"Delegation result: {result[:500]}...")
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            print(f"Delegation failed: {e}")

    asyncio.run(run_test())

if __name__ == "__main__":
    test_delegation()
