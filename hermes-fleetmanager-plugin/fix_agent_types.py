#!/usr/bin/env python3
"""
Bulk script to add type annotations to all agent code files.
Adds proper return type annotations and updates parameter types.
"""

import re
from pathlib import Path


def add_type_annotations(file_path: Path) -> bool:
    """Add type annotations to an agent file. Returns True if modified."""
    content = file_path.read_text()
    original = content

    # Ensure Any is imported
    if "from typing import" not in content and "import typing" not in content:
        # Check if there's any import section
        if content.startswith("from ") or content.startswith("import "):
            # Add typing import after first import
            lines = content.split("\n")
            insert_idx = 0
            for i, line in enumerate(lines):
                if line.startswith("from ") or line.startswith("import "):
                    insert_idx = i + 1
                else:
                    break
            lines.insert(insert_idx, "from typing import Any")
            content = "\n".join(lines)
        else:
            # Add at the beginning
            content = "from typing import Any\n\n" + content
    elif "from typing import" in content and "Any" not in content:
        # Update existing typing import
        content = re.sub(r"from typing import ([^)]+)", r"from typing import \1, Any", content)

    # Fix __init__ return type
    content = re.sub(r"def __init__\(self\):\n", "def __init__(self) -> None:\n", content)

    # Fix __init__ with parameters (with proper indentation)
    content = re.sub(r"def __init__\(self, ([^)]+)\):\n", r"def __init__(self, \1) -> None:\n", content)

    # Fix execute method: update dict parameter to dict[str, Any] and add return type
    content = re.sub(
        r"def execute\(self, task: dict\):", "def execute(self, task: dict[str, Any]) -> dict[str, Any]:", content
    )
    content = re.sub(
        r"def execute\(self, task: dict\[str, Any\]\):",
        "def execute(self, task: dict[str, Any]) -> dict[str, Any]:",
        content,
    )
    # Generic execute without full type
    content = re.sub(
        r"def execute\(self, payload: dict\):", "def execute(self, payload: dict[str, Any]) -> dict[str, Any]:", content
    )

    # Fix fast_execute method
    content = re.sub(r"def fast_execute\(self, ([^)]+)\):", r"def fast_execute(self, \1) -> dict[str, Any]:", content)

    # Fix llm_execute method
    content = re.sub(r"def llm_execute\(self, ([^)]+)\):", r"def llm_execute(self, \1) -> dict[str, Any]:", content)

    # Fix other public methods that appear in agents
    # Generic pattern for methods that should return dict[str, Any]
    # This is safer - only for obvious cases

    # Update parameter types in method signatures
    # Change dict to dict[str, Any] in parameters
    content = re.sub(r"(\w+): dict(?!\[)", r"\1: dict[str, Any]", content)

    if content != original:
        file_path.write_text(content)
        return True
    return False


def main():
    code_dir = Path(__file__).parent / ".github" / "agents" / "code"

    if not code_dir.exists():
        print(f"Code directory not found: {code_dir}")
        return

    agent_files = sorted([f for f in code_dir.glob("*.py") if f.name != "__init__.py"])

    modified_count = 0
    for agent_file in agent_files:
        if add_type_annotations(agent_file):
            print(f"✓ Fixed: {agent_file.name}")
            modified_count += 1
        else:
            print(f"  Skipped: {agent_file.name}")

    print(f"\nModified {modified_count} files out of {len(agent_files)}")


if __name__ == "__main__":
    main()
