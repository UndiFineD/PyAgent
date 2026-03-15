#!/usr/bin/env python3
"""Script to analyze PyAgent improvement list and count remaining items.
"""

import re


def count_todo_items(file_path):
    """Count total and completed items in a file."""
    total = 0
    completed = 0

    try:
        with open(file_path, 'r') as f:
            content = f.read()

        # Look for checklist items (lines with or [x])
        lines = content.split('\n')
        for line in lines:
            if '[ ]' in line or '[x]' in line:
                total += 1
                if '[x]' in line:
                    completed += 1

    except Exception as e:
        print(f"Error reading {file_path}: {e}")

    return total, completed

def analyze_todo_list():
    """Analyze the entire list structure."""
    _file = r"c:\dev\PyAgent\docs\todo-tree-20260303-1743.txt"

    print("Analyzing PyAgent Improvement list")
    print("=" * 50)

    # Count total items from the file
    total_items = 0
    completed_items = 0

    # Parse the file to count items
    with open(todo_file, 'r') as f:
        content = f.read()

    # Split into lines and count checklist items
    lines = content.split('\n')
    for line in lines:
        if '[ ]' in line or '[x]' in line:
            total_items += 1
            if '[x]' in line:
                completed_items += 1

    print(f"Total checklist items: {total_items}")
    print(f"Completed items: {completed_items}")
    print(f"Remaining items: {total_items - completed_items}")
    print(f"Completion percentage: {(completed_items/total_items)*100:.1f}%")

    # Count total files
    files = []
    for line in lines:
        if '.improvements.md' in line and not line.strip().startswith('├─'):
            # Extract file path
            file_match = re.search(r'([^\s]+\.improvements\.md)', line)
            if file_match:
                files.append(file_match.group(1))

    print(f"\nTotal improvement files: {len(set(files))}")

    # Show some sample files
    print("\nSample files:")
    sample_files = list(set(files))[:10]
    for f in sample_files:
        print(f"  - {f}")

if __name__ == "__main__":
    analyze_todo_list()
