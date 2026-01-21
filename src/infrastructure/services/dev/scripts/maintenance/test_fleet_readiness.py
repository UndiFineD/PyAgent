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
Verification script to ensure core fleet components are correctly refactored
and importable. Ported from temp/verify_refactor.py.
"""

import sys
from pathlib import Path

# Add project root to sys.path
project_root = Path(__file__).resolve().parents[5]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

def test_imports():
    """Attempts to instantiate major agents to verify import health."""
    try:
        from src.infrastructure.swarm.fleet.fleet_manager import FleetManager
        from src.logic.agents.specialists.handy_agent import HandyAgent

        print(f"Detecting workspace root at: {project_root}")

        fleet = FleetManager(workspace_root=str(project_root))
        print("SUCCESS: FleetManager instantiated.")

        handy = HandyAgent(file_path="dummy.py")
        print("SUCCESS: HandyAgent instantiated.")

        return True
    except Exception as e:
        print(f"FAILURE: Error during instantiation: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=== PyAgent Readiness Test ===")
    if test_imports():
        print("\nRESULT: PASS - Refactored classes are working correctly.")
        sys.exit(0)
    else:
        print("\nRESULT: FAIL - Critical import or initialization error.")
        sys.exit(1)
