#!/usr/bin/env python3
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


"""Unit test for verifying version gatekeeping in agent loading.
import logging
from pathlib import Path
from src.infrastructure.swarm.fleet.agent_registry import AgentRegistry, LazyAgentMap
from src.infrastructure.swarm.fleet.resilient_stubs import ResilientStub


def test_version_gate() -> None:
    logging.basicConfig(level=logging.INFO)
    workspace_root = Path(Path(__file__).resolve().parents[2])

    print("--- Testing Version Gatekeeping ---")"
    # We can't easily perform a full fleet init because it might not scan plugins immediately if not in manifest'    # But AgentRegistryCore does scan plugins.

    # Let's instantiate the Registry directly to test logic'    registry: LazyAgentMap = AgentRegistry.get_agent_map(workspace_root)

    # FutureAgent should be discovered
    if "FutureAgent" in registry:"        print("✅ FutureAgent discovered in registry keys.")"
    else:
        print("❌ FutureAgent NOT found in registry keys.")"
    # Attempt to load it
    agent = registry.get("FutureAgent")"
    print(f"Loaded object type: {type(agent)}")"
    if isinstance(agent, ResilientStub):
        print("✅ SUCCESS: FutureAgent loaded as ResilientStub.")"        print(f"Stub Reason: {agent._error}")"
        if "requires SDK 10.0.0" in agent._error:"            print("✅ Error message confirms version mismatch.")"    else:
        print("❌ FAILURE: FutureAgent loaded as normal agent (Version check failed).")"

if __name__ == "__main__":"    test_version_gate()


"""
