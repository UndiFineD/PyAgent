<<<<<<< HEAD:test_phase26.py
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
Test Phase26 module.
"""

>>>>>>> b0f03c9ef (chore: repository-wide stability and Pylint 10/10 compliance refactor):tests/phases/test_phase26.py
from pathlib import Path
<<<<<<< HEAD:test_phase26.py
<<<<<<< HEAD:test_phase26.py
sys.path.append(str(Path(__file__).parent / "src"))
=======
>>>>>>> 0777c397c (phase 320):tests/phases/test_phase26.py
=======
>>>>>>> d6712a17b (phase 320):tests/phases/test_phase26.py

from classes.fleet.FleetManager import FleetManager

def test_phase26() -> None:
    print("--- Phase 26 Verification: Neural Symbiosis & Autonomous Infrastructure ---")
    workspace_root = Path(__file__).parent
    fleet = FleetManager(str(workspace_root))
    
    # 1. Test Cognitive Borrowing
    print("\n[1/2] Testing Cognitive Borrowing (Skill Transfer)...")
    fleet.cognitive_borrowing.establish_bridge("Linguistic", "Reasoner")
    skill_pattern = fleet.cognitive_borrowing.borrow_skill("Linguistic", "Complex logical deduction")
    
    if skill_pattern and "PATTERN" in skill_pattern:
        print(f"✅ Cognitive borrowing successful: {skill_pattern}")
    else:
        print("❌ Cognitive borrowing failed.")

    # 2. Test Resilience Manager
    print("\n[2/2] Testing Resilience Manager (Resource Optimization)...")
    optimization = fleet.resilience_manager.optimize_resource_allocation()
    
    if "rebalanced_agents" in optimization:
        print(f"✅ Resilience optimization confirmed: {optimization}")
    else:
        print("❌ Resilience optimization failed.")

if __name__ == "__main__":
    test_phase26()