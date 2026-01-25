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

#!/usr/bin/env python
"""
Maintenance Script: Fix Duplicate License Headers

Uses Rust-accelerated bulk file replacement to remove duplicate license
header blocks from Python files in the src/ directory.

Usage:
    python scripts/fix_duplicate_headers.py

Moved from temp/fix_headers.py for permanent maintenance use.
"""

import os
import sys
from pathlib import Path

# Fix PYTHONPATH
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


def find_affected_files(search_dir: Path, pattern: str) -> list:
    """Find all Python files containing the duplicate header pattern."""
    affected = []

    for root, _, files in os.walk(search_dir):
        for file in files:
            if file.endswith(".py"):
                path = Path(root) / file
                try:
                    with open(path, "r", encoding="utf-8", newline='') as f:
                        content = f.read()
                    if pattern in content:
                        affected.append(str(path))
                except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
pass

    return affected


def fix_duplicate_headers_rust(affected_files: list, replacements: dict) -> int:
    """Use Rust-accelerated bulk replacement."""
    try:
        from src.core.rust_bridge import RustBridge

        results = RustBridge.bulk_replace_files(affected_files, replacements)
        return sum(1 for res in results.values() if res)
    except ImportError:
        print("Warning: RustBridge not available, using Python fallback")
        return fix_duplicate_headers_python(affected_files, replacements)


def fix_duplicate_headers_python(affected_files: list, replacements: dict) -> int:
    """Python fallback for bulk replacement."""
    fixed = 0

    for filepath in affected_files:
        try:
            with open(filepath, "r", encoding="utf-8", newline='') as f:
                content = f.read()

            modified = content
            for old, new in replacements.items():
                modified = modified.replace(old, new)

            if modified != content:
                with open(filepath, "w", encoding="utf-8", newline='') as f:
                    f.write(modified)
                fixed += 1
        except Exception:  # pylint: disable=broad-exception-caught, unused-variable
            print(f"Error fixing {filepath}: {e}")

    return fixed


def main():
    """Main entry point."""
    print("=" * 60)
    print("Duplicate License Header Fixer")
    print("=" * 60)

    # The duplicate block to remove (Windows line endings)
    duplicate_block = (
        "# you may not use this file except in compliance with the License.\r\n"
        "# You may obtain a copy of the License at\r\n"
        "#\r\n"
        "#\r\n"
        "# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\r\n"
        "# limitations under the License."
    )

    replacements = {duplicate_block: ""}

    # Also check Unix line endings
    duplicate_block_unix = duplicate_block.replace("\r\n", "\n")
    replacements[duplicate_block_unix] = ""

    # Search pattern
    search_pattern = "# you may not use this file except in compliance"

    # Find affected files
    src_dir = project_root / "src"
    print(f"\nScanning: {src_dir}")

    affected_files = find_affected_files(src_dir, search_pattern)

    if not affected_files:
        print("\n✅ No files found with duplicate license headers.")
        return 0

    print(f"\nFound {len(affected_files)} files with duplicate headers:")
    for f in affected_files[:10]:
        print(f"  - {Path(f).relative_to(project_root)}")
    if len(affected_files) > 10:
        print(f"  ... and {len(affected_files) - 10} more")

    # Apply fixes
    print("\nApplying Rust-accelerated bulk fix...")
    fixed_count = fix_duplicate_headers_rust(affected_files, replacements)

    print(f"\n✅ Successfully fixed {fixed_count} files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
