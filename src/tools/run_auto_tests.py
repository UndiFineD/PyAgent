#!/usr/bin/env python3
"""Run only generated `test_auto_*.py` tests under `tests/unit/`.
This script collects matching test files and invokes pytest on them directly to avoid
collecting unrelated tests.
"""
from __future__ import annotations
from pathlib import Path
import sys
import argparse
import concurrent.futures
import subprocess
import os

ROOT = Path(__file__).resolve().parents[2]
TESTS_DIR = ROOT / 'tests' / 'unit'


def _run_file(path_str: str) -> tuple[str, int]:
    p = subprocess.run([sys.executable, path_str])
    return (path_str, p.returncode)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--workers', '-w', type=int, default=0, help='Number of parallel workers (0=auto)')
    args = parser.parse_args()

    files = sorted(TESTS_DIR.glob('test_auto_*.py'))
    if not files:
        print('No generated tests found (test_auto_*.py)')
        return 0
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
                print('FAILED:', path, '-', e)
                continue
            if code != 0:
                failures += 1
                print('FAILED:', path, f'exit {code}')
    if failures:
        print(f'{failures} test files failed')
    else:
        print('All generated tests passed')
    return 0 if failures == 0 else 2


if __name__ == '__main__':
    raise SystemExit(main())
