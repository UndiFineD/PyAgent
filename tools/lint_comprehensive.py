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

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any

# Configure search paths
ROOT_DIR = Path(__file__).parent.parent.resolve()
SRC_DIR = ROOT_DIR / "src"
TESTS_DIR = ROOT_DIR / "tests"
OUTPUT_FILE = ROOT_DIR / "lint_results.json"


async def run_tool(cmd: List[str], file_path: str) -> Dict[str, Any]:
    """Runs a linting tool on a specific file and returns the output."""
    process = await asyncio.create_subprocess_exec(
        *cmd,
        file_path,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    
    return {
        "exit_code": process.returncode,
        "stdout": stdout.decode().strip(),
        "stderr": stderr.decode().strip()
    }


async def lint_file(file_path: Path, semaphore: asyncio.Semaphore) -> Dict[str, Any]:
    """Runs flake8, ruff, and mypy on a single file."""
    async with semaphore:
        rel_path = str(file_path.relative_to(ROOT_DIR))
        print(f"Checking: {rel_path}...")
        
        # Run tools
        results = await asyncio.gather(
            run_tool([sys.executable, "-m", "flake8", "--max-line-length=120"], str(file_path)),
            run_tool([sys.executable, "-m", "ruff", "check"], str(file_path)),
            run_tool([sys.executable, "-m", "mypy", "--ignore-missing-imports"], str(file_path))
        )
        
        return {
            "file": rel_path,
            "flake8": results[0],
            "ruff": results[1],
            "mypy": results[2]
        }


async def main():
    """Main execution loop."""
    print(f"Starting comprehensive linting for {SRC_DIR} and {TESTS_DIR}")
    
    # Directories to exclude if needed (e.g., large external candidate folders)
    EXCLUDE_DIRS = ["external_candidates", "__pycache__", ".venv", ".git"]
    
    python_files = []
    for root in [SRC_DIR, TESTS_DIR]:
        for path in root.rglob("*.py"):
            if not any(ex in path.parts for ex in EXCLUDE_DIRS):
                python_files.append(path)
    
    print(f"Found {len(python_files)} files to check (after exclusions).")
    
    all_results = []
    semaphore = asyncio.Semaphore(8)  # Adjust based on CPU cores
    
    tasks = [lint_file(f, semaphore) for f in python_files]
    
    # Process in chunks to save progress
    chunk_size = 10
    for i in range(0, len(tasks), chunk_size):
        chunk = tasks[i : i + chunk_size]
        results = await asyncio.gather(*chunk)
        all_results.extend(results)
        
        # Save progress
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(all_results, f, indent=2)
        
        print(f"Progress: {min(i + chunk_size, len(tasks))}/{len(tasks)} files processed.")
    
    print(f"\nLinting complete. Results saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    asyncio.run(main())
