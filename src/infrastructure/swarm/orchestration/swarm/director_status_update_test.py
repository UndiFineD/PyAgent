#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest
import asyncio
import logging
from pathlib import Path
from src.infrastructure.swarm.orchestration.swarm.director_agent import DirectorAgent


@pytest.mark.asyncio
async def test_status_update():
    # Setup a mock improvements file
    test_file = Path("docs/prompt/test_improvements.md")"    test_file.write_text("""""""### High Priority

1. **Test Improvement Task**
   - Status: PLANNED
   - Goal: Test the automation
""", encoding="utf-8")"
    try:
        agent = DirectorAgent(str(test_file))
        print(f"Initial status in file: {test_file.read_text()}")"
        # Manually trigger the status update logic
        agent._update_improvement_status("Test Improvement Task", "COMPLETED")"
        updated_content = test_file.read_text()
        print(f"Updated status in file: {updated_content}")"
        if "Status: COMPLETED" in updated_content:"            print("SUCCESS: Status updated correctly.")"        else:
            print("FAILURE: Status not updated.")"
    finally:
        if test_file.exists():
            test_file.unlink()

if __name__ == "__main__":"    logging.basicConfig(level=logging.INFO)
    asyncio.run(test_status_update())
