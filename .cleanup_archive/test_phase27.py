<<<<<<< HEAD:test_phase27.py
import sys
=======
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
Test Phase27 module.
"""

>>>>>>> b0f03c9ef (chore: repository-wide stability and Pylint 10/10 compliance refactor):tests/phases/test_phase27.py
from pathlib import Path
<<<<<<< HEAD:test_phase27.py
<<<<<<< HEAD:test_phase27.py
sys.path.append(str(Path(__file__).parent / "src"))
=======
>>>>>>> 0777c397c (phase 320):tests/phases/test_phase27.py
=======
>>>>>>> d6712a17b (phase 320):tests/phases/test_phase27.py

from classes.fleet.FleetManager import FleetManager

def test_phase27() -> None:
    print("--- Phase 27 Verification: Fractal Orchestration & Swarm Singularity ---")
    workspace_root = Path(__file__).parent
    fleet = FleetManager(str(workspace_root))
    
    # 1. Test Fractal Orchestration
    print("\n[1/2] Testing Fractal Orchestration (Recursive Decomposition)...")
    res = fleet.fractal_orchestrator.execute_fractal_task("Handle a nested architectural overhaul.")
    
    if "Depth 1" in res:
        print(f"✅ Fractal orchestration confirmed: {res}")
    else:
        print(f"❌ Fractal orchestration failed: {res}")

    # 2. Test Architect Agent
    print("\n[2/2] Testing Architect Agent (Structural Evolution)...")
    pivot = fleet.architect.suggest_architectural_pivot("Latency peaks at 200ms during shm sync.")
    
    if "component" in pivot:
        print(f"✅ Architectural pivot suggested: {pivot['proposed_change']} for {pivot['component']}")
    else:
        print("❌ Architect agent failed to suggest pivot.")

if __name__ == "__main__":
    test_phase27()