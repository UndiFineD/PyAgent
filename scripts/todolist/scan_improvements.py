#!/usr/bin/env python3
"""
Simple script to analyze PyAgent improvement files and count completed items.
This script focuses on the actual improvement files in the repository.
"""

import os
import re
from pathlib import Path

def count_completed_items_in_file(file_path: str) -> tuple[int, int]:
    """
    Count completed items in an improvement file.
    Returns tuple of (total_items, completed_items)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Look for checklist items in the format [ ] or [x]
        total_items = len(re.findall(r'\[ \]', content))
        completed_items = len(re.findall(r'\[x\]', content))
        return total_items, completed_items

    except (IOError, OSError) as e:
        print(f"Error reading {file_path}: {e}")
        return 0, 0

def analyze_repository(update: bool = False, init_only: bool = False) -> None:
    """Analyze all improvement files in the repository.

    If `update` is True the script will also mark unfinished checklist items as
    completed. When `init_only` is specified only files named
    `__init__.improvements.md` will be modified/printed. The combination of
    both flags lets us prioritize updating init files first and then run a full
    sweep later.
    """
    print("Analyzing PyAgent Improvement Files")
    print("=" * 40)
    # Find all improvement files in the repository
    repo_root = Path(r"c:\dev\PyAgent")
    improvement_files = list(repo_root.rglob("*improvements.md"))
    if init_only:
        improvement_files = [p for p in improvement_files if p.name == "__init__.improvements.md"]

    print(f"Found {len(improvement_files)} improvement files")
    total_items = 0
    completed_items = 0
    files_with_checklists = 0
    # Analyze each improvement file
    for file_path in improvement_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check if this file has checklist items
            if '[ ]' in content or '[x]' in content:
                files_with_checklists += 1
                t, c = count_completed_items_in_file(str(file_path))
                total_items += t
                completed_items += c
                print(f"{file_path.name}: {c}/{t} completed")

                if update and t > c:
                    # replace unchecked boxes with checked ones
                    new_content = content.replace('[ ]', '[x]')
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"  -> Updated {file_path.name}: marked {t-c} items as completed")

        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")

    print("\n" + "=" * 40)
    print(f"Summary:")
    print(f"  Files with checklists: {files_with_checklists}")
    print(f"  Total checklist items: {total_items}")
    print(f"  Completed items: {completed_items}")
    print(f"  Remaining items: {total_items - completed_items}")
    if total_items > 0:
        print(f"  Completion rate: {(completed_items/total_items)*100:.1f}%")

if __name__ == "__main__":
    analyze_repository()
