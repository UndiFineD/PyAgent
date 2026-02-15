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

"""Normalize lint results, run `ruff --fix` on files with `ruff` entries,
update `mypy` and `flake8` for changed files, and remove fully-fixed files
from the results.

This script writes an output file `lint_results.json.postruff.<ts>` and
backs up the original as `lint_results.json.bak.<ts>`.
"""

import json
import subprocess
import shutil
from pathlib import Path
import sys
import datetime


ROOT = Path(__file__).resolve().parents[1]
LINT_FILE = ROOT / "lint_results.json"


def run_cmd(cmd):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True)
        return {"exit_code": p.returncode, "stdout": p.stdout, "stderr": p.stderr}
    except FileNotFoundError as e:
        return {"exit_code": 127, "stdout": "", "stderr": str(e)}


def normalize_entry(entry):
    tools = entry.get("tools") or {}
    for k in ("ruff", "mypy", "flake8"):
        if k in entry and k not in tools:
            tools[k] = entry.pop(k)
    entry["tools"] = tools
    return entry


def main():
    if not LINT_FILE.exists():
        print(f"lint results not found at {LINT_FILE}")
        return 2

    ts = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
    bak = LINT_FILE.with_name(LINT_FILE.name + ".bak." + ts)
    shutil.copy2(LINT_FILE, bak)
    print(f"backup written to {bak}")

    data = json.loads(LINT_FILE.read_text(encoding="utf-8"))
    for e in data:
        normalize_entry(e)

    # collect files that currently have ruff entries
    ruff_files = [e["file"] for e in data if "ruff" in e.get("tools", {})]
    print(f"ruff files to process: {len(ruff_files)}")

    changed_files = []
    for rel in ruff_files:
        path = Path(rel)
        if not path.exists():
            path = ROOT / rel
        print(f"running ruff --fix on: {path}")
        # prefer running as module via the active python to ensure environment consistency
        res_fix = run_cmd([sys.executable, "-m", "ruff", "check", "--fix", str(path)])
        print(f"  ruff --fix exit={res_fix['exit_code']}")
        res_check = run_cmd([sys.executable, "-m", "ruff", "check", str(path)])

        # update entry in data
        for entry in data:
            if entry["file"] == rel:
                entry_tools = entry.setdefault("tools", {})
                entry_tools["ruff"] = {
                    "exit_code": res_check["exit_code"],
                    "stdout": res_check["stdout"],
                    "stderr": res_check["stderr"],
                }
                break

        # treat exit_code 0 as success (some tools print non-empty stdout on success)
        if res_fix["exit_code"] == 0 or res_check["exit_code"] == 0:
            changed_files.append(rel)

    # For any changed files, re-run mypy and flake8 and update entries
    for rel in changed_files:
        path = Path(rel)
        if not path.exists():
            path = ROOT / rel
        print(f"re-running mypy and flake8 for: {path}")
        mypy_res = run_cmd([sys.executable, "-m", "mypy", str(path)])
        flake_res = run_cmd([sys.executable, "-m", "flake8", str(path)])
        for entry in data:
            if entry["file"] == rel:
                tools = entry.setdefault("tools", {})
                tools["mypy"] = {
                    "exit_code": mypy_res["exit_code"],
                    "stdout": mypy_res["stdout"],
                    "stderr": mypy_res["stderr"],
                }
                tools["flake8"] = {
                    "exit_code": flake_res["exit_code"],
                    "stdout": flake_res["stdout"],
                    "stderr": flake_res["stderr"],
                }
                break

    # Remove any tool entries where exit_code == 0
    remaining = []
    total_tools = 0
    for entry in data:
        tools = entry.get("tools", {})
        for tname in list(tools.keys()):
            t = tools[tname]
            if t.get("exit_code") == 0:
                tools.pop(tname, None)
        if tools:
            total_tools += len(tools)
            remaining.append(entry)

    out = LINT_FILE.with_name(LINT_FILE.name + ".postruff." + ts)
    out.write_text(json.dumps(remaining, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"wrote updated lint_results to {out}")
    print(f"remaining files: {len(remaining)}, remaining tool entries: {total_tools}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
