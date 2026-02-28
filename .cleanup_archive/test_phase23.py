<<<<<<< HEAD:test_phase23.py
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
Test Phase23 module.
"""

import pytest
import asyncio
>>>>>>> b0f03c9ef (chore: repository-wide stability and Pylint 10/10 compliance refactor):tests/phases/test_phase23.py
from pathlib import Path
<<<<<<< HEAD:test_phase23.py
<<<<<<< HEAD:test_phase23.py
sys.path.append(str(Path(__file__).parent / "src"))
=======
>>>>>>> 0777c397c (phase 320):tests/phases/test_phase23.py
=======
>>>>>>> d6712a17b (phase 320):tests/phases/test_phase23.py

from classes.fleet.FleetManager import FleetManager

def test_phase23() -> None:
    print("--- Phase 23 Verification: NAS & Core Expansion ---")
    workspace_root = Path(__file__).parent
    fleet = FleetManager(str(workspace_root))
    
    # 1. Test NAS Agent
    print("\n[1/2] Testing Neural Architecture Search...")
    task = "High-speed tensor processing for financial sentiment"
    arch = fleet.nas.search_optimal_architecture(task)
    
    if "architecture_type" in arch:
        print(f"✅ NAS suggested: {arch['architecture_type']} with rank {arch.get('rank')}")
    else:
        print("❌ NAS search failed.")

    # 2. Test Core Expansion Agent
    print("\n[2/2] Testing Core Expansion (Environment Audit)...")
    env = fleet.core_expansion.audit_environment()
    
    if len(env) > 0:
        print(f"✅ Environment audit successful. Found {len(env)} packages.")
        # Check for a common package
        has_requests = any("requests" in pkg.lower() for pkg in env)
        if has_requests:
            print("   (Confirmed presence of 'requests')")
    else:
        print("❌ Environment audit returned no packages.")

if __name__ == "__main__":
    test_phase23()