#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
INPUT = ROOT / "lint_results.json"
BACKUP = ROOT / "lint_results.json.bak"

with open(INPUT, "r", encoding="utf-8") as f:
    data = json.load(f)

# Backup
with open(BACKUP, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

# Filter: keep entries where NOT(all three tools have exit_code == 0)
filtered = []
for entry in data:
    try:
        flake_ok = entry.get("flake8", {}).get("exit_code") == 0
        ruff_ok = entry.get("ruff", {}).get("exit_code") == 0
        mypy_ok = entry.get("mypy", {}).get("exit_code") == 0
    except Exception:
        # If structure unexpected, keep the entry for safety
        filtered.append(entry)
        continue

    if not (flake_ok and ruff_ok and mypy_ok):
        filtered.append(entry)

# Write filtered results back
with open(INPUT, "w", encoding="utf-8") as f:
    json.dump(filtered, f, indent=2)

print(f"Original entries: {len(data)}")
print(f"Kept entries: {len(filtered)}")
print(f"Backup written to: {BACKUP}")
