#!/usr/bin/env python3
"""Clean `lint_results.json` by removing tool entries with exit_code==0
and dropping files that no longer have failures. Writes a cleaned copy
`lint_results.json.cleaned.<ts>` and prints a short summary.
"""
import json
from pathlib import Path
import datetime

ROOT = Path(__file__).resolve().parents[1]
LINT_FILE = ROOT / "lint_results.json"


def main() -> int:
    if not LINT_FILE.exists():
        print("lint_results.json not found")
        return 2

    data = json.loads(LINT_FILE.read_text(encoding="utf-8"))
    orig_count = len(data)
    removed_files = []
    kept = []

    for entry in data:
        # normalize tools map
        tools = entry.get("tools") or {}
        for k in ("mypy", "flake8", "ruff"):
            if k in entry and k not in tools:
                tools[k] = entry.pop(k)
        # remove successful tools
        to_remove = [k for k, v in tools.items() if isinstance(v, dict) and v.get("exit_code") == 0]
        for k in to_remove:
            tools.pop(k, None)

        if tools:
            entry["tools"] = tools
            kept.append(entry)
        else:
            removed_files.append(entry.get("file"))

    ts = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
    out = LINT_FILE.with_name(LINT_FILE.name + f".cleaned.{ts}")
    out.write_text(json.dumps(kept, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"original entries: {orig_count}")
    print(f"removed files (fully fixed): {len(removed_files)}")
    if removed_files:
        for f in removed_files[:50]:
            print(f"  - {f}")
    print(f"remaining entries: {len(kept)}")
    print(f"wrote cleaned file: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
