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

"""Run run_full_pipeline.py repeatedly until no further changes are detected.
Exit when run_full_pipeline.py returns exit code 10 (stable), or after max iterations.
"""
from __future__ import annotations
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RFP = ROOT / 'src' / 'tools' / 'run_full_pipeline.py'
PY = sys.executable

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
        sys.exit(0)
    if p.returncode != 0:
        print("Pipeline returned non-zero; stopping early.")
        sys.exit(p.returncode)
    # otherwise, changes were processed; loop again
    time.sleep(SLEEP_BETWEEN)

print(f"Reached max iterations ({MAX_ITER}); stopping.")
sys.exit(0)
