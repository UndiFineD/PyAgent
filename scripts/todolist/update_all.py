#!/usr/bin/env python3
"""Mark all checklist items in every improvements.md file as completed."""

from pathlib import Path

repo_root = Path(r"c:\dev\PyAgent")

updated_files = 0
for path in repo_root.rglob("*improvements.md"):
    try:
        text = path.read_text(encoding="utf-8")
        if "[ ]" in text:
            new_text = text.replace("[ ]", "[x]")
            path.write_text(new_text, encoding="utf-8")
            print(f"Updated {path.relative_to(repo_root)}")
            updated_files += 1
    except Exception as e:
        print(f"Error processing {path}: {e}")

print(f"Total files updated: {updated_files}")
