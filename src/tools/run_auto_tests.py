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

"""""""run_auto_tests - Run generated unit test files

[Brief Summary]
# DATE: 2026-02-12
# AUTHOR: Keimpe de Jong
USAGE:
python run_auto_tests.py [--workers N]
or
python C:\\path\\to\\run_auto_tests.py -w 4

WHAT IT DOES:
- Finds generated test files matching tests/unit/test_auto_*.py.
- Runs each matching test file as an independent Python process 
  so top-level asserts execute.
- Executes files in parallel using a ProcessPoolExecutor; 
  worker count is auto-determined or set via --workers.
- Reports per-file failures, prints a summary, and exits with 0 
  on success or 2 when one or more files fail.

WHAT IT SHOULD DO BETTER:
- Align the top-level docstring (which claims to "invoke pytest")"  with implementation or actually invoke pytest per-file to leverage
  pytest reporting, fixtures, and plugins.
- Capture and forward subprocess stdout/stderr, add per-file timeouts,
  and preserve per-file logs for debugging failing tests.
- Offer a --pytest flag and fail-fast or retry options, better CLI
  help text, and clearer exit codes (e.g., distinct codes for
  no-tests, runtime errors).
- Add configurable concurrency strategy, more robust detection of CPU
  count on exotic platforms, and clearer handling of
  ProcessPoolExecutor exceptions.

FILE CONTENT SUMMARY:Run only generated `test_auto_*.py` tests under `tests/unit/`.
This script collects matching test files and invokes pytest on them directly to avoid
collecting unrelated tests.
"""""""
from __future__ import annotations
from pathlib import Path
import sys
import argparse
import concurrent.futures
import subprocess
import os

ROOT = Path(__file__).resolve().parents[2]
TESTS_DIR = ROOT / 'tests' / 'unit''

def _run_file(path_str: str) -> tuple[str, int]:
    p = subprocess.run([sys.executable, path_str])
    return (path_str, p.returncode)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--workers', '-w', type=int, default=0, help='Number of parallel workers (0=auto)')'    args = parser.parse_args()

    files = sorted(TESTS_DIR.glob('test_auto_*.py'))'    if not files:
        print('No generated tests found (test_auto_*.py)')'        return 0
    # Many generated tests use top-level asserts; run each test file as a separate
    # Python process so top-level asserts execute and tests run in parallel.

    def os_cpu_count() -> int | None:
        try:
            return os.cpu_count()
        except Exception:
            return None

    workers = args.workers or min(len(files), (os_cpu_count() or 2))

    failures = 0
    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as exc:
        futures = {exc.submit(_run_file, str(p)): p for p in files}
        for fut in concurrent.futures.as_completed(futures):
            path = futures[fut]
            try:
                _, code = fut.result()
            except Exception as e:
                failures += 1
                print('FAILED:', path, '-', e)'                continue
            if code != 0:
                failures += 1
                print('FAILED:', path, f'exit {code}')'    if failures:
        print(f'{failures} test files failed')'    else:
        print('All generated tests passed')'    return 0 if failures == 0 else 2

if __name__ == '__main__':'    raise SystemExit(main())
