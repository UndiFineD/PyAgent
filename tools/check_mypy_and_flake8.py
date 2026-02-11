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

"""Re-run mypy and flake8 for files listed in lint_results.json and update results."""
import json
import subprocess
from pathlib import Path
import sys
import shutil
import datetime

ROOT = Path(__file__).resolve().parents[1]
LINT_FILE = ROOT / "lint_results.json"


def run_cmd(cmd):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True)
        return {"exit_code": p.returncode, "stdout": p.stdout, "stderr": p.stderr}
    except FileNotFoundError as e:
        return {"exit_code": 127, "stdout": "", "stderr": str(e)}


def main():
    if not LINT_FILE.exists():
        print("lint_results.json not found")
        return 2

    ts = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
    bak = LINT_FILE.with_name(LINT_FILE.name + ".bak2." + ts)
    shutil.copy2(LINT_FILE, bak)
    print(f"backup written to {bak}")

    data = json.loads(LINT_FILE.read_text(encoding="utf-8"))
    updated = []
    total_tools = 0
    for entry in data:
        # normalize: move any top-level mypy/flake8 into a tools map
        tools = entry.get("tools") or {}
        for k in ("mypy", "flake8"):
            if k in entry and k not in tools:
                tools[k] = entry.pop(k)
        f = Path(entry["file"])
        if not f.exists():
            f = ROOT / entry["file"]

        # Re-run mypy/flake8 for entries that have either tool listed
        if "mypy" in tools or "flake8" in tools:
            print(f"checking mypy/flake8 for: {entry['file']}")
            mypy_res = run_cmd([sys.executable, "-m", "mypy", str(f)])
            flake_res = run_cmd([sys.executable, "-m", "flake8", str(f)])
            tools["mypy"] = {"exit_code": mypy_res["exit_code"], "stdout": mypy_res["stdout"], "stderr": mypy_res["stderr"]}
            tools["flake8"] = {"exit_code": flake_res["exit_code"], "stdout": flake_res["stdout"], "stderr": flake_res["stderr"]}

        # Remove succeeded tools
        for name in list(tools.keys()):
            t = tools[name]
            if t.get("exit_code") == 0:
                tools.pop(name, None)

        if tools:
            total_tools += len(tools)
            entry["tools"] = tools
            updated.append(entry)

    out = LINT_FILE.with_name(LINT_FILE.name + ".postmypyflake8." + ts)
    out.write_text(json.dumps(updated, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"wrote updated lint_results to {out}")
    print(f"remaining files: {len(updated)}, remaining tool entries: {total_tools}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
