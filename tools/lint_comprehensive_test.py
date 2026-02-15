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
import sys
import warnings
from pathlib import Path
from typing import Dict, List, Any

# Windows-specific noise suppression for asyncio subprocesses
if sys.platform == "win32":
    import asyncio.proactor_events

    _original_del = asyncio.proactor_events._ProactorBasePipeTransport.__del__

    def _silence_event_loop_closed(self):
        try:
            _original_del(self)
        except (RuntimeError, ValueError, ImportError):
            pass

    asyncio.proactor_events._ProactorBasePipeTransport.__del__ = _silence_event_loop_closed

# Configure search paths
ROOT_DIR = Path(__file__).parent.parent.resolve()
SRC_DIR = ROOT_DIR / "src"
TESTS_DIR = ROOT_DIR / "tests"
OUTPUT_FILE = ROOT_DIR / "temp" / "lint_results.json"


async def run_tool(cmd: List[str], file_path: str, timeout: int = 60) -> Dict[str, Any]:
    """Runs a linting tool on a specific file and returns the output."""
    try:
        process = await asyncio.create_subprocess_exec(
            *cmd,
            file_path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        try:
            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=timeout)
        except asyncio.TimeoutError:
            process.kill()
            await process.wait()
            return {
                "exit_code": -1,
                "stdout": "",
                "stderr": f"Timeout after {timeout}s"
            }

        return {
            "exit_code": process.returncode,
            "stdout": stdout.decode(errors="replace").strip(),
            "stderr": stderr.decode(errors="replace").strip()
        }
    except Exception as e:
        return {
            "exit_code": -2,
            "stdout": "",
            "stderr": f"Tool error: {str(e)}"
        }


async def lint_file(file_path: Path, semaphore: asyncio.Semaphore) -> Dict[str, Any] | None:
    """Runs flake8 on a single file."""
    async with semaphore:
        rel_path = str(file_path.relative_to(ROOT_DIR))

        # Run tools
        results = await asyncio.gather(
            run_tool([sys.executable, "-m", "flake8", "--max-line-length=120"], str(file_path))
        )

        # Only record tools with errors (non-zero exit code)
        file_record = {"file": rel_path}
        tools = ["flake8"]
        has_errors = False

        for i, tool_name in enumerate(tools):
            if results[i]["exit_code"] != 0:
                file_record[tool_name] = results[i]
                has_errors = True

        # If no tool found errors, don't record the file at all
        return file_record if has_errors else None


async def main():
    """Main execution loop."""
    print(f"Starting comprehensive linting for {SRC_DIR} and {TESTS_DIR}")
    
    # Directories to exclude if needed (e.g., large external candidate folders)
    EXCLUDE_DIRS = ["external_candidates", "__pycache__", ".venv", ".git", "node_modules", "build", "dist", "data"]

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
        # Only record files that have at least one tool error
        all_results.extend([r for r in results if r is not None])

        # Save progress
        OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(all_results, f, indent=2)

        print(f"Progress: {min(i + chunk_size, len(tasks))}/{len(tasks)} files processed.")

    print(f"\nLinting complete. Results saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nLinting interrupted by user. Partial results saved.")
        sys.exit(130)
