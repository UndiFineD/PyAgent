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
Test Resilience Community module.
"""

#!/usr/bin/env python3
import logging
from pathlib import Path

# Add project root to sys.path

from src.infrastructure.swarm.fleet.agent_registry import AgentRegistry


def test_broken_community_plugin() -> None:
    print("--- Running Broken Plugin Resilience Test ---")
    workspace = Path(".").resolve()
    agents = AgentRegistry.get_agent_map(workspace)

    print("Attempting to load BrokenCommunity...")
    try:
        agent = agents["BrokenCommunity"]
        print(f"Agent Type: {type(agent).__name__}")

        # This should fail gracefully or show it's a stub

        from src.infrastructure.swarm.fleet.resilient_stubs import ResilientStub

        if isinstance(agent, ResilientStub):
            print("Successfully caught broken plugin and returned ResilientStub!")
            # Use get_status() to see the real error since __getattr__ traps other field access

            status = agent.get_status()
            print(f"Stub Error Detail: {status['error']}")
        else:
            print("Wait, it loaded? (Unexpected)")

    except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
        print(f"Script crashed (Unexpected): {e}")

    print("\nVerifying that other agents still work...")
    try:
        demo = agents["CommunityDemo"]
        print(f"CommunityDemo still works: {demo.run('test')}")
    except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
        print(f"CommunityDemo failed because of broken plugin: {e}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR)
    test_broken_community_plugin()
