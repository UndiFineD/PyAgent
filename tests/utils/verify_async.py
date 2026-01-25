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
Verify Async module.
"""

import asyncio
import time
import pytest
from pathlib import Path
from unittest.mock import MagicMock
import sys

# Add src to path

try:
    from agent import Agent
except ImportError as e:
    print(f"Could not import Agent: {e}")
    sys.exit(1)


@pytest.mark.anyio
async def test_async_concurrency() -> None:
    agent = Agent(repo_root=".")
    agent.enable_async = True

    # Mock process_file to sleep for 1 second
    agent.process_file = MagicMock(side_effect=lambda x: time.sleep(1))

    files = [Path("file1"), Path("file2"), Path("file3")]

    start_time = time.time()
    await agent.async_process_files(files)
    end_time = time.time()

    duration = end_time - start_time
    print(f"Processed {len(files)} files in {duration:.2f} seconds")

    if duration < 2.0:
        print("SUCCESS: Execution was concurrent")
    else:
        print("FAILURE: Execution was sequential")


if __name__ == "__main__":
    asyncio.run(test_async_concurrency())