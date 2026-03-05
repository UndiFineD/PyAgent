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

"""Unit tests for AgentRegistry resilience and lazy mapping."""

import os
import sys
import logging
from pathlib import Path

# Add the workspace root to sys.path

from src.classes.fleet.AgentRegistry import AgentRegistry

def test_resilience():
    logging.basicConfig(level=logging.INFO)
    print("🧪 Testing Resilience of AgentRegistry...")

    workspace_root = Path(os.getcwd())
    agents = AgentRegistry.get_agent_map(workspace_root)

    print("\n--- Attempting to load BrokenImportAgent ---")
    broken_agent = agents.get("BrokenImport")

    if broken_agent:
        print(f"✅ Found agent: {type(broken_agent).__name__}")
        res = broken_agent.improve_content("test")
        print(f"✅ Mock response: {res}")

        if "ERROR: Component 'BrokenImport' failed to load" in res:
            print("✅ ResilientStub successfully handled the broken import.")
        else:
            print("❌ Stub did not return expected error message.")
    else:
        print("❌ Agent not found even with stub.")

    print("\n🏁 Resilience Verification Complete.")

if __name__ == "__main__":
    test_resilience()
