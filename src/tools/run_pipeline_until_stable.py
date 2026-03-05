#!/usr/bin/env python3
from __future__ import annotations

"""Run run_full_pipeline.py repeatedly until no further changes are detected.
Exit when run_full_pipeline.py returns exit code 10 (stable), or after max iterations.
"""
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RFP = ROOT / "src" / "tools" / "run_full_pipeline.py"
PY = sys.executable


def main() -> int:
    """Run `run_full_pipeline.py` until stable. Returns exit code.

    Safe to import: no top-level sys.exit() or long-running loops.
    """
    MAX_ITER = 50
    SLEEP_BETWEEN = 1

    for i in range(1, MAX_ITER + 1):
        print(f"Run {i}/{MAX_ITER}: invoking pipeline...")
        start = time.time()
        p = subprocess.run([PY, str(RFP)])
        elapsed = time.time() - start
        print(f"Pipeline run {i} exited {p.returncode} in {elapsed:.1f}s")
        if p.returncode == 10:
            print("No changed files detected — stable. Stopping loop.")
            return 0
        if p.returncode != 0:
            print("Pipeline returned non-zero; stopping early.")
            return p.returncode
        # otherwise, changes were processed; loop again
        time.sleep(SLEEP_BETWEEN)

    print(f"Reached max iterations ({MAX_ITER}); stopping.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
