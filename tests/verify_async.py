import asyncio
import time
from pathlib import Path
from unittest.mock import MagicMock
import sys
import os

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

try:
    from agent import Agent
except ImportError as e:
    print(f"Could not import Agent: {e}")
    sys.exit(1)

async def test_async_concurrency():
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
