#!/usr/bin/env python3
<<<<<<< HEAD:test_community_orchestrator.py
import sys
=======
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
Test Community Orchestrator module.
"""

#!/usr/bin/env python3
>>>>>>> b0f03c9ef (chore: repository-wide stability and Pylint 10/10 compliance refactor):tests/community/test_community_orchestrator.py
import logging
from pathlib import Path

# Add project root to sys.path

from src.classes.fleet.OrchestratorRegistry import OrchestratorRegistry
from src.version import SDK_VERSION

class MockFleet:
    def __init__(self, root: Path):
        self.workspace_root = root

def test_community_orchestrator() -> None:
    print(f"--- Running Community Orchestrator Test (SDK {SDK_VERSION}) ---")
    workspace = Path('.').resolve()
    fleet = MockFleet(workspace)
    
    orc_map = OrchestratorRegistry.get_orchestrator_map(fleet)
    
    print("Loading CommunityDemoOrc...")
    try:
        # Using getattr since it's a LazyOrchestratorMap
        orc = getattr(orc_map, "CommunityDemoOrc")
        print(f"Orchestrator Type: {type(orc).__name__}")
        
        result = orc.coordinate("Ping Fleet")
        print(f"Result: {result}")
<<<<<<< HEAD:test_community_orchestrator.py
        
    except Exception as e:
=======

    except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
>>>>>>> b0f03c9ef (chore: repository-wide stability and Pylint 10/10 compliance refactor):tests/community/test_community_orchestrator.py
        print(f"Error loading orchestrator: {e}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_community_orchestrator()
