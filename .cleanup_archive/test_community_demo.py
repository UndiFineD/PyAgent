#!/usr/bin/env python3
<<<<<<< HEAD:test_community_demo.py
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
Test Community Demo module.
"""

#!/usr/bin/env python3
>>>>>>> b0f03c9ef (chore: repository-wide stability and Pylint 10/10 compliance refactor):tests/community/test_community_demo.py
import logging
from pathlib import Path

# Add project root to sys.path

from src.classes.fleet.AgentRegistry import AgentRegistry
from src.version import SDK_VERSION

def test_community_demo() -> None:
    print(f"--- Running Community Demo Test (SDK {SDK_VERSION}) ---")
    workspace = Path('.').resolve()
    
    agents = AgentRegistry.get_agent_map(workspace)
    
    print("Loading CommunityDemo Agent...")
    try:
        agent = agents["CommunityDemo"]
        print(f"Agent Type: {type(agent).__name__}")
        
        test_input = "Hello PyAgent World!"
        result = agent.run(test_input)
        print(f"Input: {test_input}")
        print(f"Output: {result}")
    except KeyError as e:
        print(f"CommunityDemo agent not found in registry: {e}")
    except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
        print(f"Error loading agent: {e}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_community_demo()
